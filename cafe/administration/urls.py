from django.urls import path

from . import views

urlpatterns = [
    path('places', views.PlaceList.as_view(), name='all_places'),
    path('places/<int:pk>', views.PlaceDetail.as_view(), name='place_detail'),
]
