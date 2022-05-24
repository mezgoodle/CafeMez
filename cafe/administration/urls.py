from django.urls import path

from . import views

urlpatterns = [
    path('places', views.places_lists, name='all_places'),
    path('add_places', views.places_add, name='new_place'),
    path('places/<int:pk>', views.places_detail, name='place_detail'),
]
