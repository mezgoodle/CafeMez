from rest_framework import response, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from django.http import Http404
from loguru import logger

from .models import Place, Restaurant, User, Referral, Item, Category, SubCategory
from .serializers import (PlaceSerializer,
                          RestaurantSerializer,
                          UserSerializer,
                          ReferralSerializer,
                          ItemSerializer,
                          CategorySerializer,
                          SubCategorySerializer)
from .utils import set_permissions


class BaseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        # logger.info(f'Get list of objects; {request=}; {args=}; {kwargs=}')
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        # logger.info(f'Create object; {request=}; {args=}; {kwargs=}')
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        # logger.info(f'Get object; {request=}; {args=}; {kwargs=}')
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # logger.info(f'Update object; {request=}; {args=}; {kwargs=}')
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        # logger.info(f'Update object partial; {request=}; {args=}; {kwargs=}')
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # logger.info(f'Delete object; {request=}; {args=}; {kwargs=}')
        return super().destroy(request, *args, **kwargs)


class PlaceViewSet(BaseViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'code'


class SubCategoryViewSet(BaseViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class ItemViewSet(BaseViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def create(self, request, *args, **kwargs):
        item = Item(name=request.data['name'], price=request.data['price'], description=request.data['description'],
                    photo=request.data['photo'], subcategory=SubCategory.objects.get(code=request.data['subcategory']))
        item.save()
        serializer = ItemSerializer(item)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_items(request, subcategory_code):
    items = Item.objects.filter(subcategory=subcategory_code)
    serializer = ItemSerializer(items, many=True)
    return response.Response(serializer.data)


@api_view(['GET'])
def places_by_restaurant(request, restaurant_name):
    try:
        restaurant = Restaurant.objects.get(name=restaurant_name)
    except Restaurant.DoesNotExist:
        logger.error(f'Restaurant {restaurant_name} does not exist')
        raise Http404

    logger.info(f'Get places by restaurant; {request=}; {restaurant_name=}')
    places = restaurant.place_set.all()
    serializer = PlaceSerializer(places, many=True)
    return response.Response(serializer.data)


@api_view(['GET'])
def subcategories_by_category(request, category_code: str):
    try:
        category = Category.objects.get(code=category_code)
    except Category.DoesNotExist:
        logger.error(f'Category {category_code} does not exist')
        raise Http404

    logger.info(f'Get subcategories by category; {request=}; {category_code=}')
    subcategories = category.subcategory_set.all()
    serializer = SubCategorySerializer(subcategories, many=True)
    return response.Response(serializer.data)


class RestaurantViewSet(BaseViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class ReferralViewSet(BaseViewSet):
    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer


class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def create(self, request, *args, **kwargs):
        logger.info(f'Create user; {request=}; {request.data=}')
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])
            set_permissions(user)
            user.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
