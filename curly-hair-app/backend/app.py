from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend communication

# Sample data (can be moved to products.json or a database)
products = [
    {"id": 1, "name": "Curl Cream", "price": "$15", "vegan": True},
    {"id": 2, "name": "Moisturizing Shampoo", "price": "$10", "vegan": False},
]

# Quiz API
@app.route('/quiz', methods=['POST'])
def quiz():
    preferences = request.json
    vegan_only = preferences.get('vegan', False)
    filtered_products = [p for p in products if not vegan_only or p['vegan']]
    return jsonify(filtered_products)

if __name__ == "__main__":
    app.run(debug=True)
