# main.py
from utils import get_weather

def main():
    print("=== Weather Info ===")
    city = input("Enter city name: ")
    weather = get_weather(city)
    
    if weather:
        for key, value in weather.items():
            print(f"{key}: {value}")
    else:
        print("Error: Could not fetch weather data. Check city name or API key.")

if __name__ == "__main__":
    main()
