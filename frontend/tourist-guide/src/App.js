import { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/auth/Login";
import TouristPlaces from "./components/TouristPlaces" ; // Example of a protected route
import PlaceDetails from "./components/PageDetails";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
        <Route path="/home" element={isAuthenticated ? <TouristPlaces /> : <Login setIsAuthenticated={setIsAuthenticated} />} />
        <Route path="/place/:placeId" element={<PlaceDetails />} />
      </Routes>
    </Router>
  );
}

export default App;
