import streamlit as st
import pdfplumber, docx, pptx, tempfile
from supabase_config import supabase
from google import genai
import gv_config
import streamlit.components.v1 as components

# Initialize AI client — can be used later for generating summaries, Q&A, etc.
ai_client = genai.Client(api_key=gv_config.GEMINI_API_KEY)

def show_upload_page():
    st.title("📤 Upload Your Study Material")
    st.success(f"🔊 Current mode: {st.session_state.learning_style.upper()}")

    uploaded_file = st.file_uploader("Upload PDF, PPTX, or DOCX", type=["pdf", "pptx", "docx"])
    if not uploaded_file:
        st.info("Please upload a file to continue.")
        return

    # Save upload to a temporary file
    ext = uploaded_file.name.rsplit(".", 1)[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    # Extract text based on file type
    if ext == "pdf":
        content = "\n".join(p.extract_text() or "" for p in pdfplumber.open(tmp_path).pages)
    elif ext == "docx":
        content = "\n".join(para.text for para in docx.Document(tmp_path).paragraphs)
    elif ext == "pptx":
        prs = pptx.Presentation(tmp_path)
        content = "\n".join(shape.text for s in prs.slides for shape in s.shapes if hasattr(shape, "text"))
    else:
        st.error("Unsupported file type!")
        return

    # Display extracted content
    st.subheader("🧠 Extracted Content")
    st.text_area("Preview:", content[:1000], height=300)

    # Supabase upload action
    if st.button("📤 Upload to Supabase"):
        fname = f"uploads/{uploaded_file.name}"
        try:
            supabase.storage.from_("uploads").upload(
                fname,
                open(tmp_path, "rb"),
                file_options={"upsert": False}
            )
            st.success("✅ Uploaded!")
            st.info(f"Stored at: {fname}")
        except Exception as e:
            st.error(f"❌ Upload failed: {e}")

    # Voice widget embed (assuming auditory learning style)
    if st.session_state.learning_style == "auditory":
        st.markdown("---")
        st.markdown("### 🗣️ Speak to Tutor")
        components.iframe(
            src="https://loomika-senthil-hash.github.io/voice-widget/",
            height=300,
            scrolling=False,
            allow="microphone; autoplay"
        )
