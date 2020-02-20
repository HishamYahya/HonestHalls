from django import template

register=template.Library()


@register.filter(name='convert_to_int')
def convert_to_int(value):
	num = int(value)
	return num
