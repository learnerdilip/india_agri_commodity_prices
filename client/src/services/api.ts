const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000/api/v1";

export const fetchTradeData = async (filters = {}) => {
  // Convert { state: 'Goa' } to URL params string "?state=Goa"
  const params = new URLSearchParams(filters).toString();

  try {
    const response = await fetch(`${API_BASE}/enam-data/?${params}`);
    if (!response.ok) throw new Error("Network response was not ok");
    return await response.json();
  } catch (error) {
    console.error("Fetch error:", error);
    return [];
  }
};

export const fetchStates = async () => {
  const response = await fetch(`${API_BASE}/enam-data/states`);
  return await response.json();
};
