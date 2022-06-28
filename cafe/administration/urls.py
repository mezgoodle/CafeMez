from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('places', views.PlaceList.as_view(), name='all_places'),
    path('places/<int:pk>', views.PlaceDetail.as_view(), name='place_detail'),
    path('restaurants', views.RestaurantList.as_view(), name='all_restaurants'),
    path('restaurants/<int:pk>', views.RestaurantDetail.as_view(), name='restaurant_detail'),
    path('users', views.UserList.as_view(), name='all_users'),
    path('users/<str:username>', views.UserDetail.as_view(), name='user_detail'),
    path('token', obtain_auth_token, name='token'),
]
