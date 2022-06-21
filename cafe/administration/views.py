from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .models import Place, Restaurant
from .serializers import PlaceSerializer, RestaurantSerializer


class ListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    pass


class DetailView(generics.RetrieveUpdateDestroyAPIView):
    pass


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
