import json
import hashlib

SECRET_KEY = "secure_key_456"

def load_json(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except:
        return []

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# 🔐 Now supports user + vote binding
def generate_hash(data, prev_hash):
    combined = data + prev_hash + SECRET_KEY
    return hashlib.sha256(combined.encode()).hexdigest()