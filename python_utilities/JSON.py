import json
import pandas as pd


def loadJSONFromFile(fileName: str):
    try:
        obj = json.load(fileName)
        return obj
    except ValueError:
        return None


def toJSON(obj) -> str:
    return json.dumps(obj)


def fromJSON(json_str: str):
    return json.loads(json_str) if isValidJSON(json_str) else None


def isValidJSON(json_str: str) -> bool:
    try:
        json.loads(json_str)
    except ValueError:
        return False
    return True


def jsonToDataFrame(data, column):
    df = pd.DataFrame.from_records(data)

    rows = []
    for index, row in df[column].iteritems():
        for item in row:
            rows.append(item)
    df = pd.DataFrame(rows)
    return df
