from django.http import Http404
from loguru import logger
from rest_framework import response, status
from rest_framework.decorators import action, api_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

from .models import (
    Category,
    Item,
    Order,
    OrderItem,
    Place,
    Referral,
    Restaurant,
    SubCategory,
    User,
)
from .permissions import IsAdminOrReadOnly
from .serializers import (
    CategorySerializer,
    ItemSerializer,
    OrderItemSerializer,
    OrderSerializer,
    PlaceSerializer,
    ReferralSerializer,
    RestaurantSerializer,
    SubCategorySerializer,
    UserSerializer,
)
from .utils import set_permissions


class BaseViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        logger.info(f"Get list of objects; {request=}; {args=}; {kwargs=}")
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info(f"Create object; {request=}; {args=}; {kwargs=}")
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Get object; {request=}; {args=}; {kwargs=}")
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info(f"Update object; {request=}; {args=}; {kwargs=}")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        logger.info(f"Update object partial; {request=}; {args=}; {kwargs=}")
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.info(f"Delete object; {request=}; {args=}; {kwargs=}")
        return super().destroy(request, *args, **kwargs)


class PlaceViewSet(BaseViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "code"


class SubCategoryViewSet(BaseViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            subcategory = SubCategory(
                name=request.data["name"],
                code=request.data["code"],
                category=Category.objects.get(code=request.data["category"]),
            )
            subcategory.save()
            serializer = self.serializer_class(subcategory)
            return response.Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return response.Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class OrderViewSet(BaseViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            order = Order(
                user=User.objects.get(username=request.data["user"]),
                shipping_address_name=Restaurant.objects.get(
                    name=request.data["shipping_address_name"]
                ),
                payment_method=request.data["payment_method"],
                shipping_address_longitude=request.data[
                    "shipping_address_longitude"
                ]
                if "shipping_address_longitude" in request.data
                else None,
                shipping_address_latitude=request.data[
                    "shipping_address_latitude"
                ]
                if "shipping_address_latitude" in request.data
                else None,
                shipping_price=request.data["shipping_price"],
            )
            order.save()
            serializer = self.serializer_class(order)
            return response.Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return response.Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=["patch"])
    def finish_order(self, request, pk=None):
        order = self.get_object()
        order.connected_courier = None
        order.is_finished = True
        order.save()
        return response.Response(True)


class OrderItemViewSet(BaseViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            order_item = OrderItem(
                order=Order.objects.get(id=request.data["order"]),
                item=Item.objects.get(name=request.data["item"]),
                quantity=request.data["quantity"],
            )
            order_item.save()
            serializer = self.serializer_class(order_item)
            return response.Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return response.Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=["get"])
    def finished_orders(self, request):
        items = OrderItem.objects.filter(order__is_finished=True)
        serializer = OrderItemSerializer(items, many=True)
        return response.Response(serializer.data)


class ItemViewSet(BaseViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name", "description"]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            item = Item(
                name=request.data["name"],
                price=request.data["price"],
                description=request.data["description"],
                photo=request.data["photo"],
                subcategory=SubCategory.objects.get(
                    code=request.data["subcategory"]
                ),
            )
            item.save()
            serializer = self.serializer_class(item)
            return response.Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return response.Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


# TODO: rewrite functional views into ModelViewSet's actions as possible


@api_view(["GET"])
def get_items(request, subcategory_code):
    items = Item.objects.filter(subcategory=subcategory_code)
    serializer = ItemSerializer(items, many=True)
    return response.Response(serializer.data)


@api_view(["GET"])
def get_orders(request, username):
    user = User.objects.get(username=username)
    orders = None
    if user.is_chef:
        orders = user.connected_restaurant.order_set.all().filter(
            is_ready=False
        )
    elif user.is_courier:
        orders = user.connected_restaurant.order_set.all().filter(
            is_delivered=False, shipping_address_latitude__isnull=False
        )
    elif user.is_staff:
        orders = user.connected_restaurant.order_set.filter(is_finished=False)
    serializer = OrderSerializer(orders, many=True)
    return response.Response(serializer.data)


@api_view(["GET"])
def places_by_restaurant(request, restaurant_name):
    try:
        restaurant = Restaurant.objects.get(name=restaurant_name)
    except Restaurant.DoesNotExist:
        logger.error(f"Restaurant {restaurant_name} does not exist")
        raise Http404

    logger.info(f"Get places by restaurant; {request=}; {restaurant_name=}")
    places = restaurant.place_set.all()
    serializer = PlaceSerializer(places, many=True)
    return response.Response(serializer.data)


@api_view(["GET"])
def subcategories_by_category(request, category_code: str):
    try:
        category = Category.objects.get(code=category_code)
    except Category.DoesNotExist:
        logger.error(f"Category {category_code} does not exist")
        raise Http404

    logger.info(f"Get subcategories by category; {request=}; {category_code=}")
    subcategories = category.subcategory_set.all()
    serializer = SubCategorySerializer(subcategories, many=True)
    return response.Response(serializer.data)


class RestaurantViewSet(BaseViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    lookup_field = "name"


class ReferralViewSet(BaseViewSet):
    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer


class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"

    def create(self, request, *args, **kwargs):
        logger.info(f"Create user; {request=}; {request.data=}")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data["password"])
            set_permissions(user)
            user.save()
            return response.Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return response.Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=["get"])
    def get_order(self, request, username=None):
        user = self.get_object()
        try:
            order = Order.objects.get(connected_courier=user)
        except Order.DoesNotExist:
            raise Http404
        serializer = OrderSerializer(order, many=False)
        return response.Response(serializer.data)

    @action(detail=True, methods=["get"])
    def get_orders(self, request, username=None):
        user = self.get_object()
        orders = user.order_set.filter(is_finished=False)
        serializer = OrderSerializer(orders, many=True)
        return response.Response(serializer.data)

    @action(detail=True, methods=["get"])
    def get_discount(self, request, username=None):
        user = self.get_object()
        if (count := user.referred) != 0:
            return response.Response(count * 0.5)
        if Referral.objects.filter(user_id=user.telegram_id).first():
            return response.Response(2)
        return response.Response(False)

    @action(detail=True, methods=["get"])
    def get_referrer(self, request, username=None):
        user = self.get_object()
        ref = Referral.objects.filter(user_id=user.telegram_id).first()
        return response.Response(
            {
                "username": ref.referrer_id.username,
                "number": ref.referrer_id.referred,
                "activated": ref.activated,
                "id": ref.id,
            }
        )

    @action(detail=False, url_path="get_staff/(?P<restaurant>[^/.]+)")
    def get_staff(self, request, restaurant):
        staff = User.objects.filter(
            is_staff=True, connected_restaurant=restaurant
        )
        chefs = User.objects.filter(
            is_chef=True, connected_restaurant=restaurant
        )
        staff_serializer = self.get_serializer(staff, many=True)
        chefs_serializer = self.get_serializer(chefs, many=True)
        return response.Response(
            {"staff": staff_serializer.data, "chefs": chefs_serializer.data}
        )

    @action(detail=False)
    def get_admins(self, request):
        staff = User.objects.filter(is_staff=True)
        serializer = self.get_serializer(staff, many=True)
        return response.Response(serializer.data)
