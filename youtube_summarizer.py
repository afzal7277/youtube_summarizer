import os
import smtplib
import openai
import yt_dlp
from email.message import EmailMessage
from googleapiclient.discovery import build
from dotenv import load_dotenv
import logging


load_dotenv()

# Setup logging
logging.basicConfig(
    filename='youtube_summarizer.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO  # Change to DEBUG for more verbose output
)


# CONFIG
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # Target channel ID
LAST_VIDEO_FILE = "last_video_id.txt"
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

openai.api_key = OPENAI_API_KEY

def get_latest_video_id_and_title():
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    res = youtube.channels().list(part="contentDetails", id=CHANNEL_ID).execute()
    uploads_playlist = res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    
    videos = youtube.playlistItems().list(
        part="snippet",
        playlistId=uploads_playlist,
        maxResults=1
    ).execute()
    
    video_id = videos["items"][0]["snippet"]["resourceId"]["videoId"]
    video_title = videos["items"][0]["snippet"]["title"]
    return video_id, video_title



#using yt-dlp to download audio

def download_audio(video_id, video_title=None):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{video_title}.mp4',
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f'https://www.youtube.com/watch?v={video_id}'])
    return f"{video_title}.mp4"

# local whisper model works on linux and macOS
# Uncomment the following line if you want to use the local Whisper model
# def transcribe_audio(file_path):
#     model = whisper.load_model("base")
#     result = model.transcribe(file_path)
#     return result["text"]


#online whisper model works on all platforms

def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript['text']

def summarize_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Summarize the YouTube video transcript in bullet points with a short conclusion."},
            {"role": "user", "content": text}
        ]
    )
    return response["choices"][0]["message"]["content"]

def send_email(summary, current_video_title):
    msg = EmailMessage()
    msg.set_content(summary)
    msg["Subject"] = f"🧠 New YouTube Video Summary - {current_video_title}"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_FROM, EMAIL_PASSWORD)
        smtp.send_message(msg)

def load_last_video_id():
    if os.path.exists(LAST_VIDEO_FILE):
        with open(LAST_VIDEO_FILE, "r") as f:
            line = f.read().strip()
            if line:
                parts = line.split(",", 1)  # split only on first comma
                video_id = parts[0].strip()
                # video_title = parts[1].strip() if len(parts) > 1 else ""
                return video_id
    return None


def save_last_video_id(video_id, video_title):
    with open(LAST_VIDEO_FILE, "w") as f:
        f.write(f"{video_id},\t{video_title}")



def main():
    try:
        last_video_id = load_last_video_id()
        current_video_id, current_video_title = get_latest_video_id_and_title()
        
        if current_video_id == last_video_id:
            logging.info("No new video.")
            return

        logging.info(f"New video detected: {current_video_title} ({current_video_id})")
        audio_file = download_audio(current_video_id, current_video_title)
        logging.info("Audio downloaded.")
        
        transcript = transcribe_audio(audio_file)
        logging.info("Transcription complete.")
        
        summary = summarize_text(transcript)
        logging.info("Summary generated.")
        
        send_email(summary, current_video_title)
        logging.info("Summary sent via email.")
        
        save_last_video_id(current_video_id, current_video_title)
        logging.info("Video ID saved.")
        
        try:
            os.remove(audio_file)
            logging.info(f"Deleted audio file: {audio_file}")
        except OSError as e:
            logging.warning(f"Failed to delete audio file: {e}")


    except Exception as e:
        logging.error("An error occurred during execution", exc_info=True)



if __name__ == "__main__":
    main()
