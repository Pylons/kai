"""Solon decorators"""
import logging

import pylons
from decorator import decorator
from pylons.controllers.util import abort

log = logging.getLogger(__name__)

def in_group(group):
    """Requires a user to be logged in, and the group specified"""
    def wrapper(func, *args, **kwargs):
        user = pylons.c.user
        if not user:
            log.debug("No user logged in for permission restricted function")
            abort(401, "Not Authorized")
        if user.in_group(group):
            log.debug("User %s verified in group %s", user, group)
            return func(*args, **kwargs)
        else:
            log.debug("User %s not in group %s", user, group)
            abort(401, "Not Authorized")
    return decorator(wrapper)

@decorator
def logged_in(func, *args, **kwargs):
    if not pylons.c.user:
        abort(401, "Not Authorized")
    else:
        return func(*args, **kwargs)
