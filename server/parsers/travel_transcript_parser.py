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
            "You are a travel data extractor. Extract specific names of attractions, landmarks, "
            "or restaurants from the provided transcripts. "
            "Only give specific names (e.g., 'Disneyland') instead of generic ones (e.g., 'theme park'). "
            "If a city is mentioned, include it"
            "The first part is an audio transcript; the second part contains OCR text from video frames. "
            "Use the OCR text to correct any misspellings or phonetic errors found in the audio transcript. "
            "Return only the final, corrected names of the locations."
        )

    def get_locations(self, video_transcript: str, ocr_transcript: str) -> list[str]:
        user_prompt = f"First Part (Audio Transcript): {video_transcript}, Second Part (OCR Texts): {ocr_transcript}"
        response = self._client.models.generate_content(
            model=self._model,
            config=types.GenerateContentConfig(
                system_instruction=self._instructions,
                response_mime_type="application/json",
                response_schema=LocationList,
            ),
            contents=user_prompt,
        )

        if response.parsed:
            return response.parsed.locations
        return []