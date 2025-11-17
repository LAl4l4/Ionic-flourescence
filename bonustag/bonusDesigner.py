import os
import json


BONUS_TAGS = {
    1:{
        "tag":"slight attack",
        "type":"atk",
        "value":5
    },
    2:{
        "tag":"moderate attack",
        "type":"atk",
        "value":10
    },
    3:{
        "tag":"major attack",
        "type":"atk",
        "value":15
    },
    4:{
        "tag":"slight health",
        "type":"hp",
        "value":5
    },
    5:{
        "tag":"moderate health",
        "type":"hp",
        "value":10
    },
    6:{
        "tag":"major health",
        "type":"hp",
        "value":15
    },
    7:{
        "tag":"slight speed",
        "type":"spd",
        "value":2
    },
    8:{
        "tag":"moderate speed",
        "type":"spd",
        "value":3
    },
    9:{
        "tag":"major speed",
        "type":"spd",
        "value":4
    }
}

tagsnum = len(BONUS_TAGS)

bonus = {
    "tagsnum": tagsnum,
    "tags": BONUS_TAGS
}

basepath = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(basepath, "bonus.json")
with open(filepath, "w", encoding="utf-8") as f:
    json.dump(bonus, f, ensure_ascii=False, indent=2)
