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

def generate_hash(data, prev_hash):
    combined = data + prev_hash + SECRET_KEY
    return hashlib.sha256(combined.encode()).hexdigest()

def encode_vote(vote):
    return ",".join(map(str, vote))

def decode_vote(vote_str):
    c1, c2 = vote_str.split(",")
    return (int(c1), int(c2))