import json


def parse(data):
    try:
    
        return json.loads(data.decode())
    except Exception:
        return None