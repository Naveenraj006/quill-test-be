from flask import Flask, request, jsonify
import requests
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
# Configure logging (replace with your desired configuration)
app.logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)


API_KEY = '61b45d4766f913b47cbdf210b056525a' 

@app.route("/weather")
def get_weather():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "Latitude and longitude are required parameters"}), 400

    # Construct the URL with hidden API key
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={API_KEY}"
    app.logger.debug(f"Fetching weather data from {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for unsuccessful requests
        return jsonify(response.json())
    except requests.RequestException as e:
        app.logger.error(f"Error fetching weather data: {e}")
        return jsonify({"error": "Failed to retrieve weather data"}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

