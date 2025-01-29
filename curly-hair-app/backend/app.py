from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load the CSV file
CSV_PATH = "/Users/laurenlanda/PycharmProjects/CapstoneCurlyProj/curly-hair-app/backend/data/Curly Hair Products - First Iteration.csv"

try:
    df = pd.read_csv(CSV_PATH)
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")  # Ensure price is numeric
    df = df.dropna(subset=["Price"])  # Remove invalid prices
    print("✅ CSV Loaded Successfully")
except Exception as e:
    print(f"❌ Error Loading CSV: {e}")

@app.route("/quiz", methods=["POST"])
def quiz():
    data = request.json
    hair_type = data.get("hairType", "").strip()
    thickness = data.get("thickness", "").strip()
    price_range = data.get("priceRange", "").strip()

    # Price thresholds
    price_map = {"$": 0, "$$": 15, "$$$": 30}

    # Debugging print statements
    print(f"📩 Received Quiz Data: Hair Type: {hair_type}, Thickness: {thickness}, Price: {price_range}")

    # Filter products
    filtered = df[
        (df["Hair Type"].str.contains(hair_type, na=False, case=False)) &
        (df["Weight (L,M,H)"].str.contains(thickness, na=False, case=False)) &
        (df["Price"] <= price_map[price_range])
    ]

    print(f"🔎 Filtered Products: {len(filtered)} found")

    # Select up to 3 products
    recommendations = filtered.head(3).to_dict(orient="records")

    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(debug=True)
