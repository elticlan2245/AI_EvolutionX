from PIL import Image
import base64
import io
from typing import Dict, Any
import json

class VisionService:
    def __init__(self):
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
    
    async def analyze_image(self, image_data: bytes, filename: str) -> Dict[str, Any]:
        """Analyze image and extract information"""
        try:
            # Abrir imagen
            image = Image.open(io.BytesIO(image_data))
            
            # Información básica
            info = {
                "filename": filename,
                "format": image.format,
                "mode": image.mode,
                "size": {
                    "width": image.width,
                    "height": image.height
                },
                "megapixels": round((image.width * image.height) / 1_000_000, 2),
            }
            
            # Convertir a base64 para enviar a modelo de visión
            buffered = io.BytesIO()
            image.save(buffered, format=image.format or "PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            info["base64"] = img_base64[:100] + "..."  # Preview
            info["ready_for_llm"] = True
            
            return info
            
        except Exception as e:
            raise Exception(f"Error analyzing image: {str(e)}")
    
    def is_supported_format(self, filename: str) -> bool:
        """Check if file format is supported"""
        ext = '.' + filename.split('.')[-1].lower()
        return ext in self.supported_formats

vision_service = VisionService()
