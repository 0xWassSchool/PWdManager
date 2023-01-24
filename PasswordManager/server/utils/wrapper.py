import json


def loadJson(json_bytes: bytes, decode: str) -> dict | list:
    return json.loads(json_bytes.decode(decode))


def dumpJson(data: dict, encode: str) -> bytes:
    return bytes(json.dumps(data), encode)
