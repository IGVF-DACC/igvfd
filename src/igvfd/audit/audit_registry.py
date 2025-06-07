from snovault.auditor import audit_checker

DISPATCHER_REGISTRY = {}
DISPATCHER_FUNCTIONS = {}


def register_audit(object_types, frame='object'):
    # Decorator to register an audit function for one or more object types and a specific frame.
    def decorator(function):
        for object_type in object_types:
            DISPATCHER_REGISTRY.setdefault((object_type, frame), []).append(function)
        return function
    return decorator


def make_dispatcher(audit_functions):
    # Creates a dispatcher function that yields audit failures from a list of audit functions.
    def dispatcher(value, system):
        for func in audit_functions:
            yield from func(value, system)
    return dispatcher


def register_all_audits():
    # Registers dispatcher functions for all (object_type, frame) audit combinations in the registry.
    # For each set of registered audit functions, this creates a dispatcher function and assigns it
    # to the global namespace using a specific naming pattern (e.g., `audit_FileSet_object_dispatcher`).
    for (object_type, frame), audit_functions in DISPATCHER_REGISTRY.items():
        dispatcher_name = f'audit_{object_type}_{frame}_dispatcher'
        wrapped_dispatcher = audit_checker(object_type, frame=frame)(make_dispatcher(audit_functions))
        DISPATCHER_FUNCTIONS[dispatcher_name] = wrapped_dispatcher
        globals()[dispatcher_name] = wrapped_dispatcher
