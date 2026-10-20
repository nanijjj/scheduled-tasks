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
        antworten.append((datum, stunden))

    # Updates als gelesen markieren, damit sie beim nächsten Lauf nicht nochmal kommen
    if updates:
        requests.get(f"{TG}/getUpdates", params={"offset": updates[-1]["update_id"] + 1})
    return antworten


def trage_ein(datum, stunden):
    r = requests.put(
        f"{PIXEL_ENDPOINT}/{datum}",
        json={"quantity": str(stunden)},
        headers={"X-USER-TOKEN": PIXELA_TOKEN},
    )
    print(datum, stunden, r.text)


def sende(text):
    requests.get(f"{TG}/sendMessage", params={"chat_id": CHAT_ID, "text": text})


for datum, stunden in hole_antworten():
    trage_ein(datum, stunden)

sende("Hey, ein weiterer Tag ist um. Wie viele Stunden hast du gelernt?\n"
      f"Stand: {PIXEL_ENDPOINT}.html")
