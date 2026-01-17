import TitleCard from "./components/TitleCard";
import TravelInput from "./components/TravelInput";
import TravelResults from "./components/TravelResults";
import {APIProvider} from '@vis.gl/react-google-maps';

const GOOGLE_API_KEY = import.meta.env.VITE_GOOGLE_API_KEY;

function App() {
  return (
    <APIProvider apiKey={GOOGLE_API_KEY} onLoad={() => console.log('Maps API has loaded.')}>
      <div className="flex flex-col w-screen h-screen bg-white">
        <div className="flex-none">
          <TitleCard className="w-full" logo="planefella.png" />
        </div>
        <div className="flex-1 pt-25">
          <TravelInput className="w-full h-full" />
          {/* <TravelResults className="w-full h-full"/> */}
        </div>
        
      </div>
    </APIProvider>
  );
}

export default App;