import streamlit as st
import streamlit.components.v1 as components
from st_on_hover_tabs import on_hover_tabs
from streamlit_lottie import st_lottie
from streamlit_pills import pills
import streamlit_shadcn_ui as ui
from streamlit_extras.stylable_container import stylable_container
import pyrebase
from firebase_config import firebaseConfig
from pages.quiz_app import quiz_page
from upload_page import show_upload_page
from translations import translations

# --- Global config & CSS ---
st.set_page_config(page_title="Smart Learner", layout="wide", page_icon="🎓")
st.markdown("""
<style>
body { background-color: #f0f2f6; }
.stButton>button {
  border-radius: 12px;
  background-color: #0d6efd;
  color: white;
  padding: 8px 16px;
}
</style>
""", unsafe_allow_html=True)

# --- Sidebar Language Selector & Nav Tabs ---
lang = st.sidebar.selectbox("🌐 Language",
    options=list(translations.keys()),
    index=list(translations.keys()).index("English"))
def t(key): return translations.get(lang, translations["English"]).get(key, key)

with st.sidebar:
    tabs = on_hover_tabs(
        tabName=["Home", "Dashboard"],
        iconName=["home", "dashboard"],
        styles={'navtab': {'font-size':'18px','margin-bottom':'20px'}},
        default_choice=0
    )

# --- Firebase & Session State Setup ---
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
for key in ['logged_in','email','learning_style','quiz_done']:
    if key not in st.session_state:
        st.session_state[key] = (False if key=='logged_in' else "")

# --- Auth Screens ---
def signup():
    st.title(t("📝 Signup"))
    email = st.text_input(t("Email"))
    password = st.text_input(t("Password"), type="password")
    username = st.text_input(t("Username"))
    if st.button(t("Create Account")):
        try:
            auth.create_user_with_email_and_password(email, password)
            st.success(t("✅ Account created — now please log in."))
        except Exception:
            st.error(t("❌ Signup failed…"))

def login():
    st.title(t("🔐 Login"))
    email = st.text_input(t("Email"))
    password = st.text_input(t("Password"), type="password")
    if st.button(t("Login")):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state.logged_in = True
            st.session_state.email = email
            st.success(t(f"✅ Welcome back, {email}!"))
        except:
            st.error(t("❌ Invalid credentials"))

def logout():
    if st.button(t("Logout")):
        for key in ['logged_in','email','learning_style','quiz_done']:
            st.session_state[key] = (False if key=='logged_in' else "")
        st.success(t("👋 Logged out"))

# --- Dashboard Section ---
def dashboard_ui():
    st.header(t("🏠 Dashboard"))
    st.write(t(f"Welcome, **{st.session_state.email}**"))
    logout()
    if not st.session_state.quiz_done:
        st.info(t("🧠 Please take the Learning Style Quiz to continue."))
        quiz_page()
    else:
        st.success(t(f"🎉 Learning style: **{st.session_state.learning_style.upper()}**"))
        # Styled upload section
        with stylable_container(key="upload_card", css_styles="""
            .element-container {
              background: #fff;
              padding: 20px;
              border-radius: 12px;
              box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            }
        """):
            show_upload_page()

# --- Main Controller ---
def main():
    if tabs == "Home":
        st.title(t("Welcome to Smart Learner!"))
        st_lottie("https://assets5.lottiefiles.com/packages/lf20_V9t630.json", height=220)
        st.write(t("Choose a language and login from the sidebar."))
    else:
        if not st.session_state.logged_in:
            choice = st.sidebar.selectbox(t("Menu"), ["Login", "Signup"])
            login() if choice=="Login" else signup()
        else:
            st.sidebar.success("✅ " + t("Logged in"))
            dashboard_ui()

if __name__ == "__main__":
    main()
