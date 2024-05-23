import streamlit as st
from dotenv import load_dotenv,find_dotenv
import os
import google.generativeai as genai

status=load_dotenv(find_dotenv(),override=True)
st.success(status)
from youtube_transcript_api import YouTubeTranscriptApi as y
mkey=os.environ.get('GOOGLE_API_KEY')
# st.success(mkey)
genai.configure(api_key=mkey)

prompt='''You are a YouTube video summerizer. You will be taking the transcript
        text and summerizing the entire video and providing the important summary
        in points within 250 words. Please provide the summary of the text given 
        here.'''

# Getting the transcripted data from youtube-video

def extract_youtube(url):
    try:
        video_id=url.split("=")[1]
        transcripted_text=y.get_transcript(video_id)
        tr=""
        for i in transcripted_text:
            tr+=""+i["text"]
        return tr
    except Exception as e:
        st.error(e)

def generate_summary(tr,prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+tr)
    return response.text
st.title('YouTube Transcript')
url=st.text_input('Enter the YouTube Url')
if url:
    vd=url.split("=")[1]
    print(vd)
    st.image(f"http://img.youtube.com/vi/{vd}/0.jpg",use_column_width=True)

if st.button('Get Details'):
    tr=extract_youtube(url)
    if tr:
        summary=generate_summary(tr,prompt)
        st.markdown('## Detailed Notes:')
        st.write(summary)
     



