import requests
from dotenv import load_dotenv
import os
import json
from urllib.parse import quote

# Dummy queries
query_1 = "Marina Bay Sands Singapore"
query_2 = "Merlion Park Singapore"
query_3 = "Singapore Flyer"
query_4 = "Art Science Museum"
queries = [query_1, query_2, query_3, query_4]
place_ids = ['ChIJA5LATO4Z2jER111V-v6abAI', 'ChIJBTYg1g4Z2jERp_MBbu5erWY',
             'ChIJzVHFNqkZ2jERboLN2YrltH8', 'ChIJnWdQKQQZ2jERScXuKeFHyIE']

class RouteUrlBuilder:
    
    def __init__(self):
        load_dotenv()
        self._GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    # Returns a tuple of (place_ids, place_locations) associated with the place names
    def _get_place_information(self, places):
        url = 'https://places.googleapis.com/v1/places:searchText'
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self._GOOGLE_API_KEY,
            "X-Goog-FieldMask": "places.displayName,places.id,places.location"
        }

        responses = []
        for place in places:
            response = requests.post(url,
                            headers=headers,
                            json={
                                "textQuery": place
                            })
            responses.append(json.loads(response.text))

        place_ids = []
        place_locations = []
        for r in responses:
            place_ids.append(r["places"][0]["id"])
            latitude = r["places"][0]["location"]["latitude"]
            longitude = r["places"][0]["location"]["longitude"]
            place_locations.append([latitude, longitude])

        self._place_information = (place_ids, place_locations)

        return self._place_information

    # Get url from places
    def get_url(self, places):
        if hasattr(self, "_place_information"):
            place_ids, place_locations = self._place_information
        else:
            place_ids, place_locations = self._get_place_information(places)

        dir_url = "https://www.google.com/maps/dir/?api=1"
        
        final_url = dir_url
        count = len(queries) - 1
        waypoint_place_ids = ""

        for i, q in enumerate(queries):
            if count == len(queries) - 1:
                final_url += "&origin=" + quote(q) + "&origin_place_id=" + place_ids[i]
            elif count == 0:
                if len(queries) > 2:
                    final_url += waypoint_place_ids
                final_url += "&destination=" + quote(q) + "&destination_place_id=" + place_ids[i] + "&travelmode=walking"
            elif count == len(queries) - 2:
                final_url += "&waypoints=" + quote(q)
                waypoint_place_ids += "&waypoint_place_ids=" + place_ids[i]
            else:
                final_url += quote("|") + quote(q)
                waypoint_place_ids += quote("|") + place_ids[i]
            count -= 1

        return final_url

    def get_coordinates(self, places):
        if hasattr(self, "_place_information"):
            place_ids, place_locations = self._place_information
        else:
            place_ids, place_locations = self._get_place_information(places)
        
        return place_locations
    
    def get_coordinate_center(self, places):
        if hasattr(self, "_place_information"):
            place_ids, place_locations = self._place_information
        else:
            place_ids, place_locations = self._get_place_information(places)

        sum_lat = sum(lat for lat, _ in place_locations)
        sum_lon = sum(lon for _, lon in place_locations)
        n = len(place_locations)
        
        center_lat = sum_lat / n
        center_lon = sum_lon / n

        return [center_lat, center_lon]

r = RouteUrlBuilder()
print(r.get_coordinates(queries))