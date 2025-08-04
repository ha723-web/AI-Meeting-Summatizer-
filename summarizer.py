from transformers import pipeline
import re

# BART Summarizer as-is
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)

# Extracts 'next sync on Thursday at 2 PM' etc.
def extract_meeting_time(text):
    pattern = r'\b(?:regroup|next (?:sync|meeting|call)).*?(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)(?:.*?(\d{1,2}\s?(?:AM|PM)))?'
    match = re.search(pattern, text, re.IGNORECASE)
    
    if match:
        day = match.group(1)
        time = match.group(2)
        if time:
            return f"\n📅 Next Meeting: {day} at {time}"
        else:
            return f"\n📅 Next Meeting: {day}"
    return ""

# Combine original BART summary with optional meeting info
def summarize_text(text, max_len=1200):
    if len(text.strip()) == 0:
        return "⚠️ No text provided."

    summary = summarizer(text, max_length=200, min_length=30, do_sample=False)[0]['summary_text']
    meeting_info = extract_meeting_time(text)
    return summary + meeting_info
