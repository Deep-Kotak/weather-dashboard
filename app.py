from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "74068c6e6aaad08e5bfc563b94f7910e"

@app.route("/", methods=["GET", "POST"])
def home():

    weather = None
    error = None

    if request.method == "POST":

        city = request.form["city"]

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        response = requests.get(url)

        data = response.json()

        print(data)

        if data.get("cod") == 200:

            weather = {
                "city": data["name"],
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "wind": data["wind"]["speed"],
                "condition": data["weather"][0]["description"],
                "icon": data["weather"][0]["icon"]
            }

        else:
            error = "City not found or API issue."

    return render_template(
        "index.html",
        weather=weather,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)