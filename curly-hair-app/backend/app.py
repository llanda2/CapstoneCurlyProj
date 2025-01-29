from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load the CSV file
df = pd.read_csv(
    "/Users/laurenlanda/PycharmProjects/CapstoneCurlyProj/curly-hair-app/backend/data/Curly Hair Products - First "
    "Iteration.csv"
)


@app.route("/quiz", methods=["POST"])
def quiz():
    data = request.json
    hair_type = data.get("hairType")
    thickness = data.get("thickness")
    price_range = data.get("priceRange")

    # Map price range to price thresholds
    price_map = {"$": 0, "$$": 15, "$$$": 30}

    # Filter products based on quiz data
    filtered = df[
        (df["Hair Type"].apply(lambda x: hair_type in x.split(", "))) &  # Check for hair type match
        (df["Weight (L,M,H)"] == thickness) &  # Check for thickness
        (df["Price"] <= price_map[price_range])  # Check for price range
        ]

    # Select up to 3 products for the routine
    recommendations = filtered.head(3).to_dict(orient="records")
    return jsonify(recommendations)


if __name__ == "__main__":
    app.run(debug=True)
