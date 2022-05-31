from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, generics

from .models import Place
from .serializers import PlaceSerializer


class PlaceList(generics.ListCreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class PlaceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
