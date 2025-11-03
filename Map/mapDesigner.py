import json
import os

mapbase = [
    [1, 1, 1, 1, 1],
    [1, 1, 2, 2, 2],
    [1, 2, 2, 2, 2]
]

TILE_INFO = {
    1: {
        "code": 1,
        "name": "back_stone", 
        "path": "Materials/map/Tiles/boxCoin.png", 
        "walkable": False, 
        "upThroughable": False
        },
    2: {
        "code": 2,
        "name": "stone", 
        "path": "Materials/map/Tiles/castleCenter.png", 
        "walkable": True,
        "upThroughable": False
        }
}

playerSpawn = {
    "x": 200,
    "y": 200
}

mapName = "start_cave"

gameMap = [[TILE_INFO[tile] for tile in row] for row in mapbase]

mapData = {
    "name": mapName,
    "playerSpawn": playerSpawn,
    "tile_info": TILE_INFO,
    "map": gameMap
}

basepath = os.path.dirname(os.path.abspath(__file__))
filename = f"{mapName}.json"
filepath = os.path.join(basepath, filename)

with open(filepath, "w", encoding="utf-8") as f:
    json.dump(mapData, f, ensure_ascii=False, indent=2)