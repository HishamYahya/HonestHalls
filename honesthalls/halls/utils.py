import time
from functools import lru_cache
from django.contrib import messages


def render_form_errors(request, form):
    """ Uses Django messages to render the errors from the form. """
    for field, errors in form.errors.items():
        for error in errors:
            field_label = form.fields[field].label or field
            messages.error(request, field_label + ': ' + error)


def yesno(condition, yes_value, no_value):
    """ Returns yes_value if condition is True, no_value otherwise. """
    return yes_value if condition else no_value


def expiring_lru_cache(expires_in_seconds, *args, **kwargs):
    """
    A custom decorator which builds on top of functools.lru_cache, 
    extending is with the expires_in_seconds parameter. 

    The internal lru_cache is considered dirty when expires_in_seconds 
    seconds have passed. It is then cleared on the following call to the
    function.
    """
    # Construct the lru_cache decorator
    lru_decorator = lru_cache(*args, **kwargs)
    # Define our own decorator
    def decorator(func):
        # Get the cached function from the lru_cache
        cached_func = lru_decorator(func)
        # Set initial clear time
        last_clear = time.time()

        # Create the final wrapped function
        def wrapped_func(*args, **kwargs):
            nonlocal last_clear
            # If more than expires_in_seconds seconds have
            # passed, drop the whole current cache.
            if (time.time() - last_clear) > expires_in_seconds:
                # Cache expired
                cached_func.cache_clear()
                last_clear = time.time()

            # Delegated to the cached instance
            return cached_func(*args, **kwargs)

        return wrapped_func
    return decorator
