from playwright.sync_api import sync_playwright
from urllib.parse import quote

class TikTokLinkScraper:

    def __init__(self):
        pass

    def get_links(self, query):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            url = 'https://www.tiktok.com/search?q=' + quote(query)
            page.goto(url)

            page.wait_for_load_state("networkidle", timeout=10000)

            divs = page.query_selector_all('div[data-e2e="search_top-item"]')

            links = []

            for div in divs:
                anchor = div.query_selector("a[href]")   # find first <a> OR:
                # anchor = div.query_selector_all("a[href]")  # find all <a> inside

                if anchor:
                    href = anchor.get_attribute("href")
                    if href:
                        links.append(href)

            links = list(set(links))
            browser.close()
            return links
        
scraper = TikTokLinkScraper()
scraper.get_links("Singapore")
