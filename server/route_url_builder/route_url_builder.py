import copy
import requests
from dotenv import load_dotenv
import os
import json
from urllib.parse import quote

from parsers.travel_transcript_parser import TravelSchedule, DayPlan

# sample_response
sample_response = [
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
        ]
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
        ]
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
        ]
    }
]

load_dotenv()

class RouteUrlBuilder:
    
    def __init__(self, travel_sched: TravelSchedule):
        self._GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
        self._travel_sched = travel_sched
        self._day_information_list = [] # list of (place_ids, place_names, place_locations)

        for day_plan in self._travel_sched:
            self._day_information_list.append(self._get_places(day_plan))

    def get_full_travel_details(self):
        sched_with_routes = copy.deepcopy(self._travel_sched)

        for i, day_plan in enumerate(sched_with_routes):
            url = self._get_url(i + 1)
            coords_list = self._get_coordinates(i + 1)
            coords_center = self._get_coordinate_center(i + 1)

            day_plan.coordinates = coords_list
            day_plan.center = coords_center
            day_plan.route_url = url
            
        return sched_with_routes

    def _get_places(self, day_plan: DayPlan):
        url = 'https://places.googleapis.com/v1/places:searchText'
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self._GOOGLE_API_KEY,
            "X-Goog-FieldMask": "places.displayName,places.id,places.location"
        }

        responses = []
        for place in day_plan.locations:
            response = requests.post(url,
                            headers=headers,
                            json={
                                "textQuery": place.name
                            })
            responses.append(json.loads(response.text))

        place_ids = []
        place_names = []
        place_locations = []
        for r in responses:
            place_ids.append(r["places"][0]["id"])
            place_names.append(r["places"][0]["displayName"]["text"])
            latitude = r["places"][0]["location"]["latitude"]
            longitude = r["places"][0]["location"]["longitude"]
            place_locations.append([latitude, longitude])

        return (place_ids, place_names, place_locations)

    # Get url from places
    def _get_url(self, day_number):
        place_ids, place_names = self._day_information_list[day_number - 1][:2]
        dir_url = "https://www.google.com/maps/dir/?api=1"
        
        final_url = dir_url
        count = len(place_ids) - 1
        waypoint_place_ids = ""

        for place_id, place_name in zip(place_ids, place_names):
            if count == len(place_ids) - 1:
                final_url += "&origin=" + quote(place_name) + "&origin_place_id=" + place_id
            elif count == 0:
                if len(place_ids) > 2:
                    final_url += waypoint_place_ids
                final_url += "&destination=" + quote(place_name) + "&destination_place_id=" + place_id + "&travelmode=driving"
            elif count == len(place_ids) - 2:
                final_url += "&waypoints=" + quote(place_name)
                waypoint_place_ids += "&waypoint_place_ids=" + place_id
            else:
                final_url += quote("|") + quote(place_name)
                waypoint_place_ids += quote("|") + place_id
            count -= 1

        return final_url

    def _get_coordinates(self, day_number):
        return self._day_information_list[day_number - 1][2]
    
    def _get_coordinate_center(self, day_number):
        place_locations = self._get_coordinates(day_number)

        sum_lat = sum(lat for lat, _ in place_locations)
        sum_lon = sum(lon for _, lon in place_locations)
        n = len(place_locations)
        
        center_lat = sum_lat / n
        center_lon = sum_lon / n

        return [center_lat, center_lon]

if __name__ == "__main__":
    parsed_response = TravelSchedule(schedule=sample_response)
    r = RouteUrlBuilder(parsed_response.schedule)
    print(r.get_full_travel_details())