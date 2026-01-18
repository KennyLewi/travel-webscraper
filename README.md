# PlaneFella ✈️

Automatically turn TikTok travel videos into mapped itineraries

[Demo Video](https://youtu.be/iG4sZG4R9oI)

# 🚀 Overview

PlaneFella automates the entire process of converting TikTok travel videos into ready-to-use Google Maps itineraries.

<h3> 🛠️ How It Works </h3>

1. Gets the top-performing travel content related to the user's destination
2. Transcribes the audio and "reads" on-screen text via OCR to identify locations and activities
3. Groups the parsed locations into logical days
4. Maps the grouping into a Google Maps route

<h3> ✨ TL;DR </h3>

PlaneFella turns TikTok itineraries into ready-to-use Google Maps routes. :)

# 🔧 Installation
1. Clone the repository
2. Start server
```
cd server
pip install -r requirements.txt
flask run
```
3. Start client
```
cd ../client
npm install
npm run dev
```
