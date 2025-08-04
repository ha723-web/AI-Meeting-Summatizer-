import base64
import streamlit as st
from summarizer import summarize_text
from transcriber import transcribe_audio
import tempfile
import spacy
import os

import spacy
nlp = spacy.load("en_core_web_sm")



# Set full-width layout
st.set_page_config(layout="wide", page_title="AI Meeting Summarizer")

def set_hero_background(image_path):
    with open(image_path, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()

    return f"""
    <style>
    html, body {{
        height: 100%;
        width: 100%;
        margin: 0;
        padding: 0;
        overflow-x: hidden;
    }}

    .stApp {{
        padding: 0 !important;
        margin: 0 !important;
        overflow-x: hidden;
    }}

    .main .block-container {{
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
        width: 100% !important;
    }}

    .hero {{
        height: 100vh;
        width: 100%;
        background: url("data:image/jpg;base64,{encoded}") no-repeat center center;
        background-size: cover;
        display: flex;
        justify-content: center;
        align-items: center;
    }}

    .hero-content {{
        background: white;
        padding: 3rem 4rem;
        border-radius: 24px;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.2);
        max-width: 900px;
        width: 90%;
        text-align: center;
    }}

    .hero h1 {{
        font-size: 3.2rem;
        font-weight: 800;
        margin-bottom: 1rem;
        color: #111;
    }}

    .hero p {{
        font-size: 1.3rem;
        color: #333;
        margin-bottom: 2rem;
    }}

    .try-now a {{
        background-color: #ff4b4b;
        padding: 14px 34px;
        color: white;
        font-weight: bold;
        font-size: 18px;
        text-decoration: none;
        border-radius: 10px;
        transition: 0.3s ease;
    }}

    .try-now a:hover {{
        background-color: #e03c3c;
    }}

    .below-hero {{
        background-color: #fff5f9;
        padding: 3rem 2rem;
        border-radius: 16px;
        max-width: 950px;
        margin: 0 auto;
    }}
    </style>
    """


# Inject custom CSS
st.markdown(set_hero_background("images/1.jpg"), unsafe_allow_html=True)

# Hero Section HTML
st.markdown("""
<div class="hero">
    <div class="hero-content">
        <h1>🧠 Your Smart AI Assistant for Meetings</h1>
        <p>Extract action points and summaries from long transcripts in seconds.</p>
        <div class="try-now">
            <a href="#start-section">Try Now</a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Start Section
st.markdown('<div id="start-section" class="below-hero">', unsafe_allow_html=True)

# Text Input
st.markdown("### 📝 Paste Your Transcript")
text_input = st.text_area("", height=200)

if st.button("Summarize Now"):
    if text_input.strip():
        with st.spinner("Working on it..."):
            summary = summarize_text(text_input)
        st.success("✅ Summary")
        st.markdown(f"> {summary}")
    else:
        st.warning("⚠️ Please paste something to summarize.")

# Audio Upload
st.markdown("### 🎙️ Or Upload a Meeting Audio File")
st.caption("Upload (.mp3 or .wav)")

audio_file = st.file_uploader("Drag and drop file here", type=["mp3", "wav"])

if audio_file:
    st.audio(audio_file, format='audio/mp3')
    if st.button("Transcribe & Summarize Audio"):
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_path = tmp_file.name
        with st.spinner("Transcribing..."):
            transcript = transcribe_audio(tmp_path)
            summary = summarize_text(transcript)
        st.success("✅ Summary from Audio")
        st.markdown(f"> {summary}")

# End section
st.markdown('</div>', unsafe_allow_html=True)
