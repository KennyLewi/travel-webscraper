import asyncio
import os
import random
import httpx
from TikTokApi import TikTokApi

ms_token = os.environ.get("ms_token", None)


def find_video_url(data):
    """Recursively searches for the actual video file link (.mp4)."""
    if isinstance(data, dict):
        # TikTok's main video keys
        for key in ['download_addr', 'play_addr', 'play_url']:
            if key in data:
                val = data[key]
                # If it's a dict with a list of URLs (standard TikTok format)
                if isinstance(val, dict) and 'url_list' in val and val['url_list']:
                    return val['url_list'][0]
                # If it's just a direct string URL
                if isinstance(val, str) and val.startswith('http'):
                    return val
        # Dive deeper
        for v in data.values():
            result = find_video_url(v)
            if result:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_video_url(item)
            if result:
                return result
    return None


async def download_video_stealth(url, output_name="my_tiktok_video.mp4"):
    async with TikTokApi() as api:
        await api.create_sessions(
            ms_tokens=[ms_token],
            num_sessions=1,
            sleep_after=random.randint(2, 5),
            headless=False
        )

        print(f"[*] Extracting metadata for: {url}")
        video = api.video(url=url)

        try:
            video_info = await video.info()
            video_url = find_video_url(video_info)
        except Exception as e:
            print(f"[!] Metadata extraction failed: {e}")
            video_url = None

        video_bytes = None

        if video_url and video_url.startswith('http'):
            print(f"[*] Found direct .mp4 link. Downloading via HTTPX...")
            async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Referer": "https://www.tiktok.com/"
                }
                response = await client.get(video_url, headers=headers)
                if response.status_code == 200:
                    video_bytes = response.content
        print(video_bytes)
        # FALLBACK: If HTTPX failed or no URL was found, use the API's internal downloader
        if not video_bytes:
            print("[*] Attempting internal API download fallback...")
            try:
                video_bytes = await video.bytes()
            except Exception as e:
                print(f"[Error] Internal download failed: {e}")
                return  # Exit if both methods fail

        # Save the file
        if video_bytes:
            with open(output_name, "wb") as f:
                f.write(video_bytes)
            print(f"[+] DONE! Video saved as: {os.path.abspath(output_name)}")
        else:
            print("[Error] No video data captured.")

if __name__ == "__main__":
    url = "https://www.tiktok.com/@human_edition/video/7569612755678891282"
    asyncio.run(download_video_stealth(url))
