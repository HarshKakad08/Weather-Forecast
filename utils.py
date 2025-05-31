import requests
from datetime import datetime
from collections import defaultdict

API_KEY = "1d0c90b647289d84bee8afc709fb3608"

def get_weather(city, units="metric"):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={units}"
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            description = data["weather"][0]["description"].lower()

            alert = ""
            if "rain" in description or "drizzle" in description:
                alert = "🌧️ Don't forget your umbrella!"
            elif "snow" in description:
                alert = "❄️ Stay warm and watch out for slippery roads!"
            elif "clear" in description:
                alert = "☀️ It's sunny! Wear sunscreen and stay hydrated."
            elif "storm" in description or "thunder" in description:
                alert = "🌩️ Stay indoors if possible. Storm alert!"

            return {
                "Temperature": data["main"]["temp"],
                "Humidity": data["main"]["humidity"],
                "Wind Speed": data["wind"]["speed"],
                "Description": description,
                "Alert": alert
            }
        else:
            return None
    except Exception as e:
        print("Error:", e)
        return None

def get_forecast(city, units="metric"):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units={units}"
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            return None

        from collections import OrderedDict
        from datetime import datetime

        day_temp = OrderedDict()
        day_icon = OrderedDict()
        day_full_date = OrderedDict()

        for item in data["list"]:
            dt = datetime.fromtimestamp(item["dt"])
            day = dt.strftime("%a")
            full_date = dt.strftime("%d %b")

            if day not in day_temp:
                day_temp[day] = item["main"]["temp"]
                day_full_date[day] = full_date
                description = item["weather"][0]["description"].lower()

                if "rain" in description:
                    emoji = "🌧️"
                elif "cloud" in description:
                    emoji = "⛅"
                elif "clear" in description:
                    emoji = "☀️"
                elif "snow" in description:
                    emoji = "❄️"
                elif "storm" in description or "thunder" in description:
                    emoji = "🌩️"
                else:
                    emoji = "🌤️"

                day_icon[day] = emoji

            if len(day_temp) == 5:
                break

        return {
            "days": list(day_temp.keys()),
            "temps": list(day_temp.values()),
            "icons": [day_icon[day] for day in day_temp.keys()],
            "full_dates": [day_full_date[day] for day in day_temp.keys()]
        }

    except Exception as e:
        print("Forecast Error:", e)
        return None
