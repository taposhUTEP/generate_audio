import time
import requests

API_URL = "http://localhost:8000/generate"

sentences = [
    "What is your overall teaching philosophy, and how does it translate into daily classroom practice?",
    "How do you measure your own effectiveness as an instructor beyond end-of-semester student evaluations?"
]

def generate_speech_file(text: str, filename: str, exaggeration: float = 0.5):
    print(f"Synthesizing: \"{text}\"")
    start_time = time.time()
    
    # We pass 'text' and 'exaggeration' as form data to match the updated FastAPI route
    form_data = {
        "text": text,
        "exaggeration": exaggeration
    }
    
    try:
        # Pass the dictionary to the 'data' argument instead of 'params'
        response = requests.post(API_URL, data=form_data, timeout=180)
        
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

