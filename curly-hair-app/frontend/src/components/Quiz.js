import React, { useState } from "react";

const Quiz = ({ onSubmit }) => {
  // State for user responses
  const [responses, setResponses] = useState({
    curlPattern: "",
    hairType: "",
    vegan: "",
    weightPreference: "",
    helpfulArea: "",
  });

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setResponses({ ...responses, [name]: value });
  };

  // Submit responses
  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(responses);
  };

  return (
    <div className="quiz-container">
      <h2 className="text-xl font-bold mb-4">Curly Hair Routine Quiz</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block font-medium">What is your curl pattern?</label>
          <select
            name="curlPattern"
            value={responses.curlPattern}
            onChange={handleChange}
            required
            className="border p-2 rounded"
          >
            <option value="">Select your curl pattern</option>
            <option value="2A, 2B, 2C">2A, 2B, 2C</option>
            <option value="3A, 3B, 3C">3A, 3B, 3C</option>
            <option value="4A, 4B, 4C">4A, 4B, 4C</option>
          </select>
        </div>
        <div>
          <label className="block font-medium">What is your hair type?</label>
          <select
            name="hairType"
            value={responses.hairType}
            onChange={handleChange}
            required
            className="border p-2 rounded"
          >
            <option value="">Select your hair type</option>
            <option value="Thin">Thin</option>
            <option value="Medium">Medium</option>
            <option value="Thick">Thick</option>
          </select>
        </div>
        <div>
          <label className="block font-medium">Do you prefer vegan products?</label>
          <select
            name="vegan"
            value={responses.vegan}
            onChange={handleChange}
            required
            className="border p-2 rounded"
          >
            <option value="">Select preference</option>
            <option value="Yes">Yes</option>
            <option value="No">No</option>
          </select>
        </div>
        <div>
          <label className="block font-medium">What is your weight preference?</label>
          <select
            name="weightPreference"
            value={responses.weightPreference}
            onChange={handleChange}
            required
            className="border p-2 rounded"
          >
            <option value="">Select preference</option>
            <option value="Light">Light</option>
            <option value="Medium">Medium</option>
            <option value="Heavy">Heavy</option>
          </select>
        </div>
        <div>
          <label className="block font-medium">What area do you want to address?</label>
          <select
            name="helpfulArea"
            value={responses.helpfulArea}
            onChange={handleChange}
            required
            className="border p-2 rounded"
          >
            <option value="">Select area</option>
            <option value="Shine">Shine</option>
            <option value="Nourish">Nourish</option>
          </select>
        </div>
        <button
          type="submit"
          className="bg-blue-500 text-white px-4 py-2 rounded mt-4"
        >
          Submit
        </button>
      </form>
    </div>
  );
};

export default Quiz;
