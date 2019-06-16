from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from content_api.models import Item
from content_api.serializers import ItemSerializer

# Create your views here.
class ItemViewSet(viewsets.ModelViewSet):
    queryset=Item.objects.all()
    serializer_class=ItemSerializer

