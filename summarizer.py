from transformers import pipeline
import re

# Force CPU usage
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)

def extract_meeting_time(text):
    """
    Finds phrases like:
    - 'next sync is on Friday at 3 PM'
    - 'meeting scheduled for Thursday at 2pm'
    - 'let’s reconvene on Monday 11 AM'
    """
    pattern = r'\b(?:reconvene|sync|meet(?:ing)?|call|review)[^.\n]{0,40}?(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s*(at)?\s*(\d{1,2})([:.]\d{2})?\s*(AM|PM)?'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        day = match.group(1).capitalize()
        hour = match.group(3)
        minute = match.group(4) if match.group(4) else ''
        ampm = match.group(5).upper() if match.group(5) else ''
        return f"\n\n📅 Next Meeting: {day} at {hour}{minute} {ampm}".strip()
    return ""

def preprocess_text(text):
    """
    Convert chat-style lines into paragraph form for better summarization.
    E.g., 'Jason: Hello' -> 'Jason said, Hello.'
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

def summarize_text(text, max_len=1200):
    if len(text.strip()) == 0:
        return "⚠️ No text provided."

    # Step 0: Reshape transcript
    processed_text = preprocess_text(text)

    # Step 1: Main summary
    summary = summarizer(processed_text, max_length=200, min_length=30, do_sample=False)[0]['summary_text']

    # Step 2: Extract time info
    meeting_info = extract_meeting_time(text)

    return summary + meeting_info
