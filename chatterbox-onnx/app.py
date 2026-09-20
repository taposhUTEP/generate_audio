import os
import tempfile
import traceback
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from chatterbox_onnx import ChatterboxOnnx

synth = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global synth
    print("--- Initializing Chatterbox ONNX Engine (Downloading/Loading Weights) ---", flush=True)
    try:
        synth = ChatterboxOnnx(quantized=True)
        print("--- Model Loaded Successfully ---", flush=True)
    except Exception as e:
        print(f"FATAL: Failed to initialize model:\n{traceback.format_exc()}", flush=True)
        raise e
    yield

app = FastAPI(title="Chatterbox ONNX CPU Server", lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": synth is not None}

@app.post("/generate")
def generate_speech(text: str, exaggeration: float = 0.5):
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if synth is None:
        raise HTTPException(status_code=503, detail="Model is still loading or failed to initialize")

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
        output_path = tmp_wav.name

    try:
        synth.synthesize(
            text=text,
            target_voice_path=None,
            exaggeration=exaggeration,
            output_file_name=output_path,
            apply_watermark=False
        )
        return FileResponse(output_path, media_type="audio/wav", filename="speech.wav")
    except Exception as e:
        print(f"ERROR during synthesis:\n{traceback.format_exc()}", flush=True)
        if os.path.exists(output_path):
            os.remove(output_path)
        raise HTTPException(status_code=500, detail=str(e))

