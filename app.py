from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from utils import load_json, save_json, generate_hash

app = Flask(__name__)
app.secret_key = "super_secret_key_123"


# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        voters = load_json("voters.json")

        username = request.form["username"]
        password = request.form["password"]

        user = next((u for u in voters if u["username"] == username), None)

        if user and check_password_hash(user["password"], password):
            session["user"] = username
            return redirect("/vote")

        return "Invalid Credentials!"

    return render_template("login.html")


# ================= SIGNUP =================
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        voters = load_json("voters.json")

        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        if any(u["username"] == username for u in voters):
            return "User already exists!"

        voters.append({
            "username": username,
            "password": password
        })

        save_json("voters.json", voters)

        return redirect("/")

    return render_template("signup.html")


# ================= VOTE =================
@app.route("/vote", methods=["GET", "POST"])
def vote():
    if "user" not in session:
        return redirect("/")

    voters = load_json("voters.json")
    votes = load_json("votes.json")

    # 🔐 CHECK FROM VOTES.JSON (NOT has_voted)
    if any(v.get("username") == session["user"] for v in votes):
        return "You have already voted!"

    if request.method == "POST":
        candidate = request.form["candidate"].strip().lower()

        prev_hash = votes[-1]["hash"] if votes else "0"

        # 🔐 Include username in hash
        vote_hash = generate_hash(candidate + session["user"], prev_hash)

        votes.append({
            "username": session["user"],
            "vote": candidate,
            "hash": vote_hash,
            "prev_hash": prev_hash
        })

        save_json("votes.json", votes)

        return redirect("/success")

    return render_template("vote.html")


# ================= SUCCESS =================
@app.route("/success")
def success():
    return render_template("success.html")


# ================= ADMIN LOGIN =================
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = generate_password_hash("admin123")

@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            session["admin"] = True
            return redirect("/admin")

        return "Invalid Admin Credentials!"

    return render_template("admin_login.html")


# ================= ADMIN PANEL =================
@app.route("/admin")
def admin():
    if "admin" not in session:
        return redirect("/admin-login")

    votes = load_json("votes.json")

    valid = True
    prev_hash = "0"
    results = {}

    for v in votes:
        recalculated = generate_hash(v["vote"] + v["username"], prev_hash)

        if recalculated != v["hash"]:
            valid = False
            break

        prev_hash = v["hash"]
        results[v["vote"]] = results.get(v["vote"], 0) + 1

    return render_template("admin.html", results=results, valid=valid)


# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ================= RUN =================
if __name__ == "__main__":
    app.run(debug=True)