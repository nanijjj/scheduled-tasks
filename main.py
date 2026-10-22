import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

USERNAME = "keko911"
GRAPH_ID = "graph1"
PIXELA_TOKEN = os.getenv("USER_TOKEN")
BOT_TOKEN = os.getenv("RAIN_BOT_TOKEN")
CHAT_ID = 8847528871
TG = f"https://api.telegram.org/bot{BOT_TOKEN}"
PIXEL_ENDPOINT = f"https://pixe.la/v1/users/{USERNAME}/graphs/{GRAPH_ID}"


def hole_antworten():
    updates = requests.get(f"{TG}/getUpdates").json()["result"]
    antworten = []
    for u in updates:
        msg = u.get("message")
        if not msg or msg["chat"]["id"] != CHAT_ID:
            continue
        text = msg.get("text", "").strip().replace(",", ".")
        try:
            stunden = float(text)
        except ValueError:
            continue  # alles, was keine Zahl ist, ignorieren
        datum = datetime.fromtimestamp(msg["date"], ZoneInfo("Europe/Berlin")).strftime("%Y%m%d")
        antworten.append((datum, stunden,u["update_id"]))


    return antworten


def trage_ein(datum, stunden):
    for _ in range(25):
        r = requests.put(
            f"{PIXEL_ENDPOINT}/{datum}",
            json={"quantity": str(stunden)},
            headers={"X-USER-TOKEN": PIXELA_TOKEN},

        )
        if r.json()["isSuccess"]:
            print(datum, stunden, r.text)
            return True
    return False


def sende(text):
    requests.get(f"{TG}/sendMessage", params={"chat_id": CHAT_ID, "text": text})


for datum, stunden,update_id in hole_antworten():
    if trage_ein(datum, stunden):
        # Updates als gelesen markieren, damit sie beim nächsten Lauf nicht nochmal kommen
        requests.get(f"{TG}/getUpdates", params={"offset": update_id + 1})

sende("Hey, ein weiterer Tag ist um. Wie viele Stunden hast du gelernt?\n"
      f"Stand: {PIXEL_ENDPOINT}.html")
