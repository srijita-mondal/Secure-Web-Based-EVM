import hashlib

def hash_vote(vote_data: str) -> str:
    return hashlib.sha256(vote_data.encode()).hexdigest()
