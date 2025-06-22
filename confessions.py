import streamlit as st
import random
import string
from datetime import datetime
import json
import os
import hashlib
import certifi
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

# --- MongoDB Setup ---
MONGO_URI = "mongodb+srv://mindmantra:minmantra%40123@cluster0.iowcnhs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI,tlsCAFile=certifi.where())
db = client.confession_wall
users_col = db.users

# JSON files for confessions (local)
CONFESSION_FILE = "confessions.json"

# Generate random anonymous username
def get_random_username():
    return "Anonymous" + ''.join(random.choices(string.digits, k=4))

# Password hashing for security 
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register or login user in MongoDB
def register_or_login_user(email, password):
    hashed_pw = hash_password(password)
    user = users_col.find_one({"email": email})

    if user is None:
        # Register new user
        username = get_random_username()
        try:
            users_col.insert_one({
                "email": email,
                "password": hashed_pw,
                "username": username
            })
            return True, f"Registered and logged in as {username}.", username
        except DuplicateKeyError:
            return False, "User already exists, please try logging in.", None

    else:
        # User exists, check password
        if user['password'] == hashed_pw:
            return True, "Login successful.", user['username']
        else:
            return False, "Incorrect password.", None

# Confession Logic
def load_confessions():
    if not os.path.exists(CONFESSION_FILE):
        return []
    with open(CONFESSION_FILE, "r") as f:
        return json.load(f)

def save_confessions(confessions):
    with open(CONFESSION_FILE, "w") as f:
        json.dump(confessions, f, indent=2)

def add_confession(username, message):
    confessions = load_confessions()
    new_confession = {
        "id": len(confessions) + 1,
        "username": username,
        "timestamp": datetime.now().strftime('%A @ %-I:%M %p'),
        "message": message,
        "replies": []
    }
    confessions.append(new_confession)
    save_confessions(confessions)

def add_reply(confession_id, username, message):
    confessions = load_confessions()
    for c in confessions:
        if c["id"] == confession_id:
            c["replies"].append({
                "username": username,
                "timestamp": datetime.now().strftime('%A @ %-I:%M %p'),
                "message": message
            })
            break
    save_confessions(confessions)

def confess():
    # --- Login system ---
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.title("🔐 Login to Confession Wall")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login / Register"):
            if email and password:
                success, msg, username = register_or_login_user(email, password)
                if success:
                    st.session_state['email'] = email
                    st.session_state['username'] = username
                    st.session_state['logged_in'] = True
                    st.success(msg)
                    st.rerun()

                else:
                    st.error(msg)
            else:
                st.warning("Please enter both email and password.")
        return

    # --- Logout option ---
    if st.button("Logout"):
        for key in ['logged_in', 'email', 'username']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    # --- Confession Wall UI ---
    st.title("🙊 Anonymous Confession Wall")
    st.markdown(f"You're posting as: **{st.session_state['username']}**")

    # Clear confession box logic
    if 'clear_new_confession' not in st.session_state:
        st.session_state['clear_new_confession'] = False
    if st.session_state['clear_new_confession']:
        st.session_state['new_confession'] = ""
        st.session_state['clear_new_confession'] = False

    new_confession = st.text_area("Write your confession (be respectful):", key="new_confession")

    if st.button("Submit Confession"):
        if st.session_state.new_confession.strip():
            add_confession(st.session_state['username'], st.session_state.new_confession.strip())
            st.success("Your anonymous confession has been posted!")
            st.session_state['clear_new_confession'] = True
            st.rerun()
        else:
            st.warning("Please write something before submitting.")

    # Show recent confessions
    st.subheader("📜 Recent Confessions")
    confessions = load_confessions()

    if not confessions:
        st.info("No confessions yet. Be the first to confess!")
        return

    for confession in reversed(confessions[-30:]):
        st.markdown(f"**{confession['username']}**: {confession['message']}")
        st.markdown(
            f"<div style='color: gray; font-size: small;'>{confession['timestamp']}</div>",
            unsafe_allow_html=True,
        )

        # Show replies
        for reply in confession['replies']:
            st.markdown(f"&nbsp;&nbsp;&nbsp; ↳ **{reply['username']}**: {reply['message']}")
            st.markdown(
                f"<div style='color: gray; font-size: small;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {reply['timestamp']}</div>",
                unsafe_allow_html=True,
            )

        # Handle reply box logic
        reply_key = f"reply_{confession['id']}"
        clear_flag_key = f"clear_{reply_key}"

        if clear_flag_key not in st.session_state:
            st.session_state[clear_flag_key] = False
        if st.session_state[clear_flag_key]:
            st.session_state[reply_key] = ""
            st.session_state[clear_flag_key] = False

        reply_text = st.text_input(f"Reply to confession {confession['id']}", key=reply_key)

        if st.button("Submit Reply", key=f"btn_{confession['id']}"):
            if st.session_state[reply_key].strip():
                add_reply(confession['id'], st.session_state['username'], st.session_state[reply_key].strip())
                st.success("Your anonymous reply has been posted!")
                st.session_state[clear_flag_key] = True
                st.rerun()
            else:
                st.warning("Please write something before submitting your reply.")

if __name__ == "__main__":
    confess()
