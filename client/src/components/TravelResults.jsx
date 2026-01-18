import { Map, Marker } from '@vis.gl/react-google-maps';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function TravelResults({ className }) {
  const navigate = useNavigate();
  const [selectedDay, setSelectedDay] = useState(0);
  const [center, setCenter] = useState([]);

  // 1. Get the data
  const savedItinerary = localStorage.getItem("itineraryData");

  if (!savedItinerary) {
    return (
      <div className="h-screen flex flex-col items-center justify-center bg-gray-50 p-10">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">No Itinerary Found</h2>
        <p className="text-gray-600 mb-8 text-center">It looks like you haven't planned a trip yet, or your session expired.</p>
        <button 
          onClick={() => navigate('/')}
          className="px-6 py-3 bg-indigo-600 text-white rounded-xl font-bold shadow-lg hover:bg-indigo-700 transition-all"
        >
          Go Back Home
        </button>
      </div>
    );
  }

  // 3. Parse data only after the sanity check passes
  const itineraryList = JSON.parse(savedItinerary);
  const currentDay = itineraryList[selectedDay];

  // 4. Secondary sanity check: ensure the specific day exists
  if (!currentDay) return null;

  return (
    <div className={`${className} bg-white p-8 md:p-20 flex flex-col justify-center`}>
      <div className="max-w-6xl mx-auto w-full flex flex-col md:flex-row gap-10">
        
        {/* --- MAP BOX --- */}
        <div className="flex-1 flex flex-col">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Explore Your Trip</h2>

          <div className="w-full h-[400px] md:h-[550px] rounded-2xl shadow-lg border border-gray-200 overflow-hidden">
            <Map 
              key={center[0]}
              defaultZoom={13} 
              // Directly access the center from the current day object
              defaultCenter={{ lat: center[0], lng: center[1] }}
            >
              {currentDay.coordinates.map((pos, i) => (
                <Marker 
                  key={i} 
                  position={{ lat: pos[0], lng: pos[1] }} 
                  title={currentDay.locations[i]?.name} 
                />
              ))}
            </Map>
          </div>

          {/* --- Route Link --- */}
          {currentDay.route_url && (
            <div className="mt-4 w-max">
              <a
                href={currentDay.route_url}
                target="_blank"
                rel="noopener noreferrer"
                className="px-4 py-2 bg-gray-200 text-gray-800 font-semibold rounded-lg shadow hover:bg-gray-300 transition-colors text-sm"
              >
                Open in Google Maps
              </a>
            </div>
          )}
        </div>

        {/* --- LOCATIONS LIST --- */}
        <div className="flex-1 md:max-w-md">
          <h3 className="text-xl font-semibold text-gray-700 mb-4">Places to Visit</h3>
          
          {/* --- Tabs --- */}
          <div className="flex flex-wrap gap-2 mb-4">
            {itineraryList.map((curr, dayIndex) => (
              <button
                key={dayIndex}
                onClick={() => {
                  setSelectedDay(dayIndex)
                  setCenter(curr.center)
                }}
                className={`px-4 py-2 rounded-xl font-semibold text-sm transition-colors ${
                  selectedDay === dayIndex
                    ? "bg-gray-800 text-white"
                    : "bg-gray-200 text-gray-800 hover:bg-gray-300"
                }`}
              >
                Day {dayIndex + 1}
              </button>
            ))}
          </div>

          <div className="space-y-4">
            {currentDay.locations.map((place, i) => (
              <div
                key={i}
                className="p-5 bg-white border border-gray-200 rounded-xl shadow hover:shadow-md transition-shadow"
              >
                <div className="flex justify-between items-start">
                  <h4 className="text-lg font-semibold text-gray-900">{place.name}</h4>
                  <span className="text-xs px-2 py-1 rounded-md bg-gray-100 text-gray-500">
                    {place.estimated_duration_minutes >= 60
                      ? `${Math.floor(place.estimated_duration_minutes / 60)} hr ${place.estimated_duration_minutes % 60 > 0 ? (place.estimated_duration_minutes % 60) + ' min' : ''}`
                      : `${place.estimated_duration_minutes} min`}
                  </span>
                </div>
                <p className="text-gray-600 mt-3 leading-relaxed text-sm">
                  {place.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <button
        onClick={() => navigate('/')}
        className="fixed bottom-6 right-6 bg-gray-300 text-gray-800 px-8 py-4 rounded-full shadow-md hover:bg-gray-400 transition-colors text-lg font-semibold z-50"
      >
        Back to Home
      </button>
    </div>
  );
}