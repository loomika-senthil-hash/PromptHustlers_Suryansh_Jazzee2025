import streamlit as st
import pdfplumber, docx, pptx, tempfile
from supabase_config import supabase
from google import genai
import gv_config
import streamlit.components.v1 as components
from googleapiclient.discovery import build

# Initialize AI client
ai_client = genai.Client(api_key=gv_config.GEMINI_API_KEY)

def show_upload_page():
    st.title("📤 Upload Your Study Material")
    st.success(f"🔊 Current mode: {st.session_state.learning_style.upper()}")

    uploaded_file = st.file_uploader("Upload PDF, PPTX, or DOCX", type=["pdf", "pptx", "docx"])
    if not uploaded_file:
        st.info("Please upload a file to continue.")
        return

    # Save to temp file
    ext = uploaded_file.name.rsplit(".", 1)[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    # Extract content
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

    # Show extracted content
    st.subheader("🧠 Extracted Content")
    st.text_area("Preview:", content[:1000], height=300)

    st.session_state.content = content

    # Reader/Writer Learner
    if st.session_state.learning_style == "reader":
        for action in ("summary", "story", "explain"):
            st.session_state.setdefault(action, False)

        def build_on_click(a):
            def _():
                for act in ("summary", "story", "explain"):
                    st.session_state[act] = False
                st.session_state[a] = True
            return _

        cols = st.columns(3)
        cols[0].button("📝 Summary", key="summary_btn", on_click=build_on_click("summary"))
        cols[1].button("📖 Story", key="story_btn", on_click=build_on_click("story"))
        cols[2].button("💡 Explain", key="explain_btn", on_click=build_on_click("explain"))

        if st.session_state.summary:
            resp = ai_client.generate_content(f"Summarize this in 3 bullet points:\n\n{content[:5000]}")
            st.markdown("### 📝 Summary")
            st.write(resp.text)

        elif st.session_state.story:
            resp = ai_client.generate_content(f"Write a short story that explains this:\n\n{content[:5000]}")
            st.markdown("### 📖 Story")
            st.write(resp.text)

        elif st.session_state.explain:
            resp = ai_client.generate_content(f"Explain this to a 10th grader:\n\n{content[:5000]}")
            st.markdown("### 💡 Explanation")
            st.write(resp.text)

    # Auditory Learner
    elif st.session_state.learning_style == "auditory":
        st.markdown("---")
        st.markdown("### 🗣️ Speak to Tutor")
        components.iframe(
            src="https://loomika-senthil-hash.github.io/smart_learner/",
            height=300,
            scrolling=False,
            allow="microphone; autoplay"
        )

    # Visual Learner
    elif st.session_state.learning_style == "visual":
        st.markdown("---")
        st.markdown("### 🔍 Extracting Topics from your file...")

        try:
            resp = ai_client.generate_content(
                f"List 3 key topics from this learning content:\n\n{content[:5000]}"
            )
            topics = [t.strip("- ").strip() for t in resp.text.split("\n") if t.strip()]
            st.success(f"🎯 Topics: {', '.join(topics)}")

            yt = build("youtube", "v3", developerKey=gv_config.YT_API_KEY)
            video_links = []
            for topic in topics:
                res = yt.search().list(q=topic, part="snippet", type="video", maxResults=1).execute()
                items = res.get("items", [])
                if items:
                    video_links.append({
                        "url": f"https://youtu.be/{items[0]['id']['videoId']}",
                        "title": items[0]['snippet']['title']
                    })

            st.markdown("### 📺 Recommended YouTube Videos")
            if video_links:
                for vid in video_links:
                    st.video(vid["url"])
                    st.caption(vid["title"])
            else:
                st.warning("❗No videos found.")
        except Exception as e:
            st.error(f"🚨 Could not fetch video suggestions: {e}")

    # ✅ Kinesthetic Learner
    elif st.session_state.learning_style == "kinesthetic":
        st.markdown("### 👐 Kinesthetic Activity Suggestions")

        try:
            resp = ai_client.generate_content(
                f"Does this text describe a concept that has a PhET simulation? "
                f"Answer 'yes' or 'no', and list the best-matching PhET sim title:\n\n{content[:5000]}"
            )
            sim_answer = resp.text.strip().lower()
            if "yes" in sim_answer:
                sim_title = sim_answer.split(":")[-1].strip() if ":" in sim_answer else "Build an Atom"
                sim_iframe_url = "https://phet.colorado.edu/sims/html/build-an-atom/latest/build-an-atom_en-iframe.html"
                components.iframe(src=sim_iframe_url, height=400)
                st.markdown(f"**{sim_title}** — interact with this simulation to explore the concept!")
        except Exception as e:
            st.error("Couldn't load simulation suggestion.")
            resp = ai_client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=(
            "Explain the following content in a **kinesthetic-friendly** way:\n"
            "• Break it into 4–5 short steps\n"
            "• Use a vivid movement-based analogy\n"
            "• Include a simple gesture the learner can perform\n"
            "• Add a “Try it yourself!” prompt\n\n"
            "Use words like “Stand up and…”, “Pretend you are…”, or “Move your arms like…”.\n\n"
            "Here is the content:\n\n"
            f"{content[:5000]}"
        )
    )
    st.markdown("### 👐 Kinesthetic Explanation")
    st.write(resp.text)
    st.write("🔍 **Scavenger Hunt**: Find something nearby that relates to the idea.")
    photo = st.file_uploader("📸 Upload photo of your example:", type=["jpg", "png"])
    if photo:
            st.image(photo, caption="Your example in real life", use_column_width=True)
            st.info("Awesome! You’re engaging your body and brain together.")

    # ✅ Supabase Upload
    st.markdown("---")
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