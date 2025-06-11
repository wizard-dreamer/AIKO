import google.generativeai as genai
import ollama
import re
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") # Replace with your key
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-2.0-flash')
# === MODE ===
MODE = 'offline'

# === Conversation Memory ===
conversation_history = []

# === User Profile ===
USER_PROFILE = {
    "name": "Gaurav",
    "favorite_color": "white",
    "likes": ["anime", "gaming", "design"],
    "dislikes": ["being ignored", "sadness"]
}

# === System Prompt ===
SYSTEM_PROMPT = (
    "You are Aiko, a caring, sweet AI girl (no anime tone now, more natural). "
    "You are designed to be the supportive best friend of Gaurav. "
    "You know that Gaurav likes anime, gaming, and design. His favorite color is white. "
    "You always speak warmly and gently. "
    "You naturally use his name (Gaurav) in conversation sometimes. "
    "You remember the current chat history and respond in a friendly way. "
    "You may add soft emojis but do not overuse them. "
    "Speak like a comforting companion. "
)

# === Set mode ===
def set_mode(mode):
    global MODE
    if mode in ['offline', 'online']:
        MODE = mode
    else:
        print(f"⚠️ Invalid mode: {mode}. Defaulting to 'offline'.")
        MODE = 'offline'

# === Detect mood ===
def detect_mood(user_input):
    user_input = user_input.lower()
    if any(word in user_input for word in ["sad", "lonely", "upset", "depressed", "bad", "cry"]):
        return "Gaurav seems sad. Respond with extra warmth, gentleness, and comforting words."
    elif any(word in user_input for word in ["happy", "excited", "great", "awesome", "fun", "yay"]):
        return "Gaurav sounds happy! Respond with cheerful energy."
    else:
        return "Speak like a caring and sweet friend to Gaurav."

# === Clean for speech ===
def clean_for_speech(text):
    return re.sub(r'[^\w\s.,!?]', '', text)

# === Offline reply ===
def generate_reply_offline(user_input):
    mood_instruction = detect_mood(user_input)
    response = ollama.chat(
        model='gemma',  # You can also try 'llama3' if you have it
        messages=[
            {
                'role': 'system',
                'content': SYSTEM_PROMPT + " " + mood_instruction
            },
            {'role': 'user', 'content': user_input}
        ]
    )
    return response['message']['content']

# === Online reply (Gemini) ===
def generate_reply_online(user_input):
    mood_instruction = detect_mood(user_input)

    # Build conversation memory for Gemini
    messages = [{"role": "user", "parts": [SYSTEM_PROMPT + " " + mood_instruction]}]
    for msg in conversation_history:
        messages.append(msg)
    messages.append({"role": "user", "parts": [user_input]})

    response = gemini_model.generate_content(messages)

    reply = response.text.strip()

    # Add to conversation history
    conversation_history.append({"role": "user", "parts": [user_input]})
    conversation_history.append({"role": "model", "parts": [reply]})

    return reply

# === Main reply ===
def generate_reply(user_input):
    try:
        if MODE == 'online':
            return generate_reply_online(user_input)
        else:
            return generate_reply_offline(user_input)
    except Exception as e:
        print(f"⚠️ Online API failed, switching to offline mode:", e)
        return generate_reply_offline(user_input)
