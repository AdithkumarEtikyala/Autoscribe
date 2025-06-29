from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai import Credentials
import json

def process_with_granite(api_key, project_id, url, transcript):
    credentials = Credentials(api_key, url)

    model = Model(
        model_id="granite-13b-chat",
        params={"decoding_method": "greedy", "max_new_tokens": 500},
        project_id=project_id,
        credentials=credentials
    )

    prompt = f"""
You are an AI meeting assistant.

Given the transcript below, summarize the meeting, extract key action items and decisions made.

Return output strictly in JSON format as:
{{
  "summary": "...",
  "action_items": ["..."],
  "decisions": ["..."]
}}

Transcript:
\"\"\"
{transcript}
\"\"\"
"""

    response = model.generate(prompt=prompt)

    try:
        return json.loads(response)
    except Exception as e:
        return {"summary": "Error parsing Granite output", "action_items": [], "decisions": [], "error": str(e)}
