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

# 🌐 Language Selector
if "language" not in st.session_state:
    st.session_state.language = "English"

lang = st.selectbox("🌐 " + translations[st.session_state.language]["language_label"], 
                    ["English", "தமிழ்", "हिंदी"])
st.session_state.language = lang
t = translations[lang]  # 🌍 Current translation dict

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
for key in ['logged_in', 'email', 'learning_style', 'quiz_done']:
    if key not in st.session_state:
        st.session_state[key] = (False if key == 'logged_in' else "")

# --- Auth Screens ---
def signup():
    st.title("📝 " + t["signup"])
    email = st.text_input(t["email"])
    password = st.text_input(t["password"], type="password")
    username = st.text_input(t["username"])
    if st.button(t["create_account"]):
        try:
            auth.create_user_with_email_and_password(email, password)
            st.success(t["signup_success"])
        except Exception:
            st.error(t["signup_failed"])

def login():
    st.title("🔐 " + t["login"])
    email = st.text_input(t["email"])
    password = st.text_input(t["password"], type="password")
    if st.button(t["login"]):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.session_state.logged_in = True
            st.session_state.email = email
            st.success(f"{t['welcome_back']} {email}!")
        except:
            st.error(t["invalid_credentials"])

def logout():
    if st.button(t["logout"]):
        for key in ['logged_in', 'email', 'learning_style', 'quiz_done']:
            st.session_state[key] = (False if key == 'logged_in' else "")
        st.success(t["logged_out"])

# --- Dashboard Section ---
def dashboard_ui():
    st.header("🏠 " + t["dashboard"])
    st.write(f"{t['welcome_user']} **{st.session_state.email}**")
    logout()
    if not st.session_state.quiz_done:
        st.info(t["take_quiz_msg"])
        quiz_page()
    else:
        st.success(f"🎉 {t['your_learning_style']} **{st.session_state.learning_style.upper()}**")
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
        st.title(t["home_title"])
        st_lottie("https://assets5.lottiefiles.com/packages/lf20_V9t630.json", height=220)
        st.write(t["home_message"])
    else:
        if not st.session_state.logged_in:
            choice = st.sidebar.selectbox(t["menu"], [t["login"], t["signup"]])
            login() if choice == t["login"] else signup()
        else:
            st.sidebar.success("✅ " + t["logged_in"])
            dashboard_ui()

if __name__ == "__main__":
    main()
