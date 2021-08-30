# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from client.models import Client, Book, Reserve
from client.serializer import ClientSerializer, BookSerializer, ReserveSerializer
from rest_framework_extensions.mixins import NestedViewSetMixin


# Create your views here.
class ClientViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    model = Client
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class BookViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    model = Book
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ReserveViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    model = Reserve
    queryset = Reserve.objects.all()
    serializer_class = ReserveSerializer
    # @action(detail=True)
    # def books(self, request, pk=None):
    #     """
    #     Returns a list of all the group names that the given
    #     user belongs to.
    #     """
    #     books = Client.objects.filter(id=pk)
    #     # serializer = self.get_serializer(books, many=True)
    #     serializer = self.get_serializer(books)
    #     return Response(serializer.data)

