""" URLs module. """
from django.contrib import admin
from django.urls import path
from dictionary import views


urlpatterns = [
    path(
        '',
        views.DictFormView.as_view(),
        name='dict-form'
    ),
    path(
        '/admin/',
        admin.site.urls
    ),
]
