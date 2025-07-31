from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Updated inventory with gender-based categorization
inventory = {
    "Male": [
        {"category": "T-Shirts", "items": ["White T-Shirt", "Black T-Shirt", "Graphic Tee"]},
        {"category": "Jackets", "items": ["Denim Jacket", "Leather Jacket", "Bomber Jacket", "Racer Jacket"]},
        {"category": "Pants", "items": ["Blue Jeans", "Black Trousers", "Cargo Pants", "Quarter Pants"]},
        {"category": "Sneakers", "items": ["Nike Air Force-1", "Nike Jordan", "Adidas Samba", "Running Sneakers"]},
        {"category": "Accessories", "items": ["Watch", "Sunglasses", "Baseball Hat", "Beanie"]}
    ],
    "Female": [
        {"category": "T-Shirts", "items": ["White T-Shirt", "Black T-Shirt", "Graphic Tee"]},
        {"category": "Jackets", "items": ["Denim Jacket", "Leather Jacket", "Bomber Jacket"]},
        {"category": "Pants", "items": ["Blue Jeans", "Black Trousers", "Cargo Pants"]},
        {"category": "Sneakers", "items": ["Running Sneakers", "High-Top Sneakers", "Canvas Sneakers"]},
        {"category": "Skirts", "items": ["Mini Skirt", "Midi Skirt", "Maxi Skirt"]},
        {"category": "Accessories", "items": ["Watch", "Sunglasses", "Baseball Hat"]}
    ]
}

@app.route('/recommend', methods=['GET'])
def recommend_outfit():
    gender = request.args.get('gender', 'Male').capitalize()  # Case-insensitive
    category = request.args.get('category')  # Optional category filter

    if gender not in inventory:
        return jsonify({
            "error": "Invalid gender selection",
            "valid_options": list(inventory.keys())
        }), 400

    if category:
        selected_category = next((c for c in inventory[gender] if c["category"] == category), None)
        if not selected_category:
            return jsonify({"error": "Invalid category selection"}), 400
        outfit = {category: random.choice(selected_category["items"])}
    else:
        outfit = {c["category"]: random.choice(c["items"]) for c in inventory[gender]}

    return jsonify({"recommendation": outfit})

@app.route('/categories', methods=['GET'])
def get_categories():
    gender = request.args.get('gender', 'Male').capitalize()

    if gender not in inventory:
        return jsonify({
            "error": "Invalid gender selection",
            "valid_options": list(inventory.keys())
        }), 400

    categories = [category["category"] for category in inventory[gender]]
    return jsonify({"categories": categories})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Allow access from other devices
