from rest_framework import generics, views, response, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.http import Http404
from loguru import logger

from .models import Place, Restaurant, User, Referral
from .serializers import PlaceSerializer, RestaurantSerializer, UserSerializer, ReferralSerializer
from .utils import set_permissions


class ListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        logger.info(f'Get list of objects; {request=}; {args=}; {kwargs=}')
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logger.info(f'Create object; {request=}; {args=}; {kwargs=}')
        return self.create(request, *args, **kwargs)


class DetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        logger.info(f'Get object; {request=}; {args=}; {kwargs=}')
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        logger.info(f'Update object; {request=}; {args=}; {kwargs=}')
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        logger.info(f'Update object; {request=}; {args=}; {kwargs=}')
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        logger.info(f'Delete object; {request=}; {args=}; {kwargs=}')
        return self.destroy(request, *args, **kwargs)


class PlaceList(ListView):
    def __init__(self):
        super().__init__()
        self.queryset = Place.objects.all()
        self.serializer_class = PlaceSerializer


class PlaceDetail(DetailView):
    def __init__(self):
        super().__init__()
        self.queryset = Place.objects.all()
        self.serializer_class = PlaceSerializer


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


class RestaurantList(ListView):
    def __init__(self):
        super().__init__()
        self.queryset = Restaurant.objects.all()
        self.serializer_class = RestaurantSerializer


class RestaurantDetail(DetailView):
    def __init__(self):
        super().__init__()
        self.queryset = Restaurant.objects.all()
        self.serializer_class = RestaurantSerializer


class ReferralList(ListView):
    def __init__(self):
        super().__init__()
        self.queryset = Referral.objects.all()
        self.serializer_class = ReferralSerializer


class ReferralDetail(DetailView):
    def __init__(self):
        super().__init__()
        self.queryset = Referral.objects.all()
        self.serializer_class = ReferralSerializer


class UserList(views.APIView):
    """
    List all users, or create a new user.
    """

    def get(self, request):
        logger.info(f'Get list of users; {request=}')
        snippets = User.objects.all()
        serializer = UserSerializer(snippets, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        logger.info(f'Create user; {request=}; {request.data=}')
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])
            set_permissions(user)
            user.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(views.APIView):
    """
    Retrieve, update or delete a user instance.
    """

    @staticmethod
    def get_object(username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            logger.error(f'User {username} does not exist')
            raise Http404

    def get(self, request, username):
        logger.info(f'Get user; {request=}; {username=}')
        user = self.get_object(username)
        serializer = UserSerializer(user)
        return response.Response(serializer.data)

    def put(self, request, username):
        logger.info(f'Update user; {request=}; {username=}; {request.data=}')
        user = self.get_object(username)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        logger.info(f'Delete user; {request=}; {username=}')
        user = self.get_object(username)
        user.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
