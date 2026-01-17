from flask import Flask, request, jsonify
from flask_cors import CORS

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
    return jsonify({"places": ["Marina Bay Sands", "Art Science Museum", "National University of Singapore"]})