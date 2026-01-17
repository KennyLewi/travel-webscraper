from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

class LocationList(BaseModel):
    locations: list[str]
    
class TravelTranscriptParser:

    def __init__(self):
        self._client = genai.Client()
        self._model = "gemini-2.5-flash-lite"
        self._instructions = (
            "You are a travel data extractor. From the provided TikTok transcript, "
            "extract a list of attractions, landmarks, or restaurants that were recommended. "
            "Only give specific names (e.g., 'Disneyland') instead of generic ones (e.g., 'theme park'). "
            "If a city is mentioned, include it. Format the output as a simple comma-separated list."
        )

    def get_locations(self, transcript: str) -> list[str]:
        response = self._client.models.generate_content(
            model=self._model,
            config=types.GenerateContentConfig(
                system_instruction=self._instructions,
                response_mime_type="application/json",
                response_schema=LocationList,
            ),
            contents=transcript,
        )

        if response.parsed:
            return response.parsed.locations
        return []