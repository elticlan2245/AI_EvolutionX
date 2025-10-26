from gtts import gTTS
import tempfile
import os
from pathlib import Path

class VoiceService:
    def __init__(self):
        self.cache_dir = Path("/tmp/ai_evolutionx_voice_cache")
        self.cache_dir.mkdir(exist_ok=True)
    
    async def text_to_speech(self, text: str, language: str = "es", slow: bool = False) -> bytes:
        """Convert text to speech and return audio bytes"""
        try:
            # Generar audio con gTTS
            tts = gTTS(text=text, lang=language, slow=slow)
            
            # Guardar temporalmente
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            tts.save(temp_file.name)
            
            # Leer bytes
            with open(temp_file.name, 'rb') as f:
                audio_data = f.read()
            
            # Limpiar archivo temporal
            os.unlink(temp_file.name)
            
            return audio_data
        except Exception as e:
            raise Exception(f"Error generating speech: {str(e)}")
    
    def cleanup_old_cache(self):
        """Remove old cached files"""
        import time
        current_time = time.time()
        for file in self.cache_dir.glob("*.mp3"):
            if current_time - file.stat().st_mtime > 3600:  # 1 hour
                file.unlink()

voice_service = VoiceService()
