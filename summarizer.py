
from transformers import pipeline
import re

# Your existing BART summarizer
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)

# ✅ Additional lightweight function (NEW)
def extract_meeting_time(text):
    """
    Extracts meeting scheduling info like 'regroup on Thursday' etc.
    Doesn't interfere with your original summarization logic.
    """
    pattern = r'\b(regroup|next meeting|sync|call|meet)[^\n]*\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)[^\n.]*'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return f"\n\n🗓️ {match.group(0).strip().capitalize()}."
    return ""

# ✅ Updated function with both summary + meeting extraction
def summarize_text(text, max_len=1200):
    if len(text.strip()) == 0:
        return "⚠️ No text provided."

    # Step 1: Original summary
    summary = summarizer(text, max_length=200, min_length=30, do_sample=False)[0]['summary_text']

    # Step 2: Extra meeting info
    meeting_info = extract_meeting_time(text)

    # Step 3: Combine — if found, append below summary
    return summary + meeting_info
