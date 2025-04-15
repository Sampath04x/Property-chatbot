# 🏠 Property Finder Chatbot

A simple chatbot built with **Flask** and **NLTK** that helps users search for properties based on natural language input like:

> “2 bedroom house under $300k”

## 💬 Features

- Understands natural language queries
- Filters properties by:
  - Price
  - Bedrooms
  - Type (house, condo, apartment, etc.)
- Returns matching property listings
- Frontend with a chat-style interface

## 🛠️ Technologies Used

- Python + Flask
- HTML/CSS (for frontend)
- NLTK for basic NLP
- JSON for property data
- JavaScript (for AJAX chat interface)

## 🚀 Getting Started

### 1. Clone the repo

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
2. Install dependencies

pip install flask nltk flask-cors
3. Run the app

python app.py
Open your browser and visit:


http://127.0.0.1:5000/

📁 File Structure

├── app.py
├── property_data.json
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── README.md
📦 Example Property Query
“Show me 3 bedroom houses under $400,000”

Bot will return matching listings like:


123 Main St - $350,000 - 3 bed, 2 bath
...
🧠 NLP Basics
Uses:

word_tokenize for tokenizing input

Regex for price & bedroom extraction

Basic keyword detection for property type

✅ To-Do (Ideas)
Add filters for location, bathrooms, amenities

Integrate a database

Improve natural language understanding

Deploy to the web (Render / Heroku / Railway)
