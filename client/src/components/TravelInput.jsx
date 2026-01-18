import { useState } from 'react';
import { useNavigate } from "react-router-dom";

export default function TravelInput({ className, loadingLogo }) {
  const [data, setData] = useState({ location: '', days: '' });
  const [isLoading, setIsLoading] = useState(false);
  // 1. Add state for the status message
  const [statusMessage, setStatusMessage] = useState('Planning your trip...'); 
  
  const navigate = useNavigate();
  const showItineraryLink = localStorage.getItem("itineraryData");

  async function pollJobStatus(jobId) {
    const pollInterval = setInterval(async () => {
      try {
        const response = await fetch(`http://127.0.0.1:5000/api/itinerary-status/${jobId}`);
        const result = await response.json();

        if (result.status === "completed") {
          clearInterval(pollInterval);
          localStorage.setItem("itineraryData", JSON.stringify(result.itinerary));
          navigate("/itinerary");
          setIsLoading(false);
        } else if (result.status === "failed") {
          clearInterval(pollInterval);
          alert("Failed to generate itinerary: " + result.error);
          setIsLoading(false);
        } else if (result.status === "processing" || result.status === "pending") {
          // 2. Update the message from the backend
          if (result.message) {
            setStatusMessage(result.message);
          }
        }
      } catch (error) {
        console.error("Polling error:", error);
        clearInterval(pollInterval);
        setIsLoading(false);
      }
    }, 5000); 
  }

  async function handlePlanTrip() {
    if (!data.location || !data.days) {
      alert("Please fill in both fields!");
      return;
    }

    setIsLoading(true);
    setStatusMessage("Connecting to server..."); // Initial message

    try {
      const response = await fetch("http://127.0.0.1:5000/api/generate-itinerary", {
        method: "POST",
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        },
        body: JSON.stringify({
          place: data.location,
          days: parseInt(data.days)
        })
      });

      const startData = await response.json();

      if (startData.success && startData.job_id) {
        pollJobStatus(startData.job_id);
      } else {
        throw new Error("Failed to start background job");
      }

    } catch (error) {
      console.error("Error starting trip plan:", error);
      setIsLoading(false);
      alert("Something went wrong starting the process.");
    }
  }

  return (
    <div className={`${className} relative bg-white p-8 md:p-20 flex flex-col justify-center`}>
      {isLoading && (
        <div className="absolute inset-0 bg-black/30 flex items-center justify-center z-50">
          <div className="flex flex-col items-center gap-4 p-8 bg-white rounded-xl shadow-lg min-w-[300px]">
            <div className="w-32 h-32 md:w-40 md:h-40 overflow-hidden relative">
              <img
                src={loadingLogo}
                alt="Loading animation"
              />
            </div>
            {/* 3. Display the dynamic status message here */}
            <p className="text-gray-700 font-semibold text-center animate-pulse">
              {statusMessage}
            </p>
          </div>
        </div>
      )}

      {/* ... rest of your form code ... */}
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

          <button 
            className={`w-full py-4 font-bold rounded-xl shadow-lg transition-colors ${
              isLoading ? 'bg-gray-400 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-800 text-white'
            }`}
            type='button'
            onClick={handlePlanTrip}
            disabled={isLoading}
          >
            {isLoading ? "Planning..." : "Plan trip"}
          </button>
        </form>
      </div>

      {showItineraryLink && !isLoading && (
        <a 
          href="/itinerary" 
          className="fixed bottom-6 right-6 bg-gray-300 text-gray-800 px-8 py-4 rounded-full shadow-md hover:bg-gray-500 hover:text-gray-900 transition-colors text-lg font-semibold z-50"
        >
          View Itinerary
        </a>
      )}
    </div>
  );
}