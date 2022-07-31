from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter(trailing_slash=False)  # trailing slash is False for production
router.register(r'places', views.PlaceViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'items', views.ItemViewSet)
router.register(r'restaurants', views.RestaurantViewSet)
router.register(r'referrals', views.ReferralViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'order_items', views.OrderItemViewSet)
router.register(r'subcategories', views.SubCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('places/restaurant/<str:restaurant_name>', views.places_by_restaurant, name='places_by_restaurant'),
    path('items/by/<str:subcategory_code>', views.get_items, name='items_specific'),
    path('subcategories/by/<str:category_code>', views.subcategories_by_category, name='get_subcategories'),
    path('orders/by/<str:username>', views.get_orders, name='get_orders'),
    path('token', obtain_auth_token, name='token'),
]
