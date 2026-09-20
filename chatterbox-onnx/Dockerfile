FROM python:3.11-slim

# Install system dependencies required for audio file generation
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Install ONNX runtime, Chatterbox ONNX port, and web server
RUN pip install --no-cache-dir \
    chatterbox-onnx \
    onnxruntime \
    fastapi \
    uvicorn

WORKDIR /app
COPY app.py .

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

