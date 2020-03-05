from django import template


register = template.Library()

@register.filter(name="rating_filter")
def rating_filter(h, key):
    return h[key]

@register.filter(name="user_rating_filter")
def user_rating_filter(h, key):
	return h.get(key)
