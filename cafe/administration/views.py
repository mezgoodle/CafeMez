from rest_framework import generics

from .models import Place
from .serializers import PlaceSerializer


class ListView(generics.ListCreateAPIView):
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
