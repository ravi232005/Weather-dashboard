from flask import Flask, render_template, request, flash
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For flashing messages

# OpenWeatherMap API endpoint and key
API_KEY = 'd609a6c1d1758a709a9c3bfdc73640a3'  # Replace with your OpenWeatherMap API key
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = []
    if request.method == "POST":
        cities = request.form["city"].split(',')
        for city in cities:
            city = city.strip()  # Clean up any extra spaces
            url = f"{BASE_URL}?q={city}&units=metric&appid={API_KEY}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                weather_data.append({
                    "city": city,
                    "temp": data["main"]["temp"],
                    "weather": data["weather"][0]["description"],
                    "icon": data["weather"][0]["icon"],
                    "humidity": data["main"]["humidity"],
                    "pressure": data["main"]["pressure"],
                    "wind_speed": data["wind"]["speed"],
                    "lat": data["coord"]["lat"],
                    "lon": data["coord"]["lon"],
                    "air_quality": "Good",  # Static for now
                    "uv_index": "Moderate",  # Static for now
                })
            else:
                flash(f"Error fetching data for {city}: {response.status_code} - {response.reason}", 'error')

    return render_template("dashboard.html", weather_data=weather_data)


if __name__ == "__main__":
    app.run(debug=True)
