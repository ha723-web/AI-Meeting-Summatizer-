from transformers import pipeline

# Force CPU usage
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=-1)

def summarize_text(text, max_len=1200):
    if len(text) == 0:
        return "No text provided."
    summary = summarizer(text, max_length=200, min_length=30, do_sample=False)
    return summary[0]['summary_text']
