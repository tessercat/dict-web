""" Models module. """
from django.db import models


class Entry(models.Model):
    """ A Dictionary entry. """

    class Meta:
        """ Meta vars. """
        # pylint: disable=too-few-public-methods
        verbose_name_plural = "entries"

    char = models.CharField(
        primary_key=True,
        max_length=1,
    )
    definitions = models.TextField(
        max_length=10000,
    )
    pinyin = models.CharField(
        max_length=12
    )

    def __str__(self):
        return self.char
