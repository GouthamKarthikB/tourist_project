import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

const PlaceDetails = () => {
  const { placeId } = useParams();
  const [placeDetails, setPlaceDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchPlaceDetails = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/users/place-details/`, {
          params: { place_id: placeId },
        });

        setPlaceDetails(response.data);
      } catch (err) {
        setError("Failed to fetch place details.");
      } finally {
        setLoading(false);
      }
    };

    fetchPlaceDetails();
  }, [placeId]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p className="text-red-500">{error}</p>;

  return (
    <div className="max-w-3xl mx-auto p-6 bg-white shadow-lg rounded-lg">
      <h1 className="text-3xl font-bold">{placeDetails.name}</h1>
      <p className="text-gray-600">{placeDetails.address}</p>
      <p className="text-gray-500">Rating: {placeDetails.rating || "N/A"}</p>

      {placeDetails.photo_url && (
        <img
          src={placeDetails.photo_url}
          alt={placeDetails.name}
          className="w-full h-60 object-cover rounded mt-4"
        />
      )}

      <p className="mt-4">{placeDetails.description || "No description available."}</p>
    </div>
  );
};

export default PlaceDetails;
