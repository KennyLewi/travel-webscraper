import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import TitleCard from "./components/TitleCard";
import TravelInput from "./components/TravelInput";
import TravelResults from "./components/TravelResults";
import {APIProvider} from '@vis.gl/react-google-maps';

const GOOGLE_API_KEY = import.meta.env.VITE_GOOGLE_API_KEY;

function App() {
  return (
    <BrowserRouter>
      <APIProvider apiKey={GOOGLE_API_KEY} onLoad={() => console.log('Maps API has loaded.')}>
        <div className="flex flex-col w-screen h-screen bg-white">
          <div className="flex-none">
            <Link to ="/">
              <TitleCard className="w-full" logo="planefella.png" />
            </Link>
          </div>
          <div className="flex-1 pt-25">
            <Routes>
              <Route path="/" element={<TravelInput className="w-full h-full" />} />
              <Route path="/itinerary" element={<TravelResults className="w-full h-full"/>} />
            </Routes>
          </div>
        </div>
      </APIProvider>

      
    </BrowserRouter>
  );
}

export default App;