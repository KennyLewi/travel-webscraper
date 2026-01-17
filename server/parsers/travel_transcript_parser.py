from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types
import os

load_dotenv()

class Location(BaseModel):
    name: str
    description: str
    estimated_duration_minutes: int

class DayPlan(BaseModel):
    day_number: int
    locations: list[Location]

class TravelSchedule(BaseModel):
    schedule: list[DayPlan]
    
class TravelTranscriptParser:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        self._client = genai.Client(api_key=api_key)
        self._model = "gemini-3-flash-preview"
        self._instructions = (
            "You are an expert travel itinerary planner. Your goal is to transform transcripts, "
            "video descriptions, and OCR text into a structured daily schedule.\n\n"
            
            "RULES:\n"
            "1. HIERARCHY OF TRUTH: If a name is written in the OCR text (Part 3) or Video Description (Part 2), "
            "you MUST use that spelling over the Audio Transcript (Part 1). For example, if the audio says "
            "'Sunshine Studio' but OCR says 'TANCHEN Studio', use 'TANCHEN Studio'.\n"
            
            "2. SPECIFICITY: Use exact names of venues. Never use generic terms like 'bakery' if the name "
            "is available.\n"
            
            "3. DAY SEGMENTATION: Group locations logically by day based on the video narrative. "
            "If the video feels like one continuous trip, group them into 'Day 1'.\n"
            
            "4. DURATION LOGIC: Estimate duration (in minutes) based on: \n"
            "   a) Explicit mentions in the video.\n"
            "   b) Context (e.g., 'breakfast' is usually 45-60 mins, 'a hike' is 90-120 mins).\n"
            "   c) Your internal knowledge of the specific landmark size.\n"
            
            "5. DESCRIPTIONS: Write a 1 sentence summary of what to do there based on the video content."
        )

    def get_locations(self, video_transcript: str, video_description: str, ocr_transcript: str) -> list[DayPlan]:
        user_prompt = (
            f"PART 1 (Audio Transcript): {video_transcript}\n"
            f"PART 2 (Video Description): {video_description}\n"
            f"PART 3 (OCR Texts): {ocr_transcript}"
        )

        response = self._client.models.generate_content(
            model=self._model,
            config=types.GenerateContentConfig(
                system_instruction=self._instructions,
                response_mime_type="application/json",
                response_schema=TravelSchedule,
            ),
            contents=user_prompt,
        )

        if response.parsed:
            return response.parsed.schedule
        return []
    