from transformers import pipeline
import json

# Load a summarization pipeline using a small, local model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def process_with_granite(transcript):
    try:
        # Step 1: Generate the summary
        summary = summarizer(transcript, max_length=150, min_length=40, do_sample=False)[0]["summary_text"]

        # Step 2: Simulate Action Items & Decisions using basic keyword parsing (or extend with LLM if needed)
        action_items = []
        decisions = []

        for line in transcript.split('\n'):
            line = line.strip().lower()
            if "will" in line or "need to" in line or "should" in line:
                action_items.append(line)
            if "decided" in line or "agreed" in line or "approved" in line:
                decisions.append(line)

        # Step 3: Format response
        return {
            "summary": summary,
            "action_items": action_items[:5],
            "decisions": decisions[:5]
        }

    except Exception as e:
        return {
            "summary": "Error processing transcript",
            "action_items": [],
            "decisions": [],
            "error": str(e)
        }
