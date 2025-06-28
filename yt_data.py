import os
import json
import yt_dlp
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from whisper_api import transcribe

# Replace with your YouTube API Key
API_KEY = "gmail key"
YOUTUBE = build("youtube", "v3", developerKey=API_KEY)


def get_video_details(video_id):
    """Fetch video details using YouTube API"""
    request = YOUTUBE.videos().list(
        part="snippet,contentDetails",
        id=video_id
    )
    response = request.execute()
    
    if "items" in response and response["items"]:
        video_info = response["items"][0]
        return {
            "title": video_info["snippet"]["title"],
            "description": video_info["snippet"]["description"],
            "duration": video_info["contentDetails"]["duration"],
        }
    return None


def download_audio(video_url, audio_format="mp4"):
    """Download audio from a YouTube video"""
    ydl_opts = {
        "format": f"bestaudio[ext={audio_format}]",
        "outtmpl": f"audio.{audio_format}",
        "nopart": True,  # Disable creation of the .part file.
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    return f"audio.{audio_format}"



def get_transcription(video_id):
    """Fetch video transcription if available"""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return "\n".join([entry["text"] for entry in transcript])
    except TranscriptsDisabled:
        return "Transcripts not available for this video."
    except Exception as e:
        return f"Error: {str(e)}"


def get_video_transcript(video_url):
    print("URL: ", video_url)
    video_id = video_url.split("v=")[-1].split("&")[0]

    details = get_video_details(video_id)
    if details:
        print(json.dumps(details, indent=4))
    else:
        print("Failed to retrieve video details.")

    audio_file = download_audio(video_url, "mp4")
    transcription = get_transcription(video_id)
    #print("\nTranscription:\n", transcription)
    
    # transcription = "Error: rfev4gv"
    if transcription=="Transcripts not available for this video." or transcription[0:6]=="Error:":
        print("Transcription not available for this video.")
        transcription = transcribe(audio_file)
        #print("\nTranscription:\n", transcription)
    return transcription
