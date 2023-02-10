from flask import Flask, request, jsonify
import requests
import datetime
import os

app = Flask(__name__)

def get_weather(location, date, name):
    API_KEY = "<A>"
    API_URL = f"http://api.weatherapi.com/v1/history.json?key={API_KEY}&q={location}&dt={date}"
    
    response = requests.get(API_URL)
    
    if response.status_code == 200:
        weather_data = response.json()
        return {
            "requester_name": name,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "location": location,
            "date": date,
            "weather": weather_data
        }
    else:
        return {"error": "Failed to retrieve weather data"}

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
@app.route("/")
def home_page():
    return "<p><h2>Weather API"


@app.route(
    "/api"
)
def weather_endpoint():

    if request.form.get("token") is None:
        raise InvalidUsage("token is required", status_code=400)

    token = request.form.get("token")

    if token != os.getenv("API_TOKEN"):
        raise InvalidUsage("wrong API token ", status_code=403)

        exclude = request.form.get("exclude")

    result = get_weather(request.form.get("location"), request.form.get("date"), request.form.get("name"))
    return result
