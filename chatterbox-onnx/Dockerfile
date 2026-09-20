FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Added python-multipart for file upload support
RUN pip install --no-cache-dir \
    chatterbox-onnx \
    onnxruntime \
    fastapi \
    uvicorn \
    python-multipart

WORKDIR /app
COPY app.py .

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

