import requests
import time

# 👇 Your location
latitude = 29.4577801
longitude = -98.438357

# 👇 Your Discord webhook
WEBHOOK_URL = "https://discord.com/api/webhooks/1392235033825120256/pmH0Ouy_LHJ9-27cNSRNP4TL0KUwQHD3EBaRN1pFSismc6z4W7i-6G8JcOxOXq27lCmg"

def get_flag(temp_f):
    if temp_f >= 90:
        return "🚩 Black Flag", "Extreme heat is present (90°F+). Avoid outdoor activity unless mission essential."
    elif temp_f >= 88:
        return "🔴 Red Flag", "High heat risk. Limit outdoor activity. Rest often and hydrate."
    elif temp_f >= 85:
        return "🟡 Yellow Flag", "Moderate heat risk. Use caution. Hydrate frequently."
    elif temp_f >= 82:
        return "🟢 Green Flag", "Mild heat. Standard precautions apply."
    elif temp_f >= 78:
        return "⚪ White Flag", "Very low heat risk."
    else:
        return "❄️ No Flag", "Conditions are cool. No flag needed."

def post_to_discord(title, message):
    data = {
        "username": "🔥 Weather Bot",
        "content": f"**{title} Condition**\n{message}"
    }
    requests.post(WEBHOOK_URL, json=data)

def fetch_temperature():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true&temperature_unit=fahrenheit"
    response = requests.get(url)
    return response.json()["current_weather"]["temperature"]

last_flag = None

while True:
    try:
        temp = fetch_temperature()
        flag, message = get_flag(temp)
        if flag != last_flag:
            post_to_discord(flag, message + f"\nCurrent temp: {temp}°F")
            last_flag = flag
        time.sleep(3600)  # Check every hour
    except Exception as e:
        print("Error:", e)
        time.sleep(300)
