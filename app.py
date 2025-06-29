import os
import whisper
from flask import Flask, render_template, request, redirect, url_for
from transformers import pipeline
from googletrans import Translator
import pyttsx3
import textwrap

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set maximum upload size (e.g., 500MB)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

# Force PyTorch for Transformers
os.environ["TRANSFORMERS_NO_TF"] = "1"
summarizer = pipeline("summarization", model="facebook/bart-large-cnn", framework="pt")


def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result['text']


def summarize_transcript(transcript):
    chunks = textwrap.wrap(transcript, width=1000)
    summaries = []
    for chunk in chunks:
        try:
            summary = summarizer(chunk, max_length=150, min_length=40, do_sample=False)[0]['summary_text']
            summaries.append(summary)
        except Exception as e:
            print(f"Summarization error: {e}")

    full_summary = ' '.join(summaries)

    action_items, decisions = [], []
    for line in transcript.split('\n'):
        line = line.strip().lower()
        if any(phrase in line for phrase in ['will', 'should', 'need to']):
            action_items.append(line)
        if any(phrase in line for phrase in ['decided', 'agreed', 'approved']):
            decisions.append(line)

    return {
        "summary": full_summary,
        "action_items": action_items[:5],
        "decisions": decisions[:5]
    }


def translate_text(text, target_language="hi"):
    try:
        translator = Translator()
        translated = translator.translate(text, src='en', dest=target_language)
        return translated.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text


def synthesize_speech(text, output_path="static/summary.mp3"):
    engine = pyttsx3.init()
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    engine.stop()
    return output_path


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['audio_file']
        if file and file.filename.endswith('.mp3'):
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            transcript = transcribe_audio(filepath)
            result = summarize_transcript(transcript)
            translated = translate_text(result['summary'], target_language="hi")
            mp3_path = synthesize_speech(result['summary'])

            return render_template('result.html',
                                   transcript=transcript,
                                   result=result,
                                   translated=translated,
                                   mp3_path=mp3_path)
        else:
            return "Only .mp3 files are allowed.", 400wh

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
