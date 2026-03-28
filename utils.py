import hashlib
import os


def hash_vote(vote_data: str, cipher):
    salt = os.urandom(16)

    c1, c2 = cipher

    data = (
        vote_data.encode() +
        str(c1).encode() +
        str(c2).encode() +
        salt
    )

    vote_hash = hashlib.sha256(data).hexdigest()

    return vote_hash, salt.hex()


def verify_hash(vote_data: str, cipher, stored_hash: str, salt_hex: str):
    salt = bytes.fromhex(salt_hex)
    c1, c2 = cipher

    data = (
        vote_data.encode() +
        str(c1).encode() +
        str(c2).encode() +
        salt
    )

    computed_hash = hashlib.sha256(data).hexdigest()

    return computed_hash == stored_hash