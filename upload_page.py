import streamlit as st
import pdfplumber, docx, pptx, tempfile
from supabase_config import supabase
from google import genai
import gv_config
import streamlit.components.v1 as components
from googleapiclient.discovery import build
from translations import translations  # 🌐 Import translations

# 🌐 Set translation dict
t = translations.get(st.session_state.get("language", "English"))

# ✅ Initialize AI client
ai_client = genai.Client(api_key=gv_config.GEMINI_API_KEY)

def show_upload_page():
    st.title("📤 " + t["upload_material"])
    st.success(f"🔊 {t['mode']}: {st.session_state.learning_style.upper()}")

    uploaded_file = st.file_uploader(t["upload_prompt"], type=["pdf", "pptx", "docx"])
    if not uploaded_file:
        st.info(t["upload_hint"])
        return

    # Save to temporary file
    ext = uploaded_file.name.rsplit(".", 1)[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    # Extract text from file
    if ext == "pdf":
        content = "\n".join(p.extract_text() or "" for p in pdfplumber.open(tmp_path).pages)
    elif ext == "docx":
        content = "\n".join(para.text for para in docx.Document(tmp_path).paragraphs)
    elif ext == "pptx":
        prs = pptx.Presentation(tmp_path)
        content = "\n".join(shape.text for s in prs.slides for shape in s.shapes if hasattr(shape, "text"))
    else:
        st.error(t["unsupported_file"])
        return

    # Display extracted content
    st.subheader("🧠 " + t["extracted_content"])
    st.text_area(t["preview_label"], content[:1000], height=300)

    # Save content for modes
    st.session_state.content = content
    components.html(
        """
        <div class="bg-white p-6 rounded-lg shadow-lg">
          <h2 class="text-xl font-bold">Feature One</h2>
          <p>This helps learners visualize concepts.</p>
        </div>
        """,
        width=400,
        height=200
    )

    # === Reader/Writer Mode ===
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
        cols[0].button(t["summary_btn"], key="summary_btn", on_click=build_on_click("summary"))
        cols[1].button(t["story_btn"], key="story_btn", on_click=build_on_click("story"))
        cols[2].button(t["explain_btn"], key="explain_btn", on_click=build_on_click("explain"))

        if st.session_state.summary:
            resp = ai_client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=f"{t['summary_prompt']}\n\n{content[:5000]}"
            )
            st.markdown("### " + t["summary_title"])
            st.write(resp.text)

        elif st.session_state.story:
            resp = ai_client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=f"{t['story_prompt']}\n\n{content[:5000]}"
            )
            st.markdown("### " + t["story_title"])
            st.write(resp.text)

        elif st.session_state.explain:
            resp = ai_client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=f"{t['explain_prompt']}\n\n{content[:5000]}"
            )
            st.markdown("### " + t["explain_title"])
            st.write(resp.text)

    # === Auditory Mode ===
    elif st.session_state.learning_style == "auditory":
        st.markdown("---")
        st.markdown("### 🗣️ " + t["auditory_heading"])
        components.html(
            f"""
            <iframe src="https://loomika-senthil-hash.github.io/PromptHustlers_Suryansh_Jazzee2025/"
                    width="1200" height="200"
                    allow="microphone; autoplay"
                    style="border:none;">
            </iframe>
            """,
            height=700
        )

    # === Visual Mode ===
    elif st.session_state.learning_style == "visual":
        st.markdown("---")
        st.markdown("🔍 " + t["extracting_topics"])

        try:
            resp = ai_client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=f"{t['topic_prompt']}\n\n{content[:5000]}"
            )
            topics = [t.strip("- ").strip() for t in resp.text.split("\n") if t.strip()]
            st.success(f"🎯 {t['topics_found']}: {', '.join(topics)}")

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

            st.markdown("### 📺 " + t["yt_recommendations"])
            if video_links:
                for vid in video_links:
                    st.video(vid["url"])
                    st.caption(vid["title"])
            else:
                st.warning(t["no_videos"])
        except Exception as e:
            st.error(f"🚨 {t['video_fetch_error']}: {e}")

    # === Kinesthetic Mode ===
    elif st.session_state.learning_style == "kinesthetic":
        st.markdown("### 👐 " + t["kinaesthetic_heading"])
        try:
            resp = ai_client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=(
                    f"{t['kinaesthetic_prompt']}\n\n{content[:5000]}"
                )
            )
            st.write(resp.text)
        except Exception as e:
            st.error(f"❌ {t['kinaesthetic_error']}: {e}")

    # === Supabase Upload ===
    st.markdown("---")
    if st.button("📤 " + t["upload_button"]):
        fname = f"uploads/{uploaded_file.name}"
        try:
            supabase.storage.from_("uploads").upload(
                fname,
                open(tmp_path, "rb"),
                file_options={"upsert": False}
            )
            st.success("✅ " + t["upload_success"])
            st.info(f"{t['upload_path']}: {fname}")
        except Exception as e:
            st.error(f"❌ {t['upload_fail']}: {e}")
