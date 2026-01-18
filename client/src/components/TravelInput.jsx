import { useState } from 'react';
import { useNavigate } from "react-router-dom";

export default function TravelInput({ className, loadingLogo }) {
  const [data, setData] = useState({ location: '', days: '' });
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const showItineraryLink = localStorage.getItem("itineraryData");

  async function handlePlanTrip() {
    setIsLoading(true);
    try {
      const fetchPromise = fetch("http://127.0.0.1:5000/api/generate-itinerary",
        {
          method:"POST",
          headers: {
              "Content-type": "application/json; charset=UTF-8"
          },
          body: JSON.stringify({
            "days": 3,
            "location": "Singapore"
          })
        }
      ).then(res => res.json());

      const timeoutPromise = new Promise(resolve =>
        setTimeout(() => {
          setIsLoading(false);
          resolve();
        }, 3000)
      );

      const itineraryData = await Promise.all([fetchPromise, timeoutPromise])
        .then(([data]) => data);

      // const response = await fetch("http://127.0.0.1:5000/api/generate-itinerary",
      //   {
      //     method:"POST",
      //     headers: {
      //         "Content-type": "application/json; charset=UTF-8"
      //     },
      //     body: JSON.stringify({
      //       "video_transcript": "string",
      //       "video_description": "string",
      //       "ocr_transcript": "string"
      //     })
      //   }
      // )
      
      // const itineraryData = await response.json();

      console.log(itineraryData.itinerary)
      localStorage.setItem("itineraryData", JSON.stringify(itineraryData.itinerary));

      navigate("/itinerary");
      
    } catch (error) {
      console.error("Error fetching places:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={`${className} relative bg-white p-8 md:p-20 flex flex-col justify-center`}>
      {isLoading && (
        <div className="absolute inset-0 bg-black/30 flex items-center justify-center z-50">
          <div className="flex flex-col items-center gap-4 p-6 bg-white rounded-xl shadow-lg">
            {/* Whimsical spinning bar */}
            <div className="w-32 h-32 md:w-40 md:h-40 overflow-hidden relative">
              <img
                src={loadingLogo}      // path to your GIF in public folder
                alt="Loading animation"
              />
            </div>
            <p className="text-gray-700 font-semibold text-center">
              Planning your trip with your fella...
            </p>
          </div>
        </div>
      )}
      <div className="max-w-md mx-auto w-full">
        <h2 className="text-2xl font-bold text-gray-800 mb-8">Planna with your fella</h2>
        <form className="space-y-6">
          <div>
            <label className="block text-sm font-semibold text-gray-600 mb-2">Destination</label>
            <input 
                type="text" 
                value={data.location}
                placeholder="e.g. Paris, France"
                className="w-full p-4 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none transition-all text-gray-800"
                onChange={(e) => setData({...data, location: e.target.value})}
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-600 mb-2">Duration (Days)</label>
            <input 
              type="number" 
              value={data.days}
              placeholder="2"
              className="w-full p-4 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none transition-all text-gray-800"
              onChange={(e) => setData({...data, days: e.target.value})}
            />
          </div>

          <button className="w-full py-4 bg-indigo-600 hover:bg-indigo-800 hover:cursor-pointer text-white font-bold rounded-xl shadow-lg shadow-indigo-200 transition-colors"
          type='button'
          onClick={handlePlanTrip}>
            Plan trip
          </button>
        </form>
      </div>
      {showItineraryLink && (
        <a
          href="/itinerary"
          className="
            fixed bottom-6 right-6
            bg-gray-300 text-gray-800
            px-8 py-4 rounded-full
            shadow-md
            hover:bg-gray-500 hover:text-gray-900
            transition-colors
            text-lg font-semibold
            z-50
          "
        >
          View Itinerary
        </a>
      )}
    </div>
  );
}