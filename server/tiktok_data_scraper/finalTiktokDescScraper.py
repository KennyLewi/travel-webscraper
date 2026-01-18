from playwright.sync_api import sync_playwright

def get_tiktok_data(video_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # Use a standard user agent to avoid bot detection
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        )
        page = context.new_page()

        print(f"[*] Navigating to {video_url}...")
        page.goto(video_url)

        try:
            # 1. Wait for at least one description to appear
            # We use first() here to check visibility of the main one
            page.locator('div[data-e2e="video-desc"]').first.wait_for(timeout=10000)
            
            # 2. Extract text from the FIRST match
            # This ignores the duplicate elements found in the "Related Videos" feed
            desc = page.locator('div[data-e2e="video-desc"]').first.inner_text()
            
            print(f"[+] Description: {desc}")
            return desc
            
        except Exception as e:
            print(f"[-] Error: {e}")
            return None
        finally:
            browser.close()

if __name__ == "__main__":
    url = "https://www.tiktok.com/@jsmn_cooking/video/7589546219668557077"
    get_tiktok_data(url)