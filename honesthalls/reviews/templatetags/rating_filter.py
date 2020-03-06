from django import template


register = template.Library()

# tag finds a review's rating given a review id
@register.filter(name="rating_filter")
def rating_filter(h, key):
    return h[key]

# tag returns True if a user up voted a given review,
# returns False if a user down voted a given review,
# and returns None if user hasn't voted on a review
@register.filter(name="user_rating_filter")
def user_rating_filter(h, key):
	return h.get(key)
