from flask import Flask, request, jsonify
from flask_cors import CORS
from tiktok_link_scraper.tiktok_link_scraper import TikTokLinkScraper
from tiktok_data_scraper.tiktokScrapper import download_tiktok_video
from tiktok_data_scraper.transcribeAudio import transcribe_video
from tiktok_data_scraper.videoTextExtractor import fast_extract_text
from parsers.travel_transcript_parser import TravelTranscriptParser
from route_url_builder.route_url_builder import RouteUrlBuilder
import json
import uuid
import threading
import concurrent.futures

app = Flask(__name__)
CORS(app)

request_map = {} # maps uuid to response object

def process_video_thread(i, link, job_id):
    """
    Worker function to handle a single video.
    Returns the processed text chunks for this specific video.
    """
    try:
        # Update status (Note: In a real app, use a lock for shared resources, 
        # but for a simple dict update this is generally fine in Python)
        request_map[job_id]["message"] = f"Processing video {i + 1}..."
        
        # 1. Download
        result = download_tiktok_video(link)
        
        # 2. Process (Transcribe & Extract)
        # We format the strings here to keep the main logic clean
        transcript_part = f" {i + 1}." + transcribe_video(result['filename'])
        text_part = f" {i + 1}." + " ".join(fast_extract_text(result['filename']))
        desc_part = f" {i + 1}." + result['desc']
        
        return {
            "index": i,
            "transcript": transcript_part,
            "text": text_part,
            "desc": desc_part
        }
    except Exception as e:
        print(f"Error processing video {i}: {e}")
        # Return empty strings so one failure doesn't break the whole itinerary
        return {
            "index": i, 
            "transcript": "", 
            "text": "", 
            "desc": ""
        }

def process_itinerary_task(job_id, data):
    try:
        print(f"[{job_id}] Starting processing...")
        
        # ... (Your existing code to get links) ...
        scraper = TikTokLinkScraper()
        query = f" {data['place']} {data['days']} days itinerary"
        links = scraper.get_links(query)
        
        # Limit to 3 links
        target_links = links[:3]
        
        # 1. Run threads in parallel
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            # Create a list of future tasks
            future_to_index = {
                executor.submit(process_video_thread, i, link, job_id): i 
                for i, link in enumerate(target_links)
            }
            
            # Wait for all to complete
            for future in concurrent.futures.as_completed(future_to_index):
                results.append(future.result())

        # 2. Sort results to maintain order (1, 2, 3)
        # Since threads finish randomly, we must sort by the original index
        results.sort(key=lambda x: x['index'])

        # 3. Combine the results
        audio_transcript = "".join(r['transcript'] for r in results)
        video_text = "".join(r['text'] for r in results)
        description = "".join(r['desc'] for r in results)

        # 4. Continue with your parser logic
        parser = TravelTranscriptParser()
        travel_sched = parser.get_locations(audio_transcript, description, video_text)
        
        route_builder = RouteUrlBuilder(travel_sched)
        route_details = route_builder.get_full_travel_details()
        route_details_dict = [day.model_dump() for day in route_details]

        request_map[job_id] = {
            "success": True,
            "status": "completed",
            "itinerary": route_details_dict
        }

        print(f"Completed job with id {job_id}")

    except Exception as e:
        print(f"[{job_id}] Error: {e}")
        request_map[job_id] = {
            "success": False,
            "status": "failed",
            "error": str(e)
        }

"""
Response
{
    "success": true,
    "status": "completed",
    "itinerary": [
        {
            "day_number": 1,
            "locations": [...],
            "coordinates": [[float, float], ...],
            "center": [float, float],
            "route_url": string
        },
        ...
    ]
}
"""

@app.route("/api/generate-itinerary", methods=["POST"])
def generate_itinerary():
    """
    Generate a day-by-day travel itinerary with Google Maps routes.
    
    Expected Request JSON:
    {
        "days": int
        "location": str
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
    # 1. Generate the Job ID
    job_id = str(uuid.uuid4())

    # 2. Set initial "pending" state
    request_map[job_id] = {
        "success": True,
        "job_id": job_id,
        "status": "pending"
    }

    # 3. Start the background thread
    data = request.json
    thread = threading.Thread(target=process_itinerary_task, args=(job_id, data))
    thread.daemon = True # Ensures thread dies if the main app quits
    thread.start()

    # 4. Return immediately with the Job ID
    return jsonify({
        "success": True,
        "job_id": job_id,
        "status": "pending"
    })

    # Your specific stub response
    stub_itinerary = [
        {
            "day_number": 1,
            "locations": [
                {"name": "174 Bingo", "description": "Start the trip with artisanal pastries and coffee in a cozy Joo Chiat bakery.", "estimated_duration_minutes": 60},
                {"name": "Henderson Waves", "description": "A scenic walk across the tallest pedestrian bridge in Singapore, connecting green spaces.", "estimated_duration_minutes": 90},
                {"name": "TANCHEN Studio", "description": "A creative workshop and shop specializing in unique handcrafted textiles.", "estimated_duration_minutes": 45},
                {"name": "Marina Barrage", "description": "Sunset picnic and kite flying on the rooftop garden with city skyline views.", "estimated_duration_minutes": 120}
            ],
            "coordinates": [[1.3121, 103.9023], [1.2761, 103.8152], [1.3115, 103.9015], [1.2808, 103.8711]],
            "center": [1.2951, 103.8725],
            "route_url": "http://google.com/maps/dir/..."
        },
        {
            "day_number": 2,
            "locations": [
                {"name": "Maxwell Food Centre", "description": "A legendary hawker center; try the famous Tian Tian Hainanese Chicken Rice.", "estimated_duration_minutes": 60},
                {"name": "KADA", "description": "Visit this unique wellness hub and cafe located in a historic 101-year-old hospital.", "estimated_duration_minutes": 90},
                {"name": "Corner Corner", "description": "Unwind in Duxton with specialty Japanese tea and a curated vinyl collection.", "estimated_duration_minutes": 60},
                {"name": "Gardens by the Bay", "description": "Explore the Flower Dome and Cloud Forest before the nightly Supertree Grove light show.", "estimated_duration_minutes": 180}
            ],
            "coordinates": [[1.2803, 103.8447], [1.2825, 103.8431], [1.2798, 103.8415], [1.2816, 103.8636]],
            "center": [1.2810, 103.8482],
            "route_url": "http://google.com/maps/dir/..."
        },
        {
            "day_number": 3,
            "locations": [
                {"name": "Fort Canning Park", "description": "A historic hilltop park with the famous Sang Nila Utama Garden and spiral staircase.", "estimated_duration_minutes": 90},
                {"name": "National Gallery Singapore", "description": "The world's largest public collection of Singapore and Southeast Asian modern art.", "estimated_duration_minutes": 150},
                {"name": "ArtScience Museum", "description": "An iconic lotus-inspired building featuring the immersive 'Future World' exhibition.", "estimated_duration_minutes": 120}
            ],
            "coordinates": [[1.2951, 103.8466], [1.2903, 103.8519], [1.2863, 103.8592]],
            "center": [1.2905, 103.8525],
            "route_url": "http://google.com/maps/dir/..."
        }
    ]

    return jsonify({
        "success": True,
        "itinerary": stub_itinerary
    })

@app.route("/api/itinerary-status/<job_id>", methods=["GET"])
def itinerary_status(job_id):
    """
    Client polls this endpoint to see if the job is done.
    """
    result = request_map.get(job_id)
    
    if not result:
        return jsonify({"success": False, "error": "Job ID not found"}), 404
        
    return jsonify(result)

if __name__ == "__main__":
    print("server started")