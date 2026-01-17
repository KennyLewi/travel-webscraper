export default function TitleCard({ className }) {
  return (
    <div className={`${className} bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500 p-12 flex flex-col justify-center items-center text-center`}>
      <h1 className="text-4xl md:text-6xl font-black text-white tracking-tight">
        TRAVEL WEBSCRAPER
      </h1>
    </div>
  );
}