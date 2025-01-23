import React from 'react';

function Quiz({ onQuizSubmit }) {
  // Define the quiz logic here
  const handleSubmit = (event) => {
    event.preventDefault();
    // For example, pass quiz results to parent (App)
    onQuizSubmit({ result: 'Curly Hair Kit' });  // Replace with actual logic
  };

  return (
    <div>
      <h3>Curly Hair Quiz</h3>
      <form onSubmit={handleSubmit}>
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default Quiz;
