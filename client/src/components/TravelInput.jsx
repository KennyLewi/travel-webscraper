import { useState } from 'react';

export default function TravelInput({ className }) {
  const [data, setData] = useState({ location: '', days: '' });

  return (
    <div className={`${className} bg-white p-8 md:p-20 flex flex-col justify-center`}>
      <div className="max-w-md mx-auto w-full">
        <h2 className="text-2xl font-bold text-gray-800 mb-8">Planna with your fella</h2>
        <form className="space-y-6">
          <div>
            <label className="block text-sm font-semibold text-gray-600 mb-2">Destination</label>
            <input 
                type="text" 
                value={data.location}
                placeholder="e.g. Paris, France"
                className="w-full p-4 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none transition-all text-gray-800"
                onChange={(e) => setData({...data, location: e.target.value})}
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-600 mb-2">Duration (Days)</label>
            <input 
              type="number" 
              value={data.days}
              placeholder="7"
              className="w-full p-4 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none transition-all text-gray-800"
              onChange={(e) => setData({...data, days: e.target.value})}
            />
          </div>

          <button className="w-full py-4 bg-indigo-600 hover:bg-indigo-800 hover:cursor-pointer text-white font-bold rounded-xl shadow-lg shadow-indigo-200 transition-colors">
            Plan trip
          </button>
        </form>
      </div>
    </div>
  );
}