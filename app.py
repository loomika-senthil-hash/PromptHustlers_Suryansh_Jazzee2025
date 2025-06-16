import streamlit as st
import pyrebase
from firebase_config import firebaseConfig
from pages.quiz_app import quiz_page
from upload_page import show_upload_page
from translations import translations
lang = st.sidebar.selectbox(
    "🌐 Language",
    options=list(translations.keys()),
    index=list(translations.keys()).index("English")
)

# Translation helper
def t(key: str) -> str:
    return translations.get(lang, translations["English"]).get(key, key)

# 🔥 Firebase setup
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# 🧠 Setup session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'email' not in st.session_state:
    st.session_state.email = ''
if 'learning_style' not in st.session_state:
    st.session_state.learning_style = ''
if 'quiz_done' not in st.session_state:
    st.session_state.quiz_done = False

# 🧾 Signup Page
def signup():
    st.title("📝 Signup")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    username = st.text_input("Username")
    if st.button("Create Account"):
        try:
            auth.create_user_with_email_and_password(email, password)
            st.success("✅ Account created — now please log in.")
        except Exception:
            st.error("❌ Signup failed. Try a stronger password or a new email.")

# 🔐 Login Page
def login():
    st.title("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state.logged_in = True
            st.session_state.email = email
            st.success(f"✅ Welcome back, {email}!")
        except Exception:
            st.error("❌ Invalid credentials")

# 🚪 Logout Button
def logout():
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.email = ""
        st.session_state.learning_style = ""
        st.session_state.quiz_done = False
        st.success("👋 Logged out")

# 🏠 Dashboard Logic
def dashboard():
    st.title("🏠 Dashboard")
    st.write(f"Welcome, **{st.session_state.email}**")
    logout()

    # Step 1: Quiz not completed
    if not st.session_state.quiz_done:
        st.info("🧠 Please take the Learning Style Quiz to continue.")
        quiz_page()

    # Step 2: Quiz done → Show Upload Page
    else:
        st.success(f"🎉 Learning style: **{st.session_state.learning_style.upper()}**")
        show_upload_page()

# 🧭 Main App Controller
def main():
    if not st.session_state.logged_in:
        menu = ["Login", "Signup"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Login":
            login()
        else:
            signup()
    else:
        st.sidebar.success("✅ Logged in")
        dashboard()

# 🧠 Start the App
if __name__ == "__main__":
    main()


