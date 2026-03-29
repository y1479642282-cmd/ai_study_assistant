import json
import os

def load_json(file_path):
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []