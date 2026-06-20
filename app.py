from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

API_KEY = "27bf7c1eabbec193a265e70d5b80f468"

search_history = []


@app.route("/", methods=["GET", "POST"])
def home():

    global search_history

    weather = None
    forecast = []
    error = None

    if request.method == "POST":

        city = request.form["city"]

        print("City Search:", city)

        if city and city not in search_history:
            search_history.append(city)

        if len(search_history) > 5:
            search_history.pop(0)

        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

        weather_response = requests.get(weather_url)
        forecast_response = requests.get(forecast_url)

        data = weather_response.json()
        forecast_data = forecast_response.json()

        print(data)

        if str(data.get("cod")) == "200":

            weather = {
                "city": data["name"],
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "wind": data["wind"]["speed"],
                "condition": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"]
            }

            if "list" in forecast_data:

                for item in forecast_data["list"][:5]:

                    forecast.append({
                        "temp": item["main"]["temp"],
                        "icon": item["weather"][0]["icon"],
                        "date": item["dt_txt"]
                    })

        else:
            error = "❌ City not found. Please enter a valid city name."

    return render_template(
        "index.html",
        weather=weather,
        forecast=forecast,
        error=error,
        history=search_history
    )


@app.route("/clear-history")
def clear_history():

    global search_history

    search_history.clear()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)