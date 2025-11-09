import os
import json




player = {
    "path": "Materials/player_transcript.png",
    "atk": 15,
    "hp": 100,
    "height": 150,
    "width": 150,
    "name": "Ionic",
    "speed": 7,
    "atkradius": 150,
}



basepath = os.path.dirname(os.path.abspath(__file__))
jsonpath = os.path.join(basepath, "player.json")

with open(jsonpath, "w", encoding="utf-8") as f:
    json.dump(player, f, ensure_ascii=False, indent=2)