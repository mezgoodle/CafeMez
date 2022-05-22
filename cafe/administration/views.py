from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Place
from .serializers import PlaceSerializer


@api_view(['GET'])
def places_lists(request):
    places = PlaceSerializer(Place.objects.all(), many=True)
    return Response(places.data)
