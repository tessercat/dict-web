""" Config module. """
from django.apps import AppConfig


class DictionaryConfig(AppConfig):
    """ App config. """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dictionary'
