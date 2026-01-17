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
        # HUMAN STRATEGY: Randomize behavior
        await api.create_sessions(
            ms_tokens=[ms_token],
            num_sessions=1,
            sleep_after=random.randint(2, 5),
            headless=False
        )

        print(f"[*] Extracting metadata for: {url}")
        video = api.video(url=url)
        video_info = await video.info()

        # Find the .mp4 link
        video_url = find_video_url(video_info)

        if not video_url:
            print("[!] Video link not found in metadata. Attempting fallback...")
            video_bytes = await video.bytes()  # Last resort
        else:
            print(f"[*] Found direct .mp4 link. Downloading...")
            # STEALTH STRATEGY: Download via HTTPX with browser headers
            async with httpx.AsyncClient(follow_redirects=True) as client:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Referer": "https://www.tiktok.com/"
                }
                response = await client.get(video_url, headers=headers)
                video_bytes = response.content

        # Save as a real video file
        with open(output_name, "wb") as f:
            f.write(video_bytes)

        print(f"[+] DONE! Video saved as: {os.path.abspath(output_name)}")

if __name__ == "__main__":
    url = "https://www.tiktok.com/@human_edition/video/7569612755678891282"
    asyncio.run(download_video_stealth(url))
