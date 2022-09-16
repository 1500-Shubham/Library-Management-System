from .exceptions import *
import json

def validate_schema(params, required_key=['name'],msg=""):
    keys = params.keys()
    key_len = 0
    for key in required_key:
        if key in keys:
            key_len += 1
    if len(required_key) != key_len:
        raise ValidationError("Invalid data"+msg)

def is_json(myjson):
		try:
			json.loads(myjson)
		except ValueError as e:
			return False
		return True