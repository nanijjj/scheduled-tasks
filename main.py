import requests
from dotenv import load_dotenv
import os

load_dotenv("C:/Users/PCUser/Documents/.env")
api_key = os.getenv("RAIN_API_KEY")



response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params={"lat":49.142693, "lon":9.210879,"appid":api_key,"cnt":4})

response.raise_for_status()
data = response.json()

weather_data = data["list"]

def will_rain(id_codes:list):
    for id_entry in id_codes:
        if id_entry < 700:
            return True
    return False

def telegram_bot_sendtext(bot_message):
    bot_token = os.getenv("RAIN_BOT_TOKEN")
    bot_chatID = '8847528871'
    send_text = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    response = requests.get(send_text,params={"parse_mode": "Markdown","chat_id":bot_chatID,"text":bot_message})

    return response.json()

list_of_codes = []
for entry in weather_data:
    desc = entry["weather"][0]
    id_code = desc["id"]
    list_of_codes.append(id_code)



if will_rain(list_of_codes):
    telegram_bot_sendtext("It's going to rain!")
else:
    telegram_bot_sendtext("It will not rain in the next 12 hours!")


