Using  The Ultra-Lightweight Chatterbox-ONNX Docker Image
=========================================================

It should take only around 1.5 GB space. For cpu only, generation will be a bit slow.


1. $ docker build -t local-chatterbox-onnx .

2. Mount a local folder (e.g. ./hf_cache) to /root/.cache so the ONNX weights persist
$ docker run -p 8000:8000 \
  -v $(pwd)/hf_cache:/root/.cache \
  -v $(pwd)/app.py:/app/app.py \
  local-chatterbox-onnx \
  uvicorn app:app --host 0.0.0.0 --port 8000

During first run weights are downloaded. Next runs do not download weights but send HTTP req. to hugging face for some metadata,
so we get warning about HF_TOKEN, ignore it.
Takes almost half a minute to load the model and run, so wait till you see: INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)

3. Test
$ curl -X POST "http://localhost:8000/generate" -F "text=Hello world, this is Chatterbox running on my CPU." --output output.wav
