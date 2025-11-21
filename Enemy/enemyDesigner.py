import os
import json


ENEMY_INFO = {
    1: {
        "id": 1,
        "type": "normal",
        "hp": 100,
        "atk": 10,
        "speed": 5,
        "path": "Materials/diren1.png",
        "width": 150,
        "height": 150,
        "atkradius": 150
    },
    2: {
        "id": 2,
        "type": "ghost",
        "hp": 80,
        "atk": 12,
        "speed": 4,
        "width": 51,
        "height": 73,
        "atkradius": 120,
        # explicit multi-sprite paths (relative to basepath)
        "path_active": "Enemy/img/ghost.png",
        "path_normal": "Enemy/img/ghost_normal.png",
        "path_hit": "Enemy/img/ghost_hit.png",
        "path_dead": "Enemy/img/ghost_dead.png"
    }
}

basepath = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(basepath, "enemy.json")
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(ENEMY_INFO, f, ensure_ascii=False, indent=2)
