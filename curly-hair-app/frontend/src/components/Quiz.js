import React, { useState } from "react";

function Quiz({ onSubmit }) {
    const [hairType, setHairType] = useState("");
    const [thickness, setThickness] = useState("");
    const [priceRange, setPriceRange] = useState("");

    const handleSubmit = (event) => {
        event.preventDefault();

        if (!hairType || !thickness || !priceRange) {
            alert("⚠️ Please select all options.");
            return;
        }

        const quizData = { hairType, thickness, priceRange };
        console.log("📤 Submitting Quiz Data:", quizData);
        onSubmit(quizData);
    };

    return (
        <form onSubmit={handleSubmit}>
            <h3>Select Your Hair Type</h3>
            {["2A", "2B", "2C", "3A", "3B", "3C", "4A", "4B", "4C"].map((type) => (
                <button key={type} type="button" onClick={() => setHairType(type)}>
                    {type}
                </button>
            ))}

            <h3>Hair Thickness</h3>
            {["L", "M", "H"].map((w) => (
                <button key={w} type="button" onClick={() => setThickness(w)}>
                    {w}
                </button>
            ))}

            <h3>Price Preference</h3>
            {["$", "$$", "$$$"].map((p) => (
                <button key={p} type="button" onClick={() => setPriceRange(p)}>
                    {p}
                </button>
            ))}

            <br />
            <button type="submit">Get Routine</button>
        </form>
    );
}

export default Quiz;
