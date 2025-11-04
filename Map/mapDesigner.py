import json
import os

mapbase = [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 2, 2, 2, 2, 2],
    [1, 2, 2, 2, 2, 1, 1],
    [1, 2, 2, 2, 2, 1, 1],
    [1, 1, 2, 2, 2, 2, 2]
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
        "walkable": False,
        "upThroughable": False
        }
}

MAP_INFO = {
    "height": len(mapbase) * 150,
    "width": len(mapbase[0]) * 150,
    "tilesize": 150
}

playerSpawn = {
    "x": 200,
    "y": 200
}

enemy = [
    {"id": 1, "spawn": (30, 50), "delay": 0},
    {"id": 1, "spawn": (80, 100), "delay": 0},
    {"id": 1, "spawn": (1000, 2000), "delay": 0}
]
    

ENEMY_INFO = {
    1: {
        "id": 1,
        "type": "normal",
        "hp": 100,
        "atk": 10,
        "speed": 5,
        "path": "",
        "width": 30,
        "height": 60, #How many times it should spawn after game start
        "path": "Materials/diren1.png"
    }
}

mapName = "start_cave"

gameMap = [[TILE_INFO[tile] for tile in row] for row in mapbase]

#下方为json打包

mapData = {
    "name": mapName,
    "playerSpawn": playerSpawn,
    "enemy": enemy,
    "enemy_info": ENEMY_INFO,
    "tile_info": TILE_INFO,
    "map_info": MAP_INFO,
    "map": gameMap
}

basepath = os.path.dirname(os.path.abspath(__file__))
filename = f"{mapName}.json"
filepath = os.path.join(basepath, filename)

with open(filepath, "w", encoding="utf-8") as f:
    json.dump(mapData, f, ensure_ascii=False, indent=2)