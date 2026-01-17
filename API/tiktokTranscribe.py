import asyncio
import io
import os
import httpx
import whisper
import tempfile
from TikTokApi import TikTokApi

# Initialize Whisper once
model = whisper.load_model("base")


def find_audio_url(data):
    """Recursively searches the dictionary for any key containing a play URL."""
    if isinstance(data, dict):
        # Look for common TikTok audio keys
        for key in ['play_url', 'playUrl', 'play_addr', 'link']:
            if key in data and isinstance(data[key], str) and data[key].startswith('http'):
                return data[key]
            # Some versions nest the URL inside a list: play_url: [{url_list: [...]}]
            if key in data and isinstance(data[key], list) and len(data[key]) > 0:
                return data[key][0]
        # Recursively search deeper
        for v in data.values():
            result = find_audio_url(v)
            if result:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_audio_url(item)
            if result:
                return result
    return None


async def get_audio_and_transcribe(url):
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[os.environ.get("ms_token")], num_sessions=1, headless=False)

        print("Fetching video metadata...")
        video = api.video(url=url)
        video_info = await video.info()

        # Search for the audio URL in the entire metadata object
        audio_url = find_audio_url(video_info)

        if not audio_url:
            print("Failed to extract audio URL from metadata.")
            return

        print(f"Downloading audio stream...")
        async with httpx.AsyncClient(follow_redirects=True) as client:
            # We add a User-Agent to prevent TikTok from blocking the direct audio download
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
            response = await client.get(audio_url, headers=headers)

        if response.status_code != 200:
            print(f"Download failed (Status {response.status_code}).")
            return

        # Process in memory via a temporary file
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            tmp.write(response.content)
            tmp_path = tmp.name

        try:
            print("Transcribing (CPU)...")
            result = model.transcribe(tmp_path, fp16=False)
            print("\n--- TRANSCRIPT ---")
            print(result['text'])
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

if __name__ == "__main__":
    tiktok_url = "https://www.tiktok.com/@davidteathercodes/video/7074717081563942186"
    asyncio.run(get_audio_and_transcribe(tiktok_url))
