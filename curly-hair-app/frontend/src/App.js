import React, { useState } from "react";
import axios from "axios";
import Quiz from "./components/Quiz";
import Routine from "./components/Routine";

const App = () => {
  const [routine, setRoutine] = useState([]);

  // Function to call Flask backend and fetch filtered products
  const fetchProducts = async (responses) => {
    const params = {
      curlPattern: responses.curlPattern,
      hairType: responses.hairType,
      vegan: responses.vegan,
      weight: responses.weightPreference,
    };
    try {
      const response = await axios.get("http://localhost:5000/products", { params });
      return response.data;
    } catch (error) {
      console.error("Error fetching products:", error);
      return [];
    }
  };

  // Function to handle quiz submission
  const handleQuizSubmit = async (responses) => {
    const filteredRoutine = await fetchProducts(responses);
    setRoutine(filteredRoutine);
  };

  return (
    <div className="app-container p-8">
      <Quiz onSubmit={handleQuizSubmit} />
      <Routine routine={routine} />
    </div>
  );
};

export default App;
