from voice_input import record_and_transcribe
from voice_output import speak
from brain import generate_reply, set_mode
import re

def remove_emojis(text):
    return re.sub(r'[^\w\s,.!?\'\"-]', '', text)

def choose_mode():
    print("\n🌐 Choose mode:")
    print("1. Online")
    print("2. Offline (Local LLM)")
    choice = input("Enter 1 or 2: ")
    return "online" if choice.strip() == "1" else "offline"

def main():
    mode = choose_mode()
    set_mode(mode)

    speak("Hello, this is Aiko! Ready to chat.")
    print("\n🤖 Aiko is ready! Say something or type 'exit' to quit.")

    while True:
        print("\n🎙️ Listening...")
        user_text = record_and_transcribe()
        print("📝 You said: ", user_text)

        if not user_text:
            speak("I couldn't hear you. Try again.")
            continue

        if "exit" in user_text.lower():
            speak("Goodbye! See you soon.")
            break

        reply = generate_reply(user_text)
        print("Aiko's Reply:", reply)
        speak(remove_emojis(reply))

if __name__ == "__main__":
    main()
