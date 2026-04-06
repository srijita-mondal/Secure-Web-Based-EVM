from flask import Flask, render_template, request, redirect, session
import sqlite3
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "super_secret_key"

# ================= DATABASE =================

def get_db():
    return sqlite3.connect("database.db")

def init_db():
    db = get_db()
    cursor = db.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS voters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        has_voted INTEGER DEFAULT 0
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vote TEXT,
        hash TEXT,
        prev_hash TEXT
    )
    ''')

    db.commit()
    db.close()

init_db()

# ================= HASH =================

SECRET_KEY = "vote_secret"

def generate_hash(data):
    return hashlib.sha256((data + SECRET_KEY).encode()).hexdigest()

# ================= ROUTES =================

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM voters WHERE username=?", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            session["user"] = username
            return redirect("/vote")

    return render_template("login.html")

# ================= VOTE =================

@app.route("/vote", methods=["GET", "POST"])
def vote():
    if "user" not in session:
        return redirect("/")

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT has_voted FROM voters WHERE username=?", (session["user"],))
    if cursor.fetchone()[0] == 1:
        return "You have already voted!"

    if request.method == "POST":
        candidate = request.form["candidate"]

        # Get previous hash
        cursor.execute("SELECT hash FROM votes ORDER BY id DESC LIMIT 1")
        prev = cursor.fetchone()
        prev_hash = prev[0] if prev else "0"

        vote_hash = generate_hash(candidate + prev_hash)

        cursor.execute("INSERT INTO votes (vote, hash, prev_hash) VALUES (?, ?, ?)",
                       (candidate, vote_hash, prev_hash))

        cursor.execute("UPDATE voters SET has_voted=1 WHERE username=?", (session["user"],))

        db.commit()
        db.close()

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

    return render_template("admin_login.html")

# ================= ADMIN PANEL =================

@app.route("/admin")
def admin():
    if "admin" not in session:
        return redirect("/admin-login")

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT vote, hash, prev_hash FROM votes")
    votes = cursor.fetchall()

    # Verify integrity
    valid = True
    prev_hash = "0"

    results = {}

    for vote, hash_val, prev in votes:
        recalculated = generate_hash(vote + prev_hash)

        if recalculated != hash_val:
            valid = False
            break

        prev_hash = hash_val
        results[vote] = results.get(vote, 0) + 1

    return render_template("admin.html", results=results, valid=valid)

# ================= ADD VOTER =================

@app.route("/add-voter", methods=["POST"])
def add_voter():
    username = request.form["username"]
    password = generate_password_hash(request.form["password"])

    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute("INSERT INTO voters (username, password) VALUES (?, ?)", (username, password))
        db.commit()
    except:
        return "User already exists"

    return "Voter added successfully!"

# ================= RUN =================

if __name__ == "__main__":
    app.run(debug=True)