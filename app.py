from flask import Flask, render_template, request, redirect
import json
import hashlib
from utils import hash_vote
from elgamal import encrypt_vote

app = Flask(__name__)

candidate_map = {
    "A": 1,
    "B": 2,
    "C": 3
}

with open("voters.json") as f:
    VOTERS = json.load(f)


def load_votes():
    try:
        with open("votes.json") as f:
            return json.load(f)
    except:
        return []


def save_votes(votes):
    with open("votes.json", "w") as f:
        json.dump(votes, f, indent=2)


def has_voted(voter, votes):
    return any(v["voter"] == voter for v in votes)


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        voter = request.form["voter"]
        password = request.form["password"]

        user = VOTERS.get(voter)

        if user:
            hashed_input = hashlib.sha256(password.encode()).hexdigest()

            if user["password"] == hashed_input:
                return redirect(f"/vote/{voter}")

        return "Authentication failed"

    return render_template("login.html")


@app.route("/vote/<voter>", methods=["GET", "POST"])
def vote(voter):
    if request.method == "POST":
        candidate = request.form["candidate"]
        votes = load_votes()

        if has_voted(voter, votes):
            return "Duplicate vote prevented"

        vote_data = f"{voter}:{candidate}"

        cipher = encrypt_vote(candidate_map[candidate])

        cipher_data = {
            "c1": cipher[0],
            "c2": cipher[1]
        }
        vote_hash, salt = hash_vote(vote_data, cipher)

        votes.append({
            "voter": voter,
            "cipher": cipher_data,
            "hash": vote_hash,
            "salt": salt
        })

        save_votes(votes)
        return render_template("success.html")

    return render_template("vote.html", voter=voter)


if __name__ == "__main__":
    app.run(debug=True)