import React, { useState } from 'react';
import Quiz from './components/Quiz';

function App() {
  const [quizResults, setQuizResults] = useState(null);

  const handleQuizSubmit = (results) => {
    setQuizResults(results);
  };

  return (
    <div>
      <h1>Curly Hair Product Finder</h1>
      <Quiz onQuizSubmit={handleQuizSubmit} />
      {quizResults && <p>Recommended: {quizResults.result}</p>}
    </div>
  );
}

export default App;
