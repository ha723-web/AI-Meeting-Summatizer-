from transformers import pipeline
import re

# Load the summarizer
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)

def preprocess_to_narrative(text):
    lines = text.strip().split('\n')
    result = []
    for line in lines:
        if ':' in line:
            speaker, message = line.split(':', 1)
            result.append(f"{speaker.strip()} said {message.strip()}.")
        else:
            result.append(line.strip())
    return " ".join(result)

def extract_meeting_time(text):
    pattern = r'\b(?:reconvene|sync|meet(?:ing)?|call|review|check-in)[^.\n]{0,50}?(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s*(at)?\s*(\d{1,2})([:.]\d{2})?\s*(AM|PM)?'
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

    # 1. Preprocess into narrative form
    narrative_text = preprocess_to_narrative(text)

    # 2. Summarize using BART with better max length
    summary = summarizer(narrative_text, max_length=130, min_length=40, do_sample=False)[0]['summary_text']

    # 3. Extract meeting time
    meeting_info = extract_meeting_time(text)

    return summary.strip() + meeting_info

