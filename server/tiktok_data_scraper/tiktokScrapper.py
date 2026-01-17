from datetime import datetime
import json
from playwright.sync_api import sync_playwright

def download_tiktok_video(video_url):
    result = {}

    with sync_playwright() as p:
        print("[*] Launching browser...")
        browser = p.chromium.launch(headless=True)
        
        # 1. Correct way to set headers in Playwright
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            extra_http_headers={
                'Referer': 'https://www.tiktok.com/'
            }
        )
        page = context.new_page()

        print(f"[*] Navigating to {video_url}...")
        page.goto(video_url)

        try:
            # 2. Wait for data script
            selector = 'script[id="__UNIVERSAL_DATA_FOR_REHYDRATION__"]'
            page.wait_for_selector(selector, state="attached", timeout=10000)
            
            # 3. Extract JSON
            script_content = page.locator(selector).first.inner_text()
            data = json.loads(script_content)
            
            # 4. Parse JSON
            default_scope = data.get("__DEFAULT_SCOPE__", {})
            video_detail = default_scope.get("webapp.video-detail", {})
            item_info = video_detail.get("itemInfo", {}).get("itemStruct", {})
            
            video_obj = item_info.get("video", {})
            real_video_url = video_obj.get("playAddr")
            desc = item_info.get("desc")
            
            print(f"[+] Description: {desc}")

            result["desc"] = desc

            if real_video_url:
                print(f"[*] Found Real URL: {real_video_url[:50]}...")
                
                # 5. Download the video
                # We reinforce the headers here just to be safe
                response = page.request.get(
                    real_video_url,
                    headers={
                        "Referer": "https://www.tiktok.com/",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
                    }
                )
                
                if response.status == 200:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"video_{timestamp}.mp4"
                    with open(filename, "wb") as f:
                        f.write(response.body())
                    print(f"[+] Video saved as: {filename}")
                    result["filename"] = filename
                else:
                    print(f"[-] Download failed. Status: {response.status}")
                    
            else:
                print("[-] Could not find 'playAddr' in JSON data.")

        except Exception as e:
            print(f"[-] Error: {e}")
            
        finally:
            browser.close()
            return result

# Usage
if __name__ == "__main__":
    url = "https://www.tiktok.com/@jsmn_cooking/video/7589546219668557077"
    download_tiktok_video(url)