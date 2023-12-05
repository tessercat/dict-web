""" Custom tags module for the form template. """
from django.template.defaultfilters import register


@register.filter(name="get_entry")
def get_entry(cjk_chars, char):
    """ Return Entry object or raise index error. """
    return cjk_chars[char]
