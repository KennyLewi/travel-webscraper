from flask import Flask, request, jsonify
from flask_cors import CORS
from tiktok_link_scraper.tiktok_link_scraper import TikTokLinkScraper
from tiktok_data_scraper.tiktokScrapper import download_tiktok_video
from tiktok_data_scraper.transcribeAudio import transcribe_video
from tiktok_data_scraper.videoTextExtractor import fast_extract_text
from parsers.travel_transcript_parser import TravelTranscriptParser
import json

app = Flask(__name__)
CORS(app)

@app.route("/api/generate-itinerary", methods=["POST"])
def generate_itinerary():
    """
    Generate a day-by-day travel itinerary with Google Maps routes.
    
    Expected Request JSON:
    {
        "video_transcript": "string",
        "video_description": "string",
        "ocr_transcript": "string"
    }

    Example JSON Response (Success):
    {
        "success": True,
        "itinerary": [
            {
                "day_number": 1,
                "locations": [...],
                "route_url": "http://google..."
            },
            ...
        ]
    }
    """
    data = request.json
    print(f"Request received: {data}")
    query = f" {data['place']} {data['days']} days itinerary"

    scraper = TikTokLinkScraper()
    links = scraper.get_links(query)
    print(links)

    # desc = get_tiktok_data(links[0])
    result = download_tiktok_video(links[0])
    print(result)
    audio_transcript = transcribe_video(result['filename'])
    print(audio_transcript)
    video_text = fast_extract_text(result['filename'])
    print(video_text)

    # travel_json_lst = asyncio.run(scrap_urls(links))

    parser = TravelTranscriptParser()

    # # for loop to merge description, audio transcript and OCR texts into one long string
    # all_desc = " ".join([d['metadata']['desc'] for d in travel_json_lst])
    # all_audio = " ".join([d['audio_transcript'] for d in travel_json_lst])
    # all_on_screen = " ".join([text for d in travel_json_lst for text in d['on_screen_text']])
    all_on_screen = " ".join(video_text)

    plans = parser.get_locations(audio_transcript, result['desc'], all_on_screen)
    plans_as_dicts = [day.model_dump() for day in plans]
    json_str = json.dumps(plans_as_dicts, indent=2)

    # goes through the list to get their string 
    return json_str
    # return jsonify({"places": ["Marina Bay Sands", "Art Science Museum", "National University of Singapore"]})

    # Your specific stub response
    stub_itinerary = [
        {
            "day_number": 1,
            "locations": [
                {
                    "name": "174 Bingo",
                    "description": "Start the trip with artisanal pastries and coffee in a cozy Joo Chiat bakery.",
                    "estimated_duration_minutes": 60
                },
                {
                    "name": "Henderson Waves",
                    "description": "A scenic walk across the tallest pedestrian bridge in Singapore, connecting green spaces.",
                    "estimated_duration_minutes": 90
                },
                {
                    "name": "TANCHEN Studio",
                    "description": "A creative workshop and shop specializing in unique handcrafted textiles.",
                    "estimated_duration_minutes": 45
                },
                {
                    "name": "Marina Barrage",
                    "description": "Sunset picnic and kite flying on the rooftop garden with city skyline views.",
                    "estimated_duration_minutes": 120
                }
            ],
            "route_url": "https://www.google.com/maps/dir/?api=1&origin=174BINGO&origin_place_id=ChIJJbm7jjcZ2jER78JnJknmuN4&waypoints=Henderson%20Waves%7CTANCHEN%20Studio&waypoint_place_ids=ChIJeXrAvBcb2jERhWAujA0K0LE%7CChIJxy80EM8Z2jERJ-5r4PuSGZo&destination=Marina%20Barrage&destination_place_id=ChIJ50uIMa0Z2jER0cTt5fLaZt0&travelmode=driving"
        },
        {
            "day_number": 2,
            "locations": [
                {
                    "name": "Maxwell Food Centre",
                    "description": "A legendary hawker center; try the famous Tian Tian Hainanese Chicken Rice.",
                    "estimated_duration_minutes": 60
                },
                {
                    "name": "KADA",
                    "description": "Visit this unique wellness hub and cafe located in a historic 101-year-old hospital.",
                    "estimated_duration_minutes": 90
                },
                {
                    "name": "Corner Corner",
                    "description": "Unwind in Duxton with specialty Japanese tea and a curated vinyl collection.",
                    "estimated_duration_minutes": 60
                },
                {
                    "name": "Gardens by the Bay",
                    "description": "Explore the Flower Dome and Cloud Forest before the nightly Supertree Grove light show.",
                    "estimated_duration_minutes": 180
                }
            ],
            "route_url": "https://www.google.com/maps/dir/?api=1&origin=Maxwell%20Food%20Centre&origin_place_id=ChIJseQsTQ0Z2jERqpBTWF0Zf84&waypoints=Kada%7CCorner%20Corner%20%28Coffee%20Concept%29&waypoint_place_ids=ChIJ8W0UHwAZ2jERPiAUP4JyR-M%7CChIJb_7hPWAZ2jERQ30PkQx3MpQ&destination=Gardens%20by%20the%20Bay&destination_place_id=ChIJMxZ-kwQZ2jERdsqftXeWCWI&travelmode=driving"
        },
        {
            "day_number": 3,
            "locations": [
                {
                    "name": "Fort Canning Park",
                    "description": "A historic hilltop park with the famous Sang Nila Utama Garden and spiral staircase.",
                    "estimated_duration_minutes": 90
                },
                {
                    "name": "National Gallery Singapore",
                    "description": "The world's largest public collection of Singapore and Southeast Asian modern art.",
                    "estimated_duration_minutes": 150
                },
                {
                    "name": "ArtScience Museum",
                    "description": "An iconic lotus-inspired building featuring the immersive 'Future World' exhibition.",
                    "estimated_duration_minutes": 120
                }
            ],
            "route_url": "https://www.google.com/maps/dir/?api=1&origin=Fort%20Canning%20Park&origin_place_id=ChIJVSYjJKIZ2jERpRFinATD52s&waypoints=National%20Gallery%20Singapore&waypoint_place_ids=ChIJFQzeR6cZ2jERgM6--iWeY-U&destination=ArtScience%20Museum&destination_place_id=ChIJnWdQKQQZ2jERScXuKeFHyIE&travelmode=driving"
        }
    ]

    return jsonify({
        "success": True,
        "itinerary": stub_itinerary
    })

if __name__ == "__main__":
    print("server started")