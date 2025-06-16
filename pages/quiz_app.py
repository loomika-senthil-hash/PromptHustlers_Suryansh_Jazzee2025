import streamlit as st
from quiz_data import questions
from collections import Counter

def quiz_page():
    st.title("🧠 Learning Style Quiz")

    # Initialize response state if not already
    if "responses" not in st.session_state:
        st.session_state.responses = {}

    # Show all questions one by one
    for q in questions:
        st.subheader(f"Q{q['number']}. {q['question']}")
        option = st.radio(
            label="",
            options=list(q['options'].keys()),
            format_func=lambda x: q['options'][x][0],
            key=f"q{q['number']}"
        )
        st.session_state.responses[q['number']] = q['options'][option][1]

    # Submit button
    if st.button("✅ Submit Quiz"):
        # Ensure all questions are answered
        if len(st.session_state.responses) < len(questions):
            st.warning("⚠️ Please answer all questions before submitting.")
            return

        # Count the most common learning style
        styles = list(st.session_state.responses.values())
        most_common = Counter(styles).most_common(1)[0][0]

        # Save to session state
        st.session_state.learning_style = most_common
        st.session_state.quiz_done = True

        # Show result
        st.success(f"🎉 Your dominant learning style is: **{most_common.upper()}**")

        # Optional: clear responses after result is stored
        del st.session_state.responses
