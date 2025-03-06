import { useState, useEffect } from "react";
import axios from "axios";

export default function TouristPlaces() {
  const [latitude, setLatitude] = useState(null);
  const [longitude, setLongitude] = useState(null);
  const [radius, setRadius] = useState(5000);
  const [places, setPlaces] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLatitude(position.coords.latitude);
          setLongitude(position.coords.longitude);
        },
        () => {
          setError("Location access denied. Please enable location services.");
        }
      );
    } else {
      setError("Geolocation is not supported by this browser.");
    }
  }, []);

  const fetchPlaces = async () => {
    if (!latitude || !longitude) {
      setError("Unable to get location.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get(
        `http://127.0.0.1:8000/api/users/tourist-places/?lat=${latitude}&lon=${longitude}&radius=${radius}&limit=20`
      );
      setPlaces(response.data.places || []);
    } catch (err) {
      setError("Failed to fetch places. Try again later.");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center p-6">
      <h1 className="text-3xl font-bold mb-4">Tourist Guide</h1>
      <div className="flex gap-4 mb-6">
        <label htmlFor="radius" className="sr-only">Search Radius</label>
        <input
          type="number"
          id="radius"   // ✅ Added id
          name="radius" // ✅ Added name
          className="p-2 rounded-lg bg-gray-800 border border-gray-600"
          value={radius}
          onChange={(e) => setRadius(e.target.value)}
          placeholder="Enter radius in meters"
        />
        <button
          onClick={fetchPlaces}
          className="bg-blue-600 px-4 py-2 rounded-lg font-semibold hover:bg-blue-700"
        >
          Search Places
        </button>
      </div>
      {error && <p className="text-red-500">{error}</p>}
      {loading ? (
        <p className="text-gray-400">Loading places...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {places.map((place, index) => (
            <div
              key={index}
              className="bg-gray-800 p-4 rounded-lg shadow-lg flex flex-col items-center"
            >
              <img
                src={place.image_urls[0] || "https://via.placeholder.com/300"}
                alt={place.name}
                className="w-full h-48 object-cover rounded-lg"
              />
              <h2 className="text-xl font-bold mt-2">{place.name}</h2>
              <p className="text-gray-400">{place.address}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
