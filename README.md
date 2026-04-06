# 🔐 Secure Web-Based EVM (Electronic Voting Machine)

## 📌 Project Overview

This project is a **Secure Web-Based Voting System** developed using Flask.  
It allows users to register, log in, cast votes, and ensures **vote integrity and security** using cryptographic techniques.

The system focuses on:
- Preventing duplicate voting
- Securing user credentials
- Detecting vote tampering
- Providing admin-side verification

---

## 🚀 Features

- 👤 User Signup & Login
- 🔐 Password Hashing (Secure Authentication)
- 🗳️ Voting System with Candidate Selection
- 🚫 One Vote per User
- 🔗 Hash Chain for Vote Integrity
- 🧑‍💼 Admin Panel for Result Verification
- ⚠️ Tampering Detection Mechanism
- 🎨 Clean UI using CSS

---

## 🛠️ Technologies Used

- Python (Flask)
- HTML, CSS
- JSON (Data Storage)
- SHA-256 Hashing
- Werkzeug Security (Password Hashing)

---

## 📂 Project Structure

"""
Secure-Web-Based-EVM/
│
├── app.py # Main Flask Application
├── utils.py # Helper functions (JSON + hashing)
├── voters.json # Stores user data
├── votes.json # Stores votes securely
│
├── templates/ # HTML Pages
│ ├── login.html
│ ├── signup.html
│ ├── vote.html
│ ├── success.html
│ ├── admin.html
│ └── admin_login.html
│
├── static/
│ └── style.css # UI Styling
"""

