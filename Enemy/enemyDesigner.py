import os
import json


ENEMY_INFO = {
    1: {
        "id": 1,
        "type": "normal",
        "hp": 100,
        "atk": 10,
        "speed": 5,
        "path": "",
        "width": 150,
        "height": 150, 
        "path": "Materials/diren1.png",
        "atkradius": 150
    }
}

basepath = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(basepath, "enemy.json")
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(ENEMY_INFO, f, ensure_ascii=False, indent=2)
