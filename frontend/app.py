import streamlit as st
import requests

st.title("YouTube Summarizer")
url = st.text_input("Enter YouTube URL:")

if url:
    video_id = url.split("v=")[-1].split("&")[0]
    response = requests.post(
        "https://your-app.vercel.app/summarize",  # Replace with your Vercel backend URL
        json={"video_id": video_id}
    )
    
    if response.status_code == 200:
        st.write("Summary:", response.json()["summary"])
    else:
        st.error("Failed to generate summary.")