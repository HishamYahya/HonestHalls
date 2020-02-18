from django.contrib import messages


def render_form_errors(request, form):
    """ Uses Django messages to render the errors from the form. """
    for field, errors in form.errors.items():
        for error in errors:
            messages.error(request, error)
