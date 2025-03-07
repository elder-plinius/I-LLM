import requests
from tempfile import NamedTemporaryFile
import os

api_key = os.getenv("ELEVENLABS_API_KEY")
def generate_speech(text, voice_id, xi_api_key, character_name):
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "Content-Type": "application/json",
            "xi-api-key": xi_api_key,
        }
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",  # Adjust model_id as necessary
            "voice_settings": {
                "stability": 0.5,  # Adjust for stability
                "similarity_boost": 0.5  # Adjust for similarity
            }
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            # Include character name in filename for uniqueness
            filename = f"output_{character_name.replace(' ', '_')}_{voice_id}.mp3"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Generated speech saved to {filename}")
        else:
            print("Failed to generate speech:", response.text)

