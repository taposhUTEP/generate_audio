import os
import shutil
import re
import soundfile as sf
import numpy as np
import tempfile
import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import FileResponse
from chatterbox_onnx import ChatterboxOnnx

synth = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global synth
    print("--- Initializing Chatterbox ONNX Engine ---", flush=True)
    try:
        synth = ChatterboxOnnx(quantized=True)
        print("--- Model Loaded Successfully ---", flush=True)
    except Exception as e:
        print(f"FATAL: {traceback.format_exc()}", flush=True)
        raise e
    yield

app = FastAPI(
    title="Chatterbox ONNX Complete API",
    description="Local CPU TTS with zero-shot voice cloning and speech-to-speech conversion.",
    version="1.0.0",
    lifespan=lifespan
)

def remove_file(path: str):
    """Utility to clean up temporary audio files from the server after sending."""
    if os.path.exists(path):
        os.remove(path)

@app.get("/health", tags=["Status"])
def health():
    """Check if the service and ONNX sessions are ready."""
    return {"status": "ok", "model_loaded": synth is not None}


def split_text_into_sentences(text: str):
    # Splits on punctuation while keeping reasonable chunk sizes
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


@app.post("/generate", tags=["Text-to-Speech"])
def generate_speech(
    background_tasks: BackgroundTasks,
    text: str = Form(...),
    exaggeration: float = Form(0.5)
):
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    chunks = split_text_into_sentences(text)
    temp_wav_paths = []

    try:
        # 1. Synthesize each sentence into an isolated chunk (Memory stays flat)
        for i, chunk in enumerate(chunks):
            with tempfile.NamedTemporaryFile(suffix=f"_{i}.wav", delete=False) as tmp_chunk:
                chunk_path = tmp_chunk.name
                temp_wav_paths.append(chunk_path)

            synth.synthesize(
                text=chunk,
                target_voice_path=None,
                exaggeration=exaggeration,
                output_file_name=chunk_path,
                apply_watermark=False
            )

        # 2. Stitch the audio waveforms together into one master file
        combined_audio = []
        sample_rate = None

        for path in temp_wav_paths:
            data, sr = sf.read(path)
            sample_rate = sr
            combined_audio.append(data)
            # Add a brief 0.25s silence between sentences for natural pacing
            silence = np.zeros(int(sr * 0.25), dtype=data.dtype)
            combined_audio.append(silence)

        final_waveform = np.concatenate(combined_audio)

        # 3. Write final combined WAV
        with tempfile.NamedTemporaryFile(suffix="_full.wav", delete=False) as final_tmp:
            final_path = final_tmp.name

        sf.write(final_path, final_waveform, sample_rate)

        # Schedule cleanup
        for path in temp_wav_paths:
            background_tasks.add_task(remove_file, path)
        background_tasks.add_task(remove_file, final_path)

        return FileResponse(final_path, media_type="audio/wav", filename="speech.wav")

    except Exception as e:
        for path in temp_wav_paths:
            remove_file(path)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/clone-voice", tags=["Text-to-Speech"])
async def clone_voice(
    background_tasks: BackgroundTasks,
    text: str = Form(...),
    exaggeration: float = Form(0.5),
    reference_audio: UploadFile = File(..., description="5-15 second clean WAV of the target voice")
):
    """Zero-shot voice cloning. Upload a reference voice to speak the text."""
    # Save the uploaded reference audio to a temp file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as ref_tmp:
        shutil.copyfileobj(reference_audio.file, ref_tmp)
        ref_path = ref_tmp.name

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as out_tmp:
        out_path = out_tmp.name

    try:
        synth.synthesize(
            text=text,
            target_voice_path=ref_path,
            exaggeration=exaggeration,
            output_file_name=out_path,
            apply_watermark=False
        )
        background_tasks.add_task(remove_file, ref_path)
        background_tasks.add_task(remove_file, out_path)
        return FileResponse(out_path, media_type="audio/wav", filename="cloned_speech.wav")
    except Exception as e:
        remove_file(ref_path)
        remove_file(out_path)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/voice-convert", tags=["Speech-to-Speech"])
async def voice_convert(
    background_tasks: BackgroundTasks,
    source_audio: UploadFile = File(..., description="Audio file of the original speech to be converted"),
    reference_audio: UploadFile = File(..., description="Audio file of the target voice to clone")
):
    """Speech-to-Speech Conversion. Changes the voice of the source audio to match the reference audio."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as src_tmp:
        shutil.copyfileobj(source_audio.file, src_tmp)
        src_path = src_tmp.name

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as ref_tmp:
        shutil.copyfileobj(reference_audio.file, ref_tmp)
        ref_path = ref_tmp.name

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as out_tmp:
        out_path = out_tmp.name

    try:
        synth.voice_convert(
            source_audio_path=src_path,
            target_voice_path=ref_path,
            output_file_name=out_path
        )
        background_tasks.add_task(remove_file, src_path)
        background_tasks.add_task(remove_file, ref_path)
        background_tasks.add_task(remove_file, out_path)
        return FileResponse(out_path, media_type="audio/wav", filename="converted_speech.wav")
    except Exception as e:
        remove_file(src_path)
        remove_file(ref_path)
        remove_file(out_path)
        raise HTTPException(status_code=500, detail=str(e))

