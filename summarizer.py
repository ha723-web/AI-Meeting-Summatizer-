from transformers import pipeline
import re

# Force CPU usage
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)

def extract_meeting_datetime(text):
    """
    Looks for lines indicating next meetings with day/time info.
    E.g., 'Let's meet on Thursday at 2 PM'
    """
    pattern = r"(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s*(at\s*\d{1,2}\s*(AM|PM))?"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return f"\n\n📅 Next Meeting: {match.group(0).strip().capitalize()}"
    return ""

def summarize_text(text, max_len=1200):
    if len(text) == 0:
        return "No text provided."
    
    summary = summarizer(text, max_length=200, min_length=30, do_sample=False)[0]['summary_text']
    meeting_info = extract_meeting_datetime(text)
    
    return summary + meeting_info
