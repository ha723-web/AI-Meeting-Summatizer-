# 🧠 AI Meeting Notes Summarizer

A clean and intuitive **Streamlit web app** that extracts **key summaries** and **action items** from meeting transcripts using advanced **NLP models**. Users can either paste a transcript or upload `.mp3` / `.wav` audio files to generate instant summaries.

---

## 🚀 Features

- ✍️ **Text Summarization** using `facebook/bart-large-cnn`
- 🎙️ **Audio Transcription** using OpenAI `whisper`
- ⚡ Fast, accurate results via Hugging Face Transformers
- 💻 Beautiful landing page design
- 📲 Built with Python + Streamlit

---

## 🧰 Tech Stack

| Category        | Tools / Libraries                        |
|-----------------|-------------------------------------------|
| Frontend        | Streamlit                                |
| NLP Model       | `facebook/bart-large-cnn` via `transformers` |
| Audio Transcribe| `whisper`                                 |
| Language        | Python 3.8+                               |

---

## 📁 Project Structure

meeting-notes-app/
├── app.py             # Streamlit app entry point
├── summarizer.py      # Handles BART-based text summarization
├── transcriber.py     # Handles Whisper-based audio transcription
├── requirements.txt   # Required Python packages
├── images/            # Background image and design assets
└── README.md          # Project documentation
---
## ▶️ How to Run the App Locally

### 1. Clone the repository

```bash
git clone https://github.com/ha723-web/AI-Meeting-Summarizer.git
cd AI-Meeting-Summarizer


python3 -m venv venv
source venv/bin/activate      # For Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install transformers
pip install git+https://github.com/openai/whisper.git
streamlit run app.py

