import React, { useState } from "react";
import Quiz from "./Quiz";

function App() {
    const [recommendedRoutine, setRecommendedRoutine] = useState([]);

    const handleQuizSubmit = async (quizData) => {
        try {
            console.log("📩 Sending Quiz Data to Backend:", quizData);
            const response = await fetch("http://127.0.0.1:5000/quiz", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(quizData),
            });

            if (!response.ok) throw new Error("Server error");

            const data = await response.json();
            console.log("✅ Received Recommended Routine:", data);
            setRecommendedRoutine(data);
        } catch (error) {
            console.error("❌ Error submitting quiz:", error);
            alert("Something went wrong, please try again.");
        }
    };

    return (
        <div>
            <h1>Curly Hair Routine Quiz</h1>
            <Quiz onSubmit={handleQuizSubmit} />
            <h2>Recommended Routine</h2>
            {recommendedRoutine.length > 0 ? (
                <ul>
                    {recommendedRoutine.map((product, index) => (
                        <li key={index}>
                            <strong>{product.Name}</strong> - {product.Category} - ${product.Price}
                        </li>
                    ))}
                </ul>
            ) : (
                <p>No recommendations yet. Take the quiz!</p>
            )}
        </div>
    );
}

export default App;
