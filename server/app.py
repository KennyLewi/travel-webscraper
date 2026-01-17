from flask import Flask, request, jsonify
from flask_cors import CORS
from tiktok_link_scraper.tiktok_link_scraper import TikTokLinkScraper
from tiktok_data_scraper.tiktokScrapper import download_tiktok_video
from tiktok_data_scraper.transcribeAudio import transcribe_video

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
    query = f" {data['place']} {data['days']} days itinerary"

    scraper = TikTokLinkScraper()
    links = scraper.get_links(query)
    print(links)

    # desc = get_tiktok_data(links[0])
    result = download_tiktok_video(links[0])
    print(result)
    audio_transcript = transcribe_video(result['filename'])
    print(audio_transcript)

    # travel_json_lst = asyncio.run(scrap_urls(links))

    # parser = TravelTranscriptParser()

    # # for loop to merge description, audio transcript and OCR texts into one long string
    # all_desc = " ".join([d['metadata']['desc'] for d in travel_json_lst])
    # all_audio = " ".join([d['audio_transcript'] for d in travel_json_lst])
    # all_on_screen = " ".join([text for d in travel_json_lst for text in d['on_screen_text']])

    # plans = parser.get_locations(all_audio, all_desc, all_on_screen)
    # plans_as_dicts = [day.model_dump() for day in plans]
    # json_str = json.dumps(plans_as_dicts, indent=2)

    # goes through the list to get their string 
    # return json_str
    return jsonify({"places": ["Marina Bay Sands", "Art Science Museum", "National University of Singapore"]})

if __name__ == "__main__":
    print("server started")