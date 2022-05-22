from django.urls import path

from . import views

urlpatterns = [
    path('places', views.places_lists, name='all_places'),
]
