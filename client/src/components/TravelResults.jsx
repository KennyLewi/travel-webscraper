import {Map, Marker } from '@vis.gl/react-google-maps';
import { useRef, useState, useEffect } from 'react';

export default function TravelResults({className, places}) {
  const mapRef = useRef(null);

  places = places || [
    [
      { name: "Eiffel Tower", description: "Iconic landmark with stunning views.", duration: "30"},
      { name: "Louvre Museum", description: "World’s largest art museum.", duration: "45" },
    ],
    [
      { name: "Marina Bay Sands", description: "Iconic landmark with stunning views.", duration: "60"},
      { name: "Singapore Flyer", description: "World’s largest art museum.", duration: "75" },
    ],
  ];

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
  ];

  const center = [
    [1.28651875, 103.85897419999999],
    [1.2958466, 103.78234396666666]
  ];

  const route = 'https://www.google.com/maps/dir/?api=1&origin=Marina%20Bay%20Sands%20Singapore&origin_place_id=ChIJA5LATO4Z2jER111V-v6abAI&waypoints=Merlion%20Park%20Singapore%7CSingapore%20Flyer&waypoint_place_ids=ChIJBTYg1g4Z2jERp_MBbu5erWY%7CChIJzVHFNqkZ2jERboLN2YrltH8&destination=Art%20Science%20Museum&destination_place_id=ChIJnWdQKQQZ2jERScXuKeFHyIE&travelmode=walking'
  
  // const [positions, setPositions] = useState([]);
  // const [centers, setCenters] = useState([]);
  // const [routes, setRoutes] = useState([])

  // useEffect(() => {
  //   async function fetchData() {
  //     try {
  //       const [positionsRes, centersRes, routesRes] = await Promise.all([
  //         fetch("positions_url"),
  //         fetch("centers_url"),
  //         fetch("routes_url")
  //       ]);

  //       // Parse all JSON in parallel
  //       const [positionsData, centersData, routesData] = await Promise.all([
  //         positionsRes.json(),
  //         centersRes.json(),
  //         routesRes.json()
  //       ]);

  //       // Update state
  //       setPositions(positionsData);
  //       localStorage.setItem("positions", JSON.stringify(positionsData));
  //       setCenters(centersData);
  //       localStorage.setItem("centers", JSON.stringify(centersData));
  //       setRoutes(routesData);
  //       localStorage.setItem("routes", JSON.stringify(routesData));
  //     } catch (error) {
  //       console.error("Error fetching places:", error);
  //     }
  //   }

  //   const savedPositions = localStorage.getItem("positions");
  //   if (savedPositions) {
  //     setPositions(JSON.parse(savedPositions))
  //   }

  //   const savedCenters = localStorage.getItem("centers");
  //   if (savedCenters) {
  //     setCenters(JSON.parse(savedCenters))
  //   }

  //   const savedRoutes = localStorage.getItem("routes");
  //   if (savedRoutes) {
  //     setRoutes(JSON.parse(savedRoutes))
  //   }

  //   fetchData();
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
            href={route}
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
                    {place.duration >= 60
                      ? place.duration % 60 > 0 
                        ?`${Math.floor(place.duration / 60)} hr ${place.duration % 60} min`
                        :`${Math.floor(place.duration / 60)} hr`
                      : `${place.duration} min`}
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
            px-10 py-6 rounded-full
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