from django.urls import path

from . import views

urlpatterns = [
    path('places', views.PlaceList.as_view(), name='all_places'),
    path('places/<int:pk>', views.PlaceDetail.as_view(), name='place_detail'),
    path('restaurants', views.RestaurantList.as_view(), name='all_restaurants'),
    path('restaurants/<int:pk>', views.RestaurantDetail.as_view(), name='restaurant_detail'),
]
