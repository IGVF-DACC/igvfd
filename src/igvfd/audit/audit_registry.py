import re
import json

# === Dispatcher Registry ===
AUDIT_FUNCTIONS = {}


def register_audit(object_types, frame='object'):
    def decorator(function):
        for object_type in object_types:
            key = (object_type, frame)
            AUDIT_FUNCTIONS.setdefault(key, []).append(function)
        return function
    return decorator


def run_audits(value, system, frame='object'):
    object_type = value['@type'][0]
    key = (object_type, frame)
    audit_functions = AUDIT_FUNCTIONS.get(key, [])
    for function in audit_functions:
        yield from function(value, system)
