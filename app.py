from flask import Flask, render_template, request, jsonify
import json
import nltk
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load property data
try:
    with open('property_data.json') as f:
        properties = json.load(f)
    print(f"Successfully loaded {len(properties)} properties")
except Exception as e:
    print(f"Error loading property data: {e}")
    properties = []

# NLP setup
nltk.download('punkt')
nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

def preprocess(text):
    tokens = word_tokenize(text.lower())
    return [lemmatizer.lemmatize(token) for token in tokens]

def extract_criteria(message):
    message = message.lower()
    criteria = {}

    # Property type
    if 'house' in message:
        criteria['type'] = 'house'
    elif 'condo' in message:
        criteria['type'] = 'condo'
    elif 'apartment' in message:
        criteria['type'] = 'apartment'
    elif 'townhouse' in message:
        criteria['type'] = 'townhouse'

    # Price extraction
    price_match = re.search(r'(under|below|less than|max)\D*(\$?\s*\d[\d,kK]*)', message)
    if price_match:
        price = price_match.group(2).replace('$', '').replace(',', '').strip()
        if 'k' in price or 'K' in price:
            price = price.replace('k', '').replace('K', '')
            criteria['price_max'] = int(float(price) * 1000)
        else:
            criteria['price_max'] = int(price)

    # Bedroom count
    bed_match = re.search(r'(\d+)\s*(bed|bedroom|br|bd)', message)
    if bed_match:
        criteria['bedrooms'] = int(bed_match.group(1))
    elif 'studio' in message:
        criteria['bedrooms'] = 0

    print(f"Extracted criteria: {criteria}")
    return criteria

def find_properties(criteria):
    results = []

    for prop in properties:
        match = True

        if 'price_max' in criteria and prop['price'] > criteria['price_max']:
            match = False

        if 'bedrooms' in criteria and prop['bedrooms'] != criteria['bedrooms']:
            match = False

        if 'type' in criteria and criteria['type'] != prop['type'].lower():
            match = False

        if match:
            results.append(prop)

    print(f"Found {len(results)} matching properties")
    return results

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message']
        print(f"User message: {user_message}")

        if any(word in user_message.lower() for word in ['hi', 'hello', 'hey']):
            return jsonify({'response': "Hello! I can help you find properties. Tell me what you're looking for (e.g., '2 bedroom house under $300k')."})

        if 'thank' in user_message.lower():
            return jsonify({'response': "You're welcome! Let me know if you need anything else."})

        criteria = extract_criteria(user_message)
        matched_properties = find_properties(criteria)

        if matched_properties:
            response = f"I found {len(matched_properties)} matching properties:\n"
            for prop in matched_properties[:3]:
                response += f"\n{prop['address']} - ${prop['price']:,} - {prop['bedrooms']} bed, {prop['bathrooms']} bath"
            response += "\n\nWould you like more details about any of these?"
        else:
            response = "No properties match your criteria. Try adjusting your search."

        return jsonify({'response': response})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'response': "Sorry, I encountered an error processing your request."})

if __name__ == '__main__':
    app.run(debug=True)
