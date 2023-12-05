""" URL configuration for project. """
from django.urls import include, path

urlpatterns = [
    path('dictionary', include('dictionary.urls')),
]
