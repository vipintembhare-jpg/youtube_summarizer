from flask import Flask, request, jsonify, Response
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
    
    # Summarize in chunks
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    chunk_size = 1000  # Adjust as needed
    chunks = [transcript_text[i:i + chunk_size] for i in range(0, len(transcript_text), chunk_size)]
    summaries = []
    
    for chunk in chunks:
        summary = summarizer(chunk, max_length=150)[0]['summary_text']
        summaries.append(summary)
    
    # Stream the response in chunks
    def generate():
        for summary in summaries:
            yield json.dumps({"summary": summary}) + "\n"
    
    return Response(generate(), mimetype="application/json")

if __name__ == "__main__":
    app.run()