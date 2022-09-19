from .exceptions import *
import json
from .constants import *

def validate_schema(params, required_key=['name'],msg=""):
    keys = params.keys()
    key_len = 0
    for key in required_key:
        if key in keys:
            key_len += 1
        if not key:
            raise ValidationError(REQUIRED_KEY_ERROR)

    if len(required_key) != key_len:
        raise ValidationError(INVALID_DATA+msg)

def is_json(myjson):
		try:
			json.loads(myjson)
		except ValueError as e:
			return False
		return True