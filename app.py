import streamlit as st
import pyrebase
from firebase_config import firebaseConfig
from pages.quiz_app import quiz_page
from upload_page import show_upload_page
from voice_widget import show_voice_widget  # <-- our new widget
import streamlit.components.v1 as components


# 🔥 Firebase setup
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# 🧠 Initialize session_state keys with sane defaults
for key, value in {
    'logged_in': False,
    'email': '',
    'learning_style': 'auditory',  # default for now
    'quiz_done': False,
    'show_quiz': False
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

def on_toggle_quiz():
    # Reset quiz-related state when toggling quiz visibility
    st.session_state.quiz_done = False
    st.session_state.learning_style = 'auditory'

def signup():
    st.title("📝 Signup")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    username = st.text_input("Username")
    if st.button("Create Account"):
        try:
            auth.create_user_with_email_and_password(email, password)
            st.success("✅ Account created — now log in.")
        except Exception:
            st.error("❌ Signup failed. Try a stronger password or new email.")

def login():
    st.title("🔐 Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        try:
            auth.sign_in_with_email_and_password(email, password)
            st.session_state.logged_in = True
            st.session_state.email = email
            st.success(f"✅ Welcome back, {email}!")
        except Exception:
            st.error("❌ Invalid credentials")

def logout():
    if st.button("Logout"):
        for key in ['logged_in', 'email', 'quiz_done', 'show_quiz']:
            st.session_state[key] = False if isinstance(st.session_state[key], bool) else ''
        st.session_state.learning_style = 'auditory'
        st.success("👋 Logged out")

def dashboard():
    st.title("🏠 Dashboard")
    st.write(f"Welcome, **{st.session_state.email}**")
    logout()
    st.success(f"🔊 Mode: **{st.session_state.learning_style.upper()}**")
    st.markdown("---")

    # Optionally show the quiz
    st.toggle("Show quiz before upload?", key="show_quiz", on_change=on_toggle_quiz)

    if st.session_state.show_quiz and not st.session_state.quiz_done:
        st.info("🧠 Please complete the Learning Style Quiz.")
        quiz_page()  # Your quiz must set session_state.quiz_done and session_state.learning_style
    else:
        show_upload_page()
        # Now integrate the voice widget when in auditory mode
        if st.session_state.learning_style == 'auditory':
            show_voice_widget()

def main():
    st.set_page_config(page_title="Smart Learner", layout="wide")
    if not st.session_state.logged_in:
        choice = st.sidebar.selectbox("Menu", ["Login", "Signup"])
        if choice == "Login":
            login()
        else:
            signup()
    else:
        st.sidebar.success("✅ Logged in")
        dashboard()

if __name__ == "__main__":
    main()
