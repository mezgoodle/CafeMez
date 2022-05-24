from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Place
from .serializers import PlaceSerializer


@api_view(['GET'])
def places_lists(request):
    places = PlaceSerializer(Place.objects.all(), many=True)
    return Response(places.data)


@api_view(['GET'])
def places_detail(request, pk):
    place = Place.objects.get(pk=pk)
    place = PlaceSerializer(place, many=False)
    return Response(place.data)


@api_view(['POST'])
def places_add(request):
    place = PlaceSerializer(data=request.data)
    if place.is_valid():
        place.save()
        return Response(place.data)
    return Response(place.errors)
