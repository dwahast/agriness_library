# from django.shortcuts import render
from rest_framework import viewsets
from client.models import Client
from client.serializer import ClientSerializer


# Create your views here.
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


