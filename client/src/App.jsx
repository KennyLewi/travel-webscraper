import TitleCard from "./components/TitleCard";
import TravelInput from "./components/TravelInput";

function App() {
  return (
    <div className="flex flex-row w-screen h-screen">
      <TitleCard className="basis-1/3" />
      <TravelInput className="basis-2/3" />
    </div>
  );
}

export default App;