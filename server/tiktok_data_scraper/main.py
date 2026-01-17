import asyncio
from datetime import datetime
import json
from tiktokDownloader import download_video_stealth
from tiktokData import get_data_by_url
from tiktokTranscribe import get_audio_and_transcribe
from videoTextExtractor import fast_extract_text


async def process_single_tiktok(url):
    print(f"\n{'='*20}\nSTARTING: {url}\n{'='*20}")

    # Create a unique base name for this session
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_filename = f"video_{timestamp}.mp4"
    json_filename = f"data_{timestamp}.json"

    # 1. Get Metadata
    print("\n[Step 1] Fetching Metadata...")
    metadata = await get_data_by_url(url)

    # 2. Download Video
    print("\n[Step 2] Downloading Video...")
    await download_video_stealth(url, output_name=video_filename)

    # 3. Transcribe Audio (Spoken Text)
    print("\n[Step 3] Transcribing Audio...")
    transcript = await get_audio_and_transcribe(url)

    # 4. Extract On-Screen Text (Visual Text)
    print("\n[Step 4] Extracting On-Screen Text...")
    on_screen_text = fast_extract_text(video_filename)

    # --- CONSOLIDATE DATA ---
    results = {
        "url": url,
        "processed_at": timestamp,
        "video_file": video_filename,
        "metadata": metadata,
        "audio_transcript": transcript,
        "on_screen_text": on_screen_text
    }

    # Save to JSON file
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"\n[Done] All data saved to: {json_filename}")
    return results


async def scrap_urls(url_list):
    for url in url_list:
        try:
            await process_single_tiktok(url)
        except Exception as e:
            print(f"[Error] Failed to process {url}: {e}")

if __name__ == "__main__":
    # You can add one or many URLs here
    urls = [
        # "https://www.tiktok.com/@human_edition/video/7569612755678891282",
        # "https://www.tiktok.com/@davidteathercodes/video/7074717081563942186"
        "https://www.tiktok.com/@cakes_n_ale/video/7563782866342038806",
    ]

    asyncio.run(scrap_urls(urls))
