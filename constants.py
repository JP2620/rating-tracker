import json

try:
    with open('conf.json', 'r') as f:
        config = json.load(f)
except Exception as e:
    print(e.with_traceback())
    exit()

W_WIDTH = config["resolution"]["width"]
W_HEIGHT = config["resolution"]["height"]
MULTIPLICADORES = config["multipliers"]
DIFF_RATINGS = config["rating_deltas"]
PTS_GANA_MEJOR = config["points_better_wins"]
PTS_GANA_PEOR = config["points_worse_wins"]