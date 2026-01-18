from typing import Optional
import os
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
    coordinates: Optional[list[list[float]]] = None
    center: Optional[list[float]] = None
    route_url: Optional[str] = None

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

            "6. OPTIONAL FIELDS: Leave the fields 'route_url', 'coordinates' and 'center' null."
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
    
if __name__ == "__main__":
    client = TravelTranscriptParser()
    video_transcript = " Singapore is boring. Perhaps this curated guy is here to change your mind. Spawn number one. 1-7 for Bingo. Located in Ju-Chad, 1-7 for Bingo is a cozy bakery and also a creative space for light-minded souls together. Other than selling amazing pastry, 1-7 for Bingo, a host-given like pop up from friends, conversation around food, and more. Spawn number two. Henderson Wave. The tallest pedestrian bridge in Singapore is a working show connecting the southern regions and Mount Feibur. It has a unique wave-like structure and is easily accessible for mobile stride. Many running clubs have included Henderson Wave as part of their running route. Spawn number three. Sunshine Studio. It is a collaborative textile and design studio founded by Sunshine and Ambichin. Sunshine Studio creates functional textile ranging from bags, coaster, photo-posts, to farm-border holder. The space will also host events like coffee pop-up, opening launch of each collection and more. Spawn number four. Kada. Just a 3-minute walk from Maxon and Marti. Kada converted from 101-year-old hospital to still tell this cute vintage lead. It is a new hospital with plenty of dining options and wellness experiences. You can still see the traces of the old building here. Spawn World 5 corner corner. A cafe filled with one-a-collection in Daxston serving specialty coffee, Japanese tea, and delicate desserts. Corner corner is a good-to-cafe, space-out, jagood music, and a conversation with the team about Wino. Spawn number six. Marina Baraj. Upon design the roof top that has opened to the public for free, allowing public to work out for picnics, kite flying, and enjoying the views of the city's skyline. It has become an iconic spot for community together with their families and friends. Now for its full social spaces, which are the vibrant, immediate spots where community, creativity, and culture come alive. We hope this guide helps you discover a style Singapore that's authentic, unexpected, and deeply energizing."
    video_desc = "A Guide to Singapore’s Community Spaces: 1️⃣ Breakfast at @174bingo: Grab a pastry at this cozy bakery that offers a creative space for like-minded souls, with regular pop up events.  2️⃣ Morning Walk at Henderson Waves: Stroll around this unique wave-structured walking trail, famously known for being the tallest pedestrian bridge in Singapore. 3️⃣ Shop at @tanchenstudio: Shop at this collaborative textile and design studio for one-of-a-kind functional textile pieces.  Don't miss out their pop up events too!  4️⃣ Chill & Sweat at @kada_sg: (3 mins walk from Maxwell MRT) Explore the dining and wellness offers in this hot spot that used to be a historical 101-Year old hospital. Keep an eye out for any traces of the old building!  5️⃣ Teatime at @corner_corner: (A short walk from KADA in Chinatown) Unwind over Japanese tea and delicate desserts while browsing their vinyl collection — a quiet corner where time slows down. 6️⃣ Picnic at Marina Barrage: Relax and have a picnic at this rooftop park, and enjoy the beautiful views of the city skyline.  Join in on the kite flying too for some fun! 🪁 Explore these unique places in Singapore, where community, creativity and culture come alive 🇸🇬 What's your favourite spot in Singapore? @visit_singapore #VisitSingapore #PassionMadePossible #MadeInSingapore #humanedition"
    ocr_transcript = '''"'0 'and is easily accessible from a bus ride 'easily accessible from (panel begins 7pm) (part 0#Cut 01 Breakfast at 0174Bingo 02 Morning Walk 02. Morning Walk 03, 03. Shopal 03. Shopat 03Shop at 04. ChiL& Swe_L 04. Chill & Sweat 04. Chill&Swel J 05. Teatime at 06. Picnic at 06. Pionic at 0sap 15 & 16 MAR, 0830AM - 033OPNT' TikTok 174 Bingo hosts event like 174 Bingo is a cozy bakery 174 joo chiat rd 174Bingo 174bingo 174bingo and maxi coffeebar 19 ~ 20 july; 1ZABingo 2 others 23jan 2025, thurs 23jan 2025,thurs 6 pm 721 74Bingo 8.30 pm 8.3Qam @Kuman editron @Nvan_edition @aeditron @f their running route @hUman_edition @hiuman/ edition @hlj: @humal @human /editlon @human ledition @human'edition @human-edition @human/edition @humanJedition @human edition @human_ecilon @human_edition @human_edition; @human_editiont @humancedition @humat`edition @hun @hunal_edition @hurajicedition @hyntdk Tok AAS BINA BINGC BINGO BINGQJ TikTok BINI Balrage Barrage Barrage€ Boring BulL CHEESECA Change Coffee Conversations Around Food (Live) Cornen Corner Corner Corner iS ago-to cafe to space out Corner Corner is a go-to cafe to space @ut Corner Cornerisa go-to cafe to space out Curated EXIT Etudio Euen ExIT FILTER COFFEE FOR GUIDE Gatunda Good Rest Awaits Gp BINGO HYpRoTHERAPY Henderson IRENE JANSEN Ice Bath Ihelecof Is Ol IsLow J TikTok JOXi Jad Japanese tea and delicate desserts Jel Jhuman_edition JikTok Jikdoke KADA KADA is converted Keu Khange Kok Kyukei ( Located in Joo Chiat Marina Mdort Mikixk Mlaxi Mondar Morning Walk Murray St Murray Stf N'1 ~ Rise &5 Grind NOW PLAYING O1 Breakfast at O1. Breakfast at OL. Breakfast at ON SU ONLY AT H Olhuman_edition P4ysio POP-UP PROBABLY THE Paur Sip; Eelong SAUNA SINGAPORE SLOM SOUP Sc4Fori Shop: Shopa Singapore is full of social spaces Solc SooI Stuca Stuclbo Studio Su_UL; Cenc - Malcha Sundna Au TANCHEN TANCHEN Studio creates functional textile TANGHEN THH Tai Tik Tok TikTo * TikTok TikTok' TikToko Tikii8k Tikio | Tiktok U" TikTok U'jikTok UTikTok Var Veage | VerGe Vnyl collection in Duxton WITH Wan_edlition Waves Wkok Xikiok YANCHEN agonia allowing public to walk up for picnics and and also a creative space and deeply energizing and enjoying the views of the city skyline and is and is easily accessible from a bus ride and wellness experiences as part of their running route auman_edition bingo, bingo; bus ride cafe filled with coffee p@p up collection and more conversation around food and more conversation around food ang creativity and culture come alive d TikTok d' TikTok dikTol editic edition enjoy foldable stools for like minded souls founded by Sanchia Tan and Amber Chen from 101-Year old hospital ft has become an iconic spot for community gonia good haus have included Henderson Waves helps you discover a side of Singapore human_edition hume irenebjansen is here to it has a unique wave like structure it has become an iconic spot for community it is a collaborative textile and design Studio it is a collaborative textile and design studio it is a new hot spot just a 3 minute walk from Maxwell MRT just a3 minute walk from Maxwell MRT just look at this cute vintage lift just lookat this cute vintage lift kyukei Collee luman_edition many running clubs mind moren_edition music oLSEaniicu< o_0 opening launch of eac opening launch of each collection and more other than selling amazing pastries park designed @ a rooftop pat pea te pechaps this perhaps this pop up ftom friends ranging from bags, coasters rdeeam rer adrniscion rer adrnistion ruai_edition sat & serving specialty coffee sltep In f0r our break that is authentic that"s @pen to the public for free that'S open to the public for free that's open t@ the public for free the Southern Ridges and Mount Faber the fun bottle holder the space will also host event like the tallest pedestrian bridge in Singapore the traces @f the old buildinghhere to gather to gather with their families and friends tudlio uman_edition unexpected uta Fe(eata Eu4n walking trail connecting we hope this guide where community which are the vibrant in between spots with plenty @f dining options with the team about vinyl you can still see {BaMI {TikTox {duida muallbkfortk ~LmTLeSS ~Oxer fer Takearor ~iitanjoncbllaatalo"'''
    print(client.get_locations(video_transcript, video_desc, ocr_transcript))