from django import template

register=template.Library()

@register.filter(name='divide_filter')
def divide_filter(value):
	ave = ((float(value))/4)
	return (ave)
