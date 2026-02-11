import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
model = "google/gemma-3-27b-it:free"

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost:8000",
    "X-Title": "Real Estate Bot Test"
}

data = {
    "model": model,
    "messages": [{"role": "user", "content": "Say 'Gemma 3 is online and ready!'"}]
}

print(f"Testing with Model: {model}")
try:
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("Success! OpenRouter is connected.")
        print(f"Response: {response.json()['choices'][0]['message']['content']}")
    else:
        print(f"Connection Failed: {response.status_code}")
        print(f"Detail: {response.text}")
except Exception as e:
    print(f"Error during test: {e}")
