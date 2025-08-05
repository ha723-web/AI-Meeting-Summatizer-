from transformers import pipeline
import re

# Load summarizer pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)

def preprocess_text(text):
    """
    Convert dialogue-like lines into paragraph-style narration for better summarization.
    E.g., 'Ethan: We did X' → 'Ethan said, We did X.'
    """
    lines = text.strip().split('\n')
    paragraphs = []
    for line in lines:
        if ':' in line:
            speaker, sentence = line.split(':', 1)
            paragraphs.append(f"{speaker.strip()} said, {sentence.strip()}")
        else:
            paragraphs.append(line.strip())
    return " ".join(paragraphs)

def extract_meeting_time(text):
    """
    Extracts meeting timing like 'Friday at 3 PM', 'Monday 11 AM', etc.
    """
    pattern = r'\b(?:reconvene|sync|meet(?:ing)?|call|review)[^.\n]{0,40}?(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s*(at)?\s*(\d{1,2})([:.]\d{2})?\s*(AM|PM)?'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        day = match.group(1).capitalize()
        hour = match.group(3)
        minute = match.group(4) if match.group(4) else ''
        ampm = match.group(5).upper() if match.group(5) else ''
        return f"\n\n📅 Next Meeting: {day} at {hour}{minute} {ampm}"
    return ""

def summarize_text(text, max_len=1200):
    if len(text.strip()) == 0:
        return "⚠️ No text provided."

    # Preprocess for better summarization
    cleaned_text = preprocess_text(text)

    # Generate summary
    summary = summarizer(cleaned_text, max_length=200, min_length=30, do_sample=False)[0]['summary_text']

    # Extract next meeting info
    meeting_info = extract_meeting_time(text)

    return summary + meeting_info
