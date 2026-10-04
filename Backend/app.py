from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
import requests
import tempfile
import base64
import os
from dotenv import load_dotenv

# Load environment variables from .env file for local development
load_dotenv()

app = Flask(__name__)
CORS(app)

MURF_API_KEY = os.environ.get("MURF_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

# Initialize Gemini Client if API key is provided
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

PROMPTS = {
    "Summary": """
You are a professional tourist guide.
Provide a high-level overview of "{place}" in {language}.

Focus on:
- The historical significance
- Why the place is famous
- Key architectural or cultural highlights

Keep the explanation concise, engaging, and easy to follow.
Avoid excessive details and dates.
Limit the response to around 200 words.

Respond ONLY in {language}.
""",

    "Detailed": """
You are a professional tourist guide.
Provide a detailed and immersive explanation of "{place}" in {language}.

Cover:
- Historical background and timeline
- Architectural design and unique features
- Cultural importance and notable events
- Interesting facts and visitor insights

Explain concepts clearly and in a storytelling manner.
Include relevant details and examples to create a rich experience.
Limit the response to around 400 words.

Respond ONLY in {language}.
"""
}

def generate_speech(text, voice_id, locale):
    temp_audio = tempfile.NamedTemporaryFile(
        suffix=".mp3",
        delete=False
    )
   
    url = "https://global.api.murf.ai/v1/speech/stream"
    headers = {
        "api-key": MURF_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "voice_id": voice_id,
        "text": text,
        "locale": locale,
        "model": "FALCON",
        "format": "MP3",
        "sampleRate": 24000,
        "channelType": "MONO"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        with open(temp_audio.name, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print("Audio streaming completed")
        return temp_audio
    else:
        print(f"Murf API Error: {response.status_code} - {response.text}")
        return None


def generate_description(place, answer_type, language):
    if not client:
        raise ValueError("GEMINI_API_KEY environment variable is missing.")
    prompt = PROMPTS[answer_type].format(place=place, language=language)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text
    
@app.route("/", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "message": "Travel Guide API is running"
    })

@app.route("/generate-audio-guide", methods=["POST"])
def generate_audio_guide():
    data = request.json
    if not data:
        return jsonify({"error": "No input payload provided"}), 400

    place = data.get("place")
    answer_type = data.get("answerType", "Summary")
    language = data.get("language", "English")
    voice_id = data.get("voiceId")
    locale = data.get("locale")

    try:
        text_description = generate_description(place, answer_type, language)
    except Exception as e:
        print(f"Error generating description: {e}")
        return jsonify({"error": f"Failed to generate text description: {str(e)}"}), 500

    encoded_audio = None
    if MURF_API_KEY and voice_id and locale:
        try:
            audio_path = generate_speech(text_description, voice_id, locale)
            if audio_path:
                audio_bytes = open(audio_path.name, "rb").read()
                encoded_audio = base64.b64encode(audio_bytes).decode("utf-8")
        except Exception as e:
            print(f"Error generating audio: {e}")

    return jsonify({
        "description": text_description,
        "audioBase64": encoded_audio
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=False)