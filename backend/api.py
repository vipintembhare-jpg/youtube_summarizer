from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

app = Flask(__name__)

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.json
    video_id = data["video_id"]
    
    # Get transcript
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([t['text'] for t in transcript])
    except:
        return jsonify({"error": "Transcript not available"}), 400
    
    # Summarize
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    summary = summarizer(transcript_text, max_length=150)[0]['summary_text']
    
    return jsonify({"summary": summary})

@app.route("/", methods=["GET"])
def welcome():
    print("Welcome Vipin")
    return "Welcome Vipin!"

if __name__ == "__main__":
    app.run()