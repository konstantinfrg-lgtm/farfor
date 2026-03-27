from functools import wraps

from flask import abort
from flask_login import current_user


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return view_func(*args, **kwargs)

    return wrapper


def owner_or_admin_required(resource_getter):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            resource = resource_getter(**kwargs)
            if not resource:
                abort(404)
            if not current_user.is_authenticated:
                abort(403)
            if not (current_user.is_admin or resource.owner_id == current_user.id):
                abort(403)
            return view_func(*args, **kwargs)

        return wrapper

    return decorator
