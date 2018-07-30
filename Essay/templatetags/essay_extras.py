from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@stringfilter
def essay_format(value):
    """Formats the essay content to the proper layout"""
    tokens = value.split("\n")
    formatted_value = ""
    for token in tokens:
        token = "<p>" + token + "</p>"
        formatted_value = formatted_value + token
    return formatted_value

register.filter('essay_format', essay_format)