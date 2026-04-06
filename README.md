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

```
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
```


---

## ⚙️ How the System Works

### 1️⃣ User Registration (Signup)

- User enters username and password
- Password is hashed using:
  ```
generate_password_hash()
  ```

- Stored in `voters.json`

---

### 2️⃣ Login System

- User credentials are verified using:

```
check_password_hash()
```

- Session is created upon successful login

---

### 3️⃣ Voting Process

- User selects a candidate
- System checks:
- If user has already voted

- Vote is stored with:
- Candidate name
- Hash
- Previous hash

---

### 4️⃣ Hash Chain Mechanism 🔗

Each vote is linked to the previous vote:

```
Vote 1 → Hash 1
Vote 2 → Hash 2 (depends on Hash 1)
Vote 3 → Hash 3 (depends on Hash 2)
```

Hash is generated using:
```
SHA-256 (vote + previous_hash + secret_key)
```


👉 This ensures:
- If ANY vote is modified → chain breaks
- Tampering is detected instantly

---

### 5️⃣ Admin Panel

Admin can:
- View results
- Verify integrity

System recalculates all hashes:
- If mismatch → ⚠ Tampering detected

---

## 🔐 Security Features

### ✅ Password Security
- Passwords are hashed (not stored in plain text)

---

### ✅ Tamper Detection
- Hash chaining ensures integrity

---

### ✅ Duplicate Voting Prevention
- Each user has a `has_voted` flag

---

### ✅ Session Control
- Only logged-in users can vote

---

## ⚠️ Limitations

- Uses JSON instead of database (less scalable)
- Admin credentials are hardcoded
- No HTTPS (local deployment)
- Votes are not encrypted (only hashed)

---

## ▶️ How to Run the Project

### Step 1: Install dependencies

```
pip install flask werkzeug
```

---

### Step 2: Run the app

```
python app.py
```


---

### Step 3: Open in browser

```
http://127.0.0.1:5000/
```


---

### Step 4: Use the system

#### 👤 Signup
Create a new user

#### 🗳️ Vote
Login → select candidate → submit

#### 🧑‍💼 Admin Login

```
/admin-login
```


Default:
- Username: admin
- Password: admin123

---

## 🧪 Testing Security (Important)

Try modifying `votes.json` manually.

👉 Change any vote  
👉 Open admin panel  

Expected result:
```
⚠ Data has been tampered!
```


---

## 🔮 Future Enhancements

This system can be extended with:

### 🔐 Advanced Security
- End-to-end encryption (ElGamal / RSA)
- Digital signatures
- Blockchain-based voting

---

### 🧠 Identity Verification
- Aadhaar / Government ID verification
- OTP-based authentication

---

### 🧬 Biometric Authentication
- Fingerprint recognition
- Face recognition
- Iris scanning

---

### 🌐 Deployment & Security
- HTTPS integration
- Secure server hosting
- Cloud database (MongoDB/PostgreSQL)

---

### 📊 UI Improvements
- Graphical result visualization
- Real-time vote counting
- Interactive dashboard

---

## 🎯 Conclusion

This project demonstrates a **secure and transparent voting system** using:
- Cryptographic hashing
- Integrity verification
- Controlled access

Even with JSON storage, the system ensures:
✔ Vote security  
✔ Tamper detection  
✔ User authentication  

## ⭐ Acknowledgment

This project was developed as part of learning secure system design, web development, and cryptography concepts.

---
