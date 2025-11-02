import json
import os

mapbase = [
    [1, 1, 1, 1, 1],
    [1, 1, 2, 2, 2],
    [1, 2, 2, 2, 2]
]

TILE_INFO = {
    1: {"name": "air", "icon": "assets/air.png", "walkable": True},
    2: {"name": "stone", "icon": "assets/stone.png", "walkable": False}
}

gameMap = [[TILE_INFO[tile] for tile in row] for row in mapbase]

basepath = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(basepath, "map.json")

with open(filepath, "w", encoding="utf-8") as f:
    json.dump(gameMap, f, ensure_ascii=False, indent=2)