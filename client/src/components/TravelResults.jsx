import {Map, Marker } from '@vis.gl/react-google-maps';
import { useRef, useState, useEffect } from 'react';

export default function TravelResults({className}) {
  const mapRef = useRef(null);

  const [selectedDay, setSelectedDay] = useState(0);

  const positions = [
    [
      [1.2837574999999999, 103.8591065], 
      [1.2867449, 103.85438719999999], 
      [1.2892987999999999, 103.86313679999999], 
      [1.2862738, 103.8592663]
    ],
    [
      [1.3068072, 103.7883997], 
      [1.2830833, 103.78194060000001], 
      [1.2976493, 103.77669159999999]
    ],
    [
      [1.3068072, 103.7883997], 
      [1.2830833, 103.78194060000001], 
      [1.2976493, 103.77669159999999]
    ],
  ];

  const center = [
    [1.28651875, 103.85897419999999],
    [1.2958466, 103.78234396666666],
    [1.2958466, 103.78234396666666]
  ];

  const intializePlaces = () => {
    const savedItinerary = localStorage.getItem("itineraryData");
    if (savedItinerary) {
      const currRoutes = [];
      const locations = [];
      const itineraryList = JSON.parse(savedItinerary);
      
      itineraryList.forEach(day => {
          if (day.route_url) {
              currRoutes.push(day.route_url);
            }
          
          const tempLocations = [];
          // Add each location to the locations array
          if (day.locations) {
            day.locations.forEach(loc => {
              tempLocations.push(loc);
            });
          }
          locations.push(tempLocations);
      });
      console.log(locations);
      return locations
    }
  }

  const intializeRoutes = () => {
    const savedItinerary = localStorage.getItem("itineraryData");
    if (savedItinerary) {
      const currRoutes = [];
      const itineraryList = JSON.parse(savedItinerary);
      
      itineraryList.forEach(day => {
          if (day.route_url) {
              currRoutes.push(day.route_url);
            }
      });
      console.log(currRoutes);
      return currRoutes
    }
  }

  const [places, setPlaces] = useState(() => intializePlaces());
  // const [centers, setCenters] = useState([]);
  const [routes, setRoutes] = useState(() => intializeRoutes());

  // useEffect(() => {
  //     const savedPositions = localStorage.getItem("positions");
  //     if (savedPositions) {
  //       setPositions(JSON.parse(savedPositions))
  //     }

  //     const savedCenters = localStorage.getItem("centers");
  //     if (savedCenters) {
  //       setCenters(JSON.parse(savedCenters))
  //     }

  //     const savedRoutes = localStorage.getItem("routes");
  //     if (savedRoutes) {
  //       setRoutes(JSON.parse(savedRoutes))
  //     }

  // }, []);

  return (
    <div className={`${className} bg-white p-8 md:p-20 flex flex-col justify-center`}>
      <div className="max-w-6xl mx-auto w-full flex flex-col md:flex-row gap-10">
        
        {/* --- MAP BOX --- */}
        <div className="flex-1 flex flex-col">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Explore Your Trip</h2>

        <div
          ref={mapRef}
          id="map"
          className="w-full h-[400px] md:h-[550px] rounded-2xl shadow-lg border border-gray-200"
        >
          <Map defaultZoom={14} center={{ lat: center[selectedDay][0], lng: center[selectedDay][1] }}>
            {positions[selectedDay].map((pos, i) => (
              <Marker key={i} position={{ lat: pos[0], lng: pos[1] }} title={pos.name} />
            ))}
          </Map>
        </div>

        {/* --- Compact Route Link --- */}
        <div className="mt-4 w-max">
          <a
            href={routes[selectedDay]}
            target="_blank"
            rel="noopener noreferrer"
            className="px-4 py-2 bg-gray-200 text-gray-800 dark:text-gray-800 font-semibold rounded-lg shadow hover:bg-gray-400 transition-colors text-sm"
          >
            Open in Google Maps
          </a>
        </div>
      </div>

        {/* --- LOCATIONS LIST --- */}
        <div className="flex-1 md:max-w-md">
          <h3 className="text-xl font-semibold text-gray-700 mb-4">Places to Visit</h3>
          {/* --- Tabs --- */}
            <div className="flex gap-2 mb-4">
              {places.map((_, dayIndex) => (
                <button
                  key={dayIndex}
                  onClick={() => setSelectedDay(dayIndex)}
                  className={`px-4 py-2 rounded-xl font-semibold text-sm ${
                    selectedDay === dayIndex
                      ? "bg-gray-800 text-white"
                      : "bg-gray-200 text-gray-800 hover:bg-gray-300"
                  } transition-colors`}
                >
                  Day {dayIndex + 1}
                </button>
              ))}
            </div>

          <div className="space-y-4">
            {places[selectedDay].map((place, i) => (
              <div
                key={i}
                className="p-5 bg-white border border-gray-200 rounded-xl shadow hover:shadow-md transition-shadow"
              >
                <div className="flex justify-between items-start">
                  <h4 className="text-lg font-semibold text-gray-900">{place.name}</h4>
                  <span className="text-xs px-2 py-1 rounded-md bg-gray-100 text-gray-500">
                    {place.estimated_duration_minutes >= 60
                      ? place.estimated_duration_minutes % 60 > 0 
                        ?`${Math.floor(place.estimated_duration_minutes / 60)} hr ${place.estimated_duration_minutes % 60} min`
                        :`${Math.floor(place.estimated_duration_minutes / 60)} hr`
                      : `${place.estimated_duration_minutes} min`}
                  </span>
                </div>

                <p className="text-gray-600 mt-3 leading-relaxed">
                  {place.description}
                </p>
              </div>
            ))}
          </div>
        </div>

      </div>
      <a
          href="/"
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
          Back to Home
      </a>
    </div>
  );
}