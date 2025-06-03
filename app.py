from fastapi import FastAPI, HTTPException
from piper import PiperVoice
import subprocess
import os

app = FastAPI()

# Load voices (we'll download these later)
voice_en = PiperVoice.load("en_GB-alan-low.onnx", use_cuda=False)
voice_hi = PiperVoice.load("hin-Hashir-low.onnx", use_cuda=False)

@app.post("/tts")
async def tts(text: str, lang: str = "hi"):
    try:
        # Generate WAV
        output_wav = "output.wav"
        if lang == "en":
            voice_en.synthesize(text, output_wav)
        else:
            voice_hi.synthesize(text, output_wav)
        
        # Convert to MP3
        output_mp3 = "output.mp3"
        subprocess.run(["ffmpeg", "-i", output_wav, output_mp3], check=True)
        
        # Return MP3 URL
        return {"url": f"YOUR_RENDER_URL/{output_mp3}"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
