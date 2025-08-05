from functools import wraps
from pyramid.exceptions import HTTPBadRequest
from snosearch.parsers import QueryString


def allowed_types(types):
    def decorator(func):
        @wraps(func)
        def wrapper(context, request):
            qs = QueryString(request)
            type_filters = qs.get_type_filters()
            for type_ in type_filters:
                if type_[1] not in types:
                    raise HTTPBadRequest(
                        explanation=f'{type_[1]} not a valid type for endpoint.'
                    )
            return func(context, request)
        return wrapper
    return decorator
