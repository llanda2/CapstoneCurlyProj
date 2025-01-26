import React from "react";

const Routine = ({ routine }) => {
  if (!routine || routine.length === 0) {
    return <p>No routine found. Please adjust your quiz answers.</p>;
  }

  return (
    <div className="routine-container">
      <h2 className="text-xl font-bold mb-4">Your Curly Hair Routine</h2>
      <ul className="space-y-4">
        {routine.map((item, index) => (
          <li key={index} className="border p-4 rounded">
            <h3 className="text-lg font-bold">{item.Name}</h3>
            <p>Brand: {item.Brand}</p>
            <p>Category: {item.Category}</p>
            <p>Price: ${item.Price.toFixed(2)}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Routine;
