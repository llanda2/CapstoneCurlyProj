import React, { useState } from "react";

const App = () => {
  const [hairType, setHairType] = useState("");
  const [thickness, setThickness] = useState("");
  const [priceRange, setPriceRange] = useState("");

  const handleSubmit = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/quiz", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          hairType,
          thickness,
          priceRange,
        }),
      });

      const data = await response.json();
      console.log("Recommended products:", data); // For debugging
      alert(`Recommended routine: ${JSON.stringify(data)}`);
    } catch (error) {
      console.error("Error submitting quiz:", error);
      alert("Something went wrong. Please try again.");
    }
  };

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-6">Find Your Curly Hair Routine</h1>

      {/* Question 1: Hair Type */}
      <div className="mb-6">
        <h2 className="text-lg font-semibold">What is your hair type?</h2>
        <div className="flex gap-2 mt-2">
          {["2A", "3B", "4C"].map((type) => (
            <button
              key={type}
              className={`px-4 py-2 rounded-md ${
                hairType === type ? "bg-blue-500 text-white" : "bg-gray-200"
              }`}
              onClick={() => setHairType(type)}
            >
              {type}
            </button>
          ))}
        </div>
      </div>

      {/* Question 2: Thickness */}
      <div className="mb-6">
        <h2 className="text-lg font-semibold">What is your hair thickness?</h2>
        <div className="flex gap-2 mt-2">
          {["Thin", "Medium", "Thick"].map((option) => (
            <button
              key={option}
              className={`px-4 py-2 rounded-md ${
                thickness === option ? "bg-blue-500 text-white" : "bg-gray-200"
              }`}
              onClick={() => setThickness(option)}
            >
              {option}
            </button>
          ))}
        </div>
      </div>

      {/* Question 3: Price Range */}
      <div className="mb-6">
        <h2 className="text-lg font-semibold">What is your price range?</h2>
        <div className="flex gap-2 mt-2">
          {["$", "$$", "$$$"].map((price) => (
            <button
              key={price}
              className={`px-4 py-2 rounded-md ${
                priceRange === price ? "bg-blue-500 text-white" : "bg-gray-200"
              }`}
              onClick={() => setPriceRange(price)}
            >
              {price}
            </button>
          ))}
        </div>
      </div>

      {/* Submit Button */}
      <button
        className="bg-green-500 text-white px-6 py-3 rounded-md hover:bg-green-600"
        onClick={handleSubmit}
        disabled={!hairType || !thickness || !priceRange}
      >
        Get Recommendations
      </button>
    </div>
  );
};

export default App;
