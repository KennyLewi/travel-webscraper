import TitleCard from "./components/TitleCard";
import TravelInput from "./components/TravelInput";
import TravelResults from "./components/TravelResults";
import {APIProvider} from '@vis.gl/react-google-maps';

const GOOGLE_API_KEY = import.meta.env.VITE_GOOGLE_API_KEY;

function App() {
  return (
    <APIProvider apiKey={GOOGLE_API_KEY} onLoad={() => console.log('Maps API has loaded.')}>
      <div className="flex flex-row w-screen h-screen">
        <TitleCard className="basis-1/3" />
        {/* <TravelInput className="basis-2/3" /> */}
        <TravelResults className="basis-2/3"/>
      </div>
    </APIProvider>
  );
}

export default App;