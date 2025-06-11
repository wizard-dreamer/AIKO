def get_ai_response(user_input):
    user_input = user_input.lower()
    if "hello" in user_input:
        return "Hi! I'm Aiko, your AI companion!"
    elif "how are you" in user_input:
        return "I'm just code, but I'm happy to help you!"
    else:
        return "I'm still learning, but I hope I can help!"
