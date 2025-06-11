import json

PROFILE_FILE = "user_profile.json"

def save_profile(profile):
    with open(PROFILE_FILE, "w") as f:
        json.dump(profile, f)

def load_profile():
    try:
        with open(PROFILE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
