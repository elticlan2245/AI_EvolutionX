from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from app.db.redis import redis_client
from app.config import settings
import time

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not redis_client.client:
            return await call_next(request)
        
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"
        
        try:
            # Get current count
            count = await redis_client.get(key)
            
            if count and int(count) >= settings.RATE_LIMIT_PER_MINUTE:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Rate limit exceeded"}
                )
            
            # Increment
            if count:
                await redis_client.incr(key)
            else:
                await redis_client.set(key, 1, expire=60)
            
        except Exception:
            pass  # Don't block on rate limit errors
        
        response = await call_next(request)
        return response
