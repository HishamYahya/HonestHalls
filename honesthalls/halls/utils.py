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
