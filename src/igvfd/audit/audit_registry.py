AUDIT_FUNCTIONS = {}


def register_audit(object_types, frame):
    def decorator(function):
        for object_type in object_types:
            key = (object_type, frame)
            AUDIT_FUNCTIONS.setdefault(key, []).append(function)
        return function
    return decorator


def run_audits(value, system, frame):
    seen_functions = set()
    if frame == 'object?skip_calculated=true':
        object_types = system.get('types')
    else:
        object_types = value['@type']
    for object_type in object_types:
        key = (object_type, frame)
        for function in AUDIT_FUNCTIONS.get(key, []):
            if function not in seen_functions:
                seen_functions.add(function)
                yield from function(value, system)
