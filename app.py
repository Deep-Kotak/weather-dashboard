from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "27bf7c1eabbec193a265e70d5b80f468"

@app.route("/", methods=["GET", "POST"])
def home():

    weather = None
    forecast = []
    error = None

    if request.method == "POST":

        city = request.form["city"]

        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

        weather_response = requests.get(weather_url)
        forecast_response = requests.get(forecast_url)

        data = weather_response.json()
        forecast_data = forecast_response.json()

        if data.get("cod") == 200:

            weather = {
                "city": data["name"],
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "wind": data["wind"]["speed"],
                "condition": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"]
            }

            for item in forecast_data["list"][:5]:

                forecast.append({
                    "temp": item["main"]["temp"],
                    "icon": item["weather"][0]["icon"],
                    "date": item["dt_txt"]
                })

        else:
            error = "City not found or API issue."

    return render_template(
        "index.html",
        weather=weather,
        forecast=forecast,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)