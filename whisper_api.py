from openai import OpenAI
from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

OPENAI_API_KEY="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"
upload_folder = "uploads"

def split_audio(file_path, min_silence_len=500, silence_thresh=-40):
    """
    Splits audio into chunks based on silence.
    :param file_path: Path to the audio file.
    :param min_silence_len: Minimum length of silence to split on (in milliseconds).
    :param silence_thresh: Silence threshold (in dB).
    :return: List of audio chunks.
    """
    audio = AudioSegment.from_file(file_path)
    chunks = split_on_silence(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh
    )
    return chunks

def transcribe(filename):
    if (filename.endswith('.mp3') or filename.endswith('.wav') or filename.endswith('.mp4')):
        # Save the file to the uploads folder
        #file_path = os.path.join(upload_folder, filename)
        #file.save(file_path)
        file_path = filename
        # Initialize OpenAI client
        client = OpenAI(api_key=OPENAI_API_KEY)

        # Split audio into chunks if it's longer than 30 seconds
        audio_chunks = split_audio(file_path)

        # Transcribe each chunk
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
        print(f"Folder '{upload_folder}' created.")

        transcriptions = []
        for i, chunk in enumerate(audio_chunks):
            chunk_path = os.path.join(upload_folder, f"chunk_{i}.wav")
            chunk.export(chunk_path, format="wav")

            with open(chunk_path, 'rb') as audio_file:
                transcription_chunk = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            transcriptions.append(transcription_chunk.text)

            # Delete the chunk file after transcription
            os.remove(chunk_path)

        # Combine all transcriptions
        transcription = " ".join(transcriptions)

        # Delete the original file after transcription
        os.remove(file_path)

        return transcription
