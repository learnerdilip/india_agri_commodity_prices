import { useEffect, useState } from "react";
import { fetchTradeData, fetchStates, fetchCommodities } from "./services/api";

function App() {
  const [data, setData] = useState([]);  
  const [states, setStates] = useState([]);
  const [selectedState, setSelectedState] = useState("");
  const [commodities, setCommodities] = useState([]);  
  const [selectedCommodity, setSelectedCommodity] = useState("");

  // 1. Load initial data
  useEffect(() => {
    fetchStates().then(setStates);
    fetchCommodities().then(setCommodities);
    loadData();
  }, []);

  // 2. Fetch data when filters change
  const loadData = async () => {
    const filters = {};
    
    // Only add filters if the user actually selected something
    if (selectedState) filters.state = selectedState;
    if (selectedCommodity) filters.commodity = selectedCommodity;

    const result = await fetchTradeData(filters);
    setData(result);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-green-700 mb-6">eNAM Dashboard</h1>

        <div className="bg-white p-4 rounded shadow mb-6 flex flex-wrap gap-4 items-end">
          
          {/* State Dropdown */}
          <div className="flex flex-col">
            <label className="text-sm font-semibold text-gray-600 mb-1">State</label>
            <select 
              className="border p-2 rounded w-64 focus:outline-none focus:ring-2 focus:ring-green-500"
              value={selectedState}
              onChange={(e) => setSelectedState(e.target.value)}
            >
              <option value="">-- All States --</option>
              {states.map((s) => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>

          {/* Commodity Dropdown */}
          <div className="flex flex-col">
            <label className="text-sm font-semibold text-gray-600 mb-1">Commodity</label>
            <select 
              className="border p-2 rounded w-64 focus:outline-none focus:ring-2 focus:ring-green-500"
              value={selectedCommodity}
              onChange={(e) => setSelectedCommodity(e.target.value)}
            >
              <option value="">-- All Commodities --</option>
              {commodities.map((c) => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>
          
          <button 
            onClick={loadData}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          >
            Search
          </button>
        </div>

        {/* Data Table */}
        <div className="bg-white rounded shadow overflow-hidden">
          <table className="w-full text-left">
            <thead className="bg-gray-200">
              <tr>
                <th className="p-3">Date</th>
                <th className="p-3">State</th>
                <th className="p-3">APMC</th>
                <th className="p-3">Commodity</th>
                <th className="p-3">Price</th>
              </tr>
            </thead>
            <tbody>
              {data.map((row) => (
                <tr key={row._id} className="border-t hover:bg-gray-50">
                  <td className="p-3">{row.created_at}</td>
                  <td className="p-3">{row.state}</td>
                  <td className="p-3">{row.apmc}</td>
                  <td className="p-3">{row.commodity}</td>
                  <td className="p-3 font-bold">₹{row.modal_price}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {data.length === 0 && (
            <div className="p-8 text-center text-gray-500">No records found.</div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;