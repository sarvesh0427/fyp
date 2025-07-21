
import streamlit as st
import random
import string
from datetime import datetime
import hashlib
import certifi
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
import pandas as pd
import io

# --- MongoDB Setup ---
MONGO_URI = "mongodb+srv://bhujelsuja:mindmitra2001@cluster0.qihuqeg.mongodb.net/"
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client.confession_db

users_col = db.users
confessions_col = db.confession

# --- Utils Functions ---

def get_random_username():
    return "Anonymous" + ''.join(random.choices(string.digits, k=4))

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_or_login_user(email, password):
    hashed_pw = hash_password(password)
    user = users_col.find_one({"email": email})

    if user is None:
        # New registration
        username = get_random_username()
        try:
            users_col.insert_one({
                "email": email,
                "password": hashed_pw,
                "username": username
            })
            return True, f"Registered and logged in as {username}.", username
        except DuplicateKeyError:
            return False, "User already exists. Please log in.", None
    else:
        # Existing user login
        if user['password'] == hashed_pw:
            return True, "Login successful.", user['username']
        else:
            return False, "Incorrect password.", None

def load_confessions():
    return list(confessions_col.find())

def add_confession(username, message):
    new_confession = {
        "username": username,
        "timestamp": datetime.now().strftime('%A @ %I:%M %p'),
        "message": message,
        "replies": []
    }
    confessions_col.insert_one(new_confession)

def add_reply(confession_id, username, message):
    confessions_col.update_one(
        {"_id": ObjectId(confession_id)},
        {"$push": {
            "replies": {
                "username": username,
                "timestamp": datetime.now().strftime('%A @ %I:%M %p'),
                "message": message
            }
        }}
    )

# --- Admin Panel Functions ---

def export_to_csv(data_list, filename):
    df = pd.DataFrame(data_list)
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    st.download_button(
        label=f"📥 Download {filename}",
        data=buffer.getvalue(),
        file_name=f"{filename}.csv",
        mime='text/csv'
    )

def show_admin_panel():
    st.title("🛠️ Admin Panel")

    # Fetch data here
    users = list(users_col.find({}, {"_id": 0}))
    confessions = list(confessions_col.find({}, {"_id": 0}))

    # Export capability
    st.subheader("📤 Export Data")
    export_to_csv(users, "users")
    export_to_csv(confessions, "confessions")

    # Show list of users
    st.subheader("👥 Registered Users")
    for user in users:
        st.markdown(f"- **{user['username']}** | {user['email']}")

    # Show all confessions and replies with delete options
    st.subheader("🧾 All Confessions")
    for confession in reversed(load_confessions()):
        confession_id = str(confession['_id'])
        st.markdown(f"**{confession['username']}**: {confession['message']}")
        st.markdown(
            f"<div style='color: gray; font-size: small;'>{confession['timestamp']}</div>",
            unsafe_allow_html=True,
        )

        # Replies with delete option
        for i, reply in enumerate(confession.get('replies', [])):
            st.markdown(f"&nbsp;&nbsp;&nbsp; ↳ **{reply['username']}**: {reply['message']}")
            st.markdown(
                f"<div style='color: gray; font-size: small;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {reply['timestamp']}</div>",
                unsafe_allow_html=True,
            )
            if st.button("Delete Reply", key=f"del_reply_{confession_id}_{i}"):
                confessions_col.update_one(
                    {"_id": ObjectId(confession_id)},
                    {"$pull": {"replies": reply}}
                )
                st.success("Reply deleted.")
                safe_rerun()

        # Option to delete entire confession
        if st.button("🗑️ Delete Confession", key=f"delete_{confession_id}"):
            confessions_col.delete_one({"_id": ObjectId(confession_id)})
            st.success("Confession deleted.")
            safe_rerun()

def safe_rerun():
    try:
        st.experimental_rerun()
    except AttributeError:
        st.stop()

# --- Main App Functionality ---

ADMIN_EMAIL = "admin@confession.com"

def confess():
    # Login/Register
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
                    safe_rerun()
                else:
                    st.error(msg)
            else:
                st.warning("Please enter both email and password.")
        return

    # Logout button
    if st.button("Logout"):
        for key in ['logged_in', 'email', 'username']:
            st.session_state.pop(key, None)
        safe_rerun()

    # Admin panel
    if st.session_state.get('email') == ADMIN_EMAIL:
        show_admin_panel()
        return

    # Normal user view
    st.title("🙊 Anonymous Confession Wall")
    st.markdown(f"You're posting as: **{st.session_state['username']}**")

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
            safe_rerun()
        else:
            st.warning("Please write something before submitting.")

    st.subheader("📜 Recent Confessions")
    confessions = load_confessions()
    if not confessions:
        st.info("No confessions yet. Be the first to confess!")
        return

    for confession in reversed(confessions[-30:]):
        confession_id = str(confession['_id'])
        st.markdown(f"**{confession['username']}**: {confession['message']}")
        st.markdown(
            f"<div style='color: gray; font-size: small;'>{confession['timestamp']}</div>",
            unsafe_allow_html=True,
        )

        for reply in confession.get('replies', []):
            st.markdown(f"&nbsp;&nbsp;&nbsp; ↳ **{reply['username']}**: {reply['message']}")
            st.markdown(
                f"<div style='color: gray; font-size: small;'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {reply['timestamp']}</div>",
                unsafe_allow_html=True,
            )

        reply_key = f"reply_{confession_id}"
        clear_flag_key = f"clear_{reply_key}"
        if clear_flag_key not in st.session_state:
            st.session_state[clear_flag_key] = False
        if st.session_state[clear_flag_key]:
            st.session_state[reply_key] = ""
            st.session_state[clear_flag_key] = False

        st.text_input("Reply to confession", key=reply_key)
        if st.button("Submit Reply", key=f"btn_{confession_id}"):
            if st.session_state[reply_key].strip():
                add_reply(confession_id, st.session_state['username'], st.session_state[reply_key].strip())
                st.success("Your anonymous reply has been posted!")
                st.session_state[clear_flag_key] = True
                safe_rerun()
            else:
                st.warning("Please write something before submitting your reply.")

if __name__ == "__main__":
    confess()
