from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# Load the CSV file into a pandas dataframe
df = pd.read_csv('backend/data/Curly Hair Products - First Iteration.csv')

# Route to filter products
@app.route('/products', methods=['GET'])
def get_products():
    # Get query parameters from the request
    curl_pattern = request.args.get('curlPattern')
    hair_type = request.args.get('hairType')
    vegan = request.args.get('vegan')
    weight = request.args.get('weight')

    # Filter products based on query parameters
    filtered_df = df

    if curl_pattern:
        filtered_df = filtered_df[filtered_df['Curl Pattern'].str.contains(curl_pattern, na=False)]
    if hair_type:
        filtered_df = filtered_df[filtered_df['Hair Type'].str.contains(hair_type, na=False)]
    if vegan:
        filtered_df = filtered_df[filtered_df['Vegan?'] == vegan]
    if weight:
        filtered_df = filtered_df[filtered_df['Weight (L,M,H)'] == weight]

    # Convert the filtered dataframe to a list of dictionaries and return as JSON
    return jsonify(filtered_df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
