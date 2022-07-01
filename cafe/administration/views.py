from rest_framework import generics, views, response, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.http import Http404

from .models import Place, Restaurant, User
from .serializers import PlaceSerializer, RestaurantSerializer, UserSerializer
from .utils import set_permissions


class ListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]


class DetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]


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
        raise Http404

    places = Place.objects.filter(restaurant=restaurant)
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


class UserList(views.APIView):
    """
    List all users, or create a new user.
    """

    def get(self, request):
        snippets = User.objects.all()
        serializer = UserSerializer(snippets, many=True)
        return response.Response(serializer.data)

    def post(self, request):
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
            raise Http404

    def get(self, request, username):
        user = self.get_object(username)
        serializer = UserSerializer(user)
        return response.Response(serializer.data)

    def put(self, request, username):
        user = self.get_object(username)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        user = self.get_object(username)
        user.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)
