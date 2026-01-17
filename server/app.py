from flask import Flask, request, jsonify
from flask_cors import CORS
from tiktok_link_scraper.tiktok_link_scraper import TikTokLinkScraper
from tiktok_data_scraper.main import scrap_urls
import asyncio
from parsers.travel_transcript_parser import TravelTranscriptParser

app = Flask(__name__)
CORS(app)

@app.route("/api/generate-itinerary", methods=["POST"])
def generate_itinerary():
    #TODO
    """
    Generate a day-by-day travel itinerary with Google Maps routes.
    
    Expected Request JSON:
    {
        "place": "Singapore",
        "days": 2,
    }

    Example JSON Response:
    {
        "place": "Singapore",
        "days": [
            {
                "day": 1,
                "locations": ["174 Bingo", "Marina Barrage"],
                "route_link": "https://www.google.com/maps/dir/174+Bingo/Marina+Barrage/"
            },
            ...
        ]
    }
    """
    data = request.json
    print(data)
    query = data.place + f"{data.place} {data.days} itinerary"

    scraper = TikTokLinkScraper()
    links = scraper.get_links(query)
    travel_json_lst = asyncio.run(scrap_urls(links))

    parser = TravelTranscriptParser()

    # for loop to merge description, audio transcript and OCR texts into one long string
    all_desc = " ".join([d['metadata']['desc'] for d in travel_json_lst])
    all_audio = " ".join([d['audio_transcript'] for d in travel_json_lst])
    all_on_screen = " ".join([text for d in travel_json_lst for text in d['on_screen_text']])
        

    locations = parser.get_locations(all_audio, all_on_screen)

    # goes through the list to get their string 
    return jsonify({"places": locations})
    # return jsonify({"places": ["Marina Bay Sands", "Art Science Museum", "National University of Singapore"]})