from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('places', views.PlaceList.as_view(), name='all_places'),
    path('places/<int:pk>', views.PlaceDetail.as_view(), name='place_detail'),
    path('places/restaurant/<str:restaurant_name>', views.places_by_restaurant, name='places_by_restaurant'),
    path('restaurants', views.RestaurantList.as_view(), name='all_restaurants'),
    path('restaurants/<int:pk>', views.RestaurantDetail.as_view(), name='restaurant_detail'),
    path('users', views.UserList.as_view(), name='all_users'),
    path('users/<str:username>', views.UserDetail.as_view(), name='user_detail'),
    path('referrals', views.ReferralList.as_view(), name='all_referrals'),
    path('referrals/<int:pk>', views.ReferralDetail.as_view(), name='referral_detail'),
    path('items', views.ItemList.as_view(), name='all_items'),
    path('items/<int:pk>', views.ItemDetail.as_view(), name='item_detail'),
    path('token', obtain_auth_token, name='token'),
]
