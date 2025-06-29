from transformers import pipeline

# Load a summarization pipeline (this uses a small model for example purposes)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(transcript):
    print("🧠 Summarizing transcript locally...")
    summary_text = summarizer(transcript, max_length=150, min_length=40, do_sample=False)[0]['summary_text']

    # Simulate action items and decisions for demo
    action_items = "- [ ] Follow up with marketing team\n- [ ] Finalize project plan"
    decisions = "- Launch postponed to Q3\n- Adopt hybrid working model"

    return {
        "summary": summary_text,
        "action_items": action_items,
        "decisions": decisions
    }
