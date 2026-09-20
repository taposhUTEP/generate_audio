import time
import requests

API_URL = "http://localhost:8000/generate"

sentences = [
    "Hello! This is the first audio generated with the ONNX pipeline.",
    "And here is the second sentence, generated and saved into a completely separate file."
]

def generate_speech_file(text: str, filename: str, exaggeration: float = 0.5):
    print(f"Synthesizing: \"{text}\"")
    start_time = time.time()
    
    # We pass 'text' and 'exaggeration' as URL query parameters to match the FastAPI route
    params = {
        "text": text,
        "exaggeration": exaggeration
    }
    
    try:
        # Give it up to 180s per generation to account for CPU inference time
        response = requests.post(API_URL, params=params, timeout=180)
        
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            elapsed = time.time() - start_time
            print(f"Saved: {filename} ({len(response.content) / 1024:.1f} KB) in {elapsed:.1f}s\n")
        else:
            print(f"Failed ({response.status_code}): {response.text}\n")
            
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}\n")

if __name__ == "__main__":
    for index, text in enumerate(sentences, start=1):
        output_filename = f"audio_{index}.wav"
        generate_speech_file(text, output_filename)

