import {APIProvider, Map, Marker } from '@vis.gl/react-google-maps';
import { useRef } from 'react';

export default function TravelResults({className, places}) {
  const mapRef = useRef(null);

  places = places || [
    { name: "Eiffel Tower", description: "Iconic landmark with stunning views.", lat: 48.8584, lng: 2.2945 },
    { name: "Louvre Museum", description: "World’s largest art museum.", lat: 48.8606, lng: 2.3376 },
  ];
  
  return (
    <div className={`${className} bg-white p-8 md:p-20 flex flex-col justify-center`}>
      <div className="max-w-6xl mx-auto w-full flex flex-col md:flex-row gap-10">
        
        {/* --- MAP BOX --- */}
        <div className="flex-1">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Explore Your Trip</h2>
          <div
            ref={mapRef}
            id="map"
            className="w-full h-[400px] md:h-[600px] rounded-2xl shadow-lg border border-gray-200"
          >
            <Map defaultZoom={14} defaultCenter={{lat: 1.2867, lng: 103.8544}}>
              <Marker position={{lat: 1.2867, lng: 103.8544}} />
            </Map>
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