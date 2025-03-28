import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const TouristPlaces = () => {
  const [placeName, setPlaceName] = useState("");
  const [places, setPlaces] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSearch = async () => {
    if (!placeName.trim()) {
      setError("Please enter a place name.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await axios.get("http://127.0.0.1:8000/api/users/tourist-places/", {
        params: { place_name: placeName },
      });

      if (response.data && response.data.places.length > 0) {
        setPlaces(response.data.places);
      } else {
        setPlaces([]);
        setError("No places found.");
      }
    } catch (err) {
      setError("Failed to fetch places. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white shadow-lg rounded-lg">
      <h2 className="text-2xl font-semibold mb-4">Search for Tourist Places</h2>

      <div className="flex space-x-2 mb-4">
        <input
          type="text"
          className="border p-2 flex-grow rounded-md"
          placeholder="Enter place name..."
          value={placeName}
          onChange={(e) => setPlaceName(e.target.value)}
        />
        <button
          className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-600"
          onClick={handleSearch}
        >
          Search
        </button>
      </div>

      {loading && <p className="text-gray-500">Loading...</p>}
      {error && <p className="text-red-500">{error}</p>}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {places.map((place) => (
          <div key={place.place_id} className="p-4 border rounded-lg shadow-md">
            <h3 className="text-lg font-semibold">{place.name}</h3>
            <p className="text-gray-600">{place.address}</p>

            {/* Click image to navigate to place details */}
            {place.photo_url ? (
              <img
                src={place.photo_url}
                alt={place.name}
                className="w-full h-40 object-cover rounded mt-2 cursor-pointer"
                onClick={() => navigate(`/place/${place.place_id}`)}
              />
            ) : (
              <p className="text-gray-500">No image available</p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default TouristPlaces;
