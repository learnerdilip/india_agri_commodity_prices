import { useEffect, useState } from "react";
import { fetchTradeData, fetchStates } from "./services/api";

function App() {
  const [data, setData] = useState([]);
  const [states, setStates] = useState([]);
  const [selectedState, setSelectedState] = useState("");

  // 1. Load initial data
  useEffect(() => {
    fetchStates().then(setStates);
    loadData();
  }, []);

  // 2. Fetch data when filters change
  const loadData = async () => {
    const filters = selectedState ? { state: selectedState } : {};
    const result = await fetchTradeData(filters);
    setData(result);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-green-700 mb-6">eNAM Dashboard</h1>

        {/* Filters */}
        <div className="bg-white p-4 rounded shadow mb-6 flex gap-4">
          <select 
            className="border p-2 rounded w-64"
            value={selectedState}
            onChange={(e) => setSelectedState(e.target.value)}
          >
            <option value="">-- All States --</option>
            {states.map((s) => <option key={s} value={s}>{s}</option>)}
          </select>
          
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
                  <td className="p-3">{row.fetched_date}</td>
                  <td className="p-3">{row.stateName}</td>
                  <td className="p-3">{row.apmcName}</td>
                  <td className="p-3">{row.commodityName}</td>
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