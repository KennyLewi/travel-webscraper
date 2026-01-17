from TikTokApi import TikTokApi
import asyncio
import os
import json

ms_token = os.environ.get("ms_token", None)


async def get_data_by_url(video_url):
    async with TikTokApi() as api:
        # Step 1: Create Session
        await api.create_sessions(
            ms_tokens=[ms_token],
            num_sessions=1,
            sleep_after=3,
            browser=os.getenv("TIKTOK_BROWSER", "chromium"),
            headless=False  # Set to True once you confirm it works
        )

        # Step 2: Create a video object from the URL
        video = api.video(url=video_url)

        # Step 3: Fetch the full metadata (info)
        # This returns the dictionary found in 'as_dict' or raw from TikTok
        video_info = await video.info()

        # Print specific data points
        print(f"Author: {video_info.get('author', {}).get('nickname')}")
        print(f"Description: {video_info.get('desc')}")
        print(f"View Count: {video_info.get('stats', {}).get('playCount')}")

        # Optional: Save to JSON
        with open("single_video_data.json", "w", encoding="utf-8") as f:
            json.dump(video_info, f, indent=4, ensure_ascii=False)

        return video_info

if __name__ == "__main__":
    url = "https://www.tiktok.com/@davidteathercodes/video/7074717081563942186"
    asyncio.run(get_data_by_url(url))
