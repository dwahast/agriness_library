# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from client.models import Client, Book, Reserve
from client.serializer import ClientSerializer, BookSerializer, ReserveSerializer
from rest_framework_extensions.mixins import NestedViewSetMixin


# Create your views here.
class ClientViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class BookViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ReserveViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Reserve.objects.all()
    serializer_class = ReserveSerializer

    @action(methods=["POST"], detail=True)
    def reserve(self, request, parent_lookup_client, pk):
        """
        Returns a list of all the group names that the given
        user belongs to.
        """
        client = Client.objects.get(id=parent_lookup_client)
        book = Book.objects.get(id=pk)
        if not book.reserved:
            book.reserved = True

            new_reserve = Reserve(client=client, book=book, client_name=client.name, book_name=book.name)
            new_reserve.save()
            book.save()
            return Response(data={"resultCode": 0, "message": f"livro {book.name} reservado com sucesso!"})

        else:
            return Response(status=400, data={"resultCode": 1, "message": f"livro {book.name} já reservado!"})


