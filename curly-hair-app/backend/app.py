from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load the CSV file
df = pd.read_csv(
    "/Users/laurenlanda/PycharmProjects/CapstoneCurlyProj/curly-hair-app/backend/data/Curly Hair Products - First Iteration.csv")


@app.route("/quiz", methods=["POST"])
def quiz():
    data = request.json
    hair_type = data.get("hairType")
    thickness = data.get("thickness")
    price_range = data.get("priceRange")

    # Map price range to price thresholds
    price_map = {"$": 0, "$$": 15, "$$$": 30}
    price_threshold = price_map.get(price_range, 30)  # Default to max price

    # Filter products based on quiz data
    filtered = df[
        (df["Hair Type"].str.contains(hair_type, na=False)) &
        (df["Weight (L,M,H)"].str.contains(thickness, na=False)) &
        (df["Price"] <= price_threshold)
        ]
    # Debug filtered results
    print(f"Filtered products: {filtered}")

    # Select up to 3 products for the routine
    recommendations = filtered.head(3).to_dict(orient="records")
    print(f"Recommendations: {recommendations}")  # Debug recommendations
    return jsonify(recommendations)


exit()

if __name__ == "__main__":
    app.run(debug=True)
