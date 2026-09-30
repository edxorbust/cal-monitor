import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login/Login";
import Dashboard from "./pages/Dashboard/Dashboard";
import Register from "./pages/Register/Register";
import Food from "./pages/Food/Food";
import Exercises from "./pages/Exercises/Exercises";
import Ingredients from "./pages/Ingredients/Ingredients";
import Profile from "./pages/Profile/Profile";
import PrivateRoute from "./components/PrivateRoute";
import "./App.css";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
    {/* Protected Routes */}
      <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
      <Route path="/food" element={<PrivateRoute><Food /></PrivateRoute>} />
      <Route path="/exercises" element={<PrivateRoute><Exercises /></PrivateRoute>} />
      <Route path="/ingredients" element={<PrivateRoute><Ingredients /></PrivateRoute>} />
      <Route path="/profile" element={<PrivateRoute><Profile /></PrivateRoute>} />

    </Routes>
  );
}

export default App;
