import json
import traceback
from typing import Dict, List
try:
    with open('conf.json', 'r') as f:
        config = json.load(f)
except Exception as e:
    print(traceback.format_exc())
    exit()

W_WIDTH: int = config["resolution"]["width"]
W_HEIGHT: int = config["resolution"]["height"]
MULTIPLICADORES: Dict[str, float] = config["multipliers"]
DIFF_RATINGS: List[int]  = config["rating_deltas"]
PTS_GANA_MEJOR: List[int] = config["points_better_wins"]
PTS_GANA_PEOR: List[int] = config["points_worse_wins"]