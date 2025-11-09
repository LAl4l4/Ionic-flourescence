import os
import json


ENTITY_INFO = {
    1: {
        "code":1,
        "name":"exit",
        "uppath":"Materials/map/Tiles/door_closedTop.png",
        "downpath":"Materials/map/Tiles/door_closedMid.png",
        "uppath_unlock":"Materials/map/Tiles/door_openTop.png",
        "downpath_unlock":"Materials/map/Tiles/door_openMid.png"
    }
}

basepath = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(basepath, "entity.json")
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(ENTITY_INFO, f, ensure_ascii=False, indent=2)
