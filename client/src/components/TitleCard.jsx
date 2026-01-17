export default function TitleCard({ className, logo }) {
  return (
    <div
      className={`${className} fixed top-0 left-0 w-full bg-white border-b border-gray-200 p-6 md:p-8 flex flex-col justify-center items-center text-center shadow-lg z-50`}
    >
      {/* --- Logo + Title Row --- */}
      <div className="flex items-center justify-center mb-2">
        {logo && (
          <img
            src={logo}
            alt="App Logo"
            className="w-12 h-12 md:w-16 md:h-16 object-contain mr-4"
          />
        )}
        <h1 className="text-3xl md:text-5xl font-extrabold text-gray-900 tracking-tight">
          PlaneFella
        </h1>
      </div>

      {/* --- Subtitle / Whimsical touch --- */}
      <p className="text-gray-500 text-sm md:text-lg italic">
        Fella for your planna ;D
      </p>
    </div>
  );
}
