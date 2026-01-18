import os
import whisper
from moviepy import VideoFileClip

def transcribe_video(filename: str) -> str:
    """
    Takes an mp4 filename, extracts audio, transcribes it using local Whisper,
    and returns the text string.
    """
    model = whisper.load_model("base") # Options: tiny, base, small, medium, large
    temp_audio = "temp_audio_extract.mp3"

    try:
        # 1. Extract Audio
        video = VideoFileClip(filename)
        video.audio.write_audiofile(temp_audio, logger=None)
        video.close()

        # 2. Transcribe
        result = model.transcribe(temp_audio)
        return result["text"].strip()

    except Exception as e:
        return f"Error: {e}"

    finally:
        # 3. Cleanup
        if os.path.exists(temp_audio):
            os.remove(temp_audio)

# Usage
if __name__ == "__main__":
    text = transcribe_video("tiktok_download.mp4")
    print(text)