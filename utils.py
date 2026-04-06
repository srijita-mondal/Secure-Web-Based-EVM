import json
import hashlib

SECRET_KEY = "super_secret_key_123"

def load_json(filename):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except:
        return []

def save_json(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def generate_hash(vote, prev_hash):
    data = vote + prev_hash + SECRET_KEY
    return hashlib.sha256(data.encode()).hexdigest()