import {APIProvider, Map, Marker } from '@vis.gl/react-google-maps';
import { useRef } from 'react';

export default function TravelResults({className, places}) {
  const mapRef = useRef(null);

  places = places || [
    { name: "Eiffel Tower", description: "Iconic landmark with stunning views.", lat: 48.8584, lng: 2.2945 },
    { name: "Louvre Museum", description: "World’s largest art museum.", lat: 48.8606, lng: 2.3376 },
  ];

  const positions = [
    [1.2837574999999999, 103.8591065], 
    [1.2867449, 103.85438719999999], 
    [1.2892987999999999, 103.86313679999999], 
    [1.2862738, 103.8592663]
  ];

  const center = [1.2867449, 103.85438719999999];

  const route = 'https://www.google.com/maps/dir/?api=1&origin=Marina%20Bay%20Sands%20Singapore&origin_place_id=ChIJA5LATO4Z2jER111V-v6abAI&waypoints=Merlion%20Park%20Singapore%7CSingapore%20Flyer&waypoint_place_ids=ChIJBTYg1g4Z2jERp_MBbu5erWY%7CChIJzVHFNqkZ2jERboLN2YrltH8&destination=Art%20Science%20Museum&destination_place_id=ChIJnWdQKQQZ2jERScXuKeFHyIE&travelmode=walking'
  
  return (
    <div className={`${className} bg-white p-8 md:p-20 flex flex-col justify-center`}>
      <div className="max-w-6xl mx-auto w-full flex flex-col md:flex-row gap-10">
        
        {/* --- MAP BOX --- */}
        <div className="flex-1 flex flex-col">
        <h2 className="text-2xl font-bold text-gray-800 mb-4">Explore Your Trip</h2>

        <div
          ref={mapRef}
          id="map"
          className="w-full h-[400px] md:h-[600px] rounded-2xl shadow-lg border border-gray-200"
        >
          <Map defaultZoom={14} defaultCenter={{ lat: center[0], lng: center[1] }}>
            {positions.map((pos, i) => (
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
          <div className="space-y-4">
            {places.map((place, i) => (
              <div
                key={i}
                className="p-5 bg-gray-50 border border-gray-200 rounded-xl shadow-sm"
              >
                <h4 className="text-lg font-bold text-gray-800">{place.name}</h4>
                <p className="text-gray-600 mt-1">{place.description}</p>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
}