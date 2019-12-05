import json

def error(code, message):
    return json.dumps({ "error" : message }), code