from rest_framework import serializers
from client.models import Client, Book, Reserve


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'doc_id']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'value', 'reserved']


class ReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserve
        fields = ['id', 'client', 'book', 'client_name', 'book_name', 'reservation_date', 'return_date', 'fees']
