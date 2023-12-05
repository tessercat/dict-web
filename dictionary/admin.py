""" Admin module. """
from django.contrib import admin
from dictionary.models import Entry


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    """ Register dictionary Entry. """
    search_fields = (
        'char',
    )
