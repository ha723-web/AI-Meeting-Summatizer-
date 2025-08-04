
from transformers import pipeline
import re

# Your existing BART summarizer
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)

#lightweight function (NEW)
def extract_meeting_time(text):
    """
    Finds phrases like 'next sync will be on Wednesday at 2 PM'
    """
    pattern = r'\b(regroup|next (sync|meeting|call)|meeting)[^\n.]*?(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)(.*?)\b(\d{1,2} ?[apAP][mM])?'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return f"\n\n🗓️ {match.group(0).strip().capitalize()}."
    return ""


#function with both summary + meeting extraction
def summarize_text(text, max_len=1200):
    if len(text.strip()) == 0:
        return "⚠️ No text provided."

    # Step 1: Original summary
    summary = summarizer(text, max_length=200, min_length=30, do_sample=False)[0]['summary_text']

    # Step 2: Extra meeting info
    meeting_info = extract_meeting_time(text)

    # Step 3: Combine — if found, append below summary
    return summary + meeting_info
