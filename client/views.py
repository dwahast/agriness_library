# from django.shortcuts import render
from django.utils import timezone
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

    @action(methods=["GET"], detail=False, url_path='')
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        for reserved_book in queryset.all():
            print(f"Dias de aluguel {reserved_book.book.name}: {(timezone.now() - reserved_book.reservation_date).days}")

            if timezone.now() > reserved_book.reservation_date + timezone.timedelta(days=7):

                delta = timezone.now() - reserved_book.reservation_date
                print(f"Em atraso {delta.days} dias!")
                if delta.days <= 3:
                    """Até 3 dias 3% 0.2%"""
                    new_fee = reserved_book.book.value * 0.03 + delta.days * (0.002 * reserved_book.book.value)
                    print(f"Taxa de atraso. Até 3 dias (3% 0.2%):{new_fee}")
                    reserved_book.fees = new_fee
                    reserved_book.save()

                elif 3 < delta.days <= 5:
                    """Acima 3 dias 5% 0.4%"""
                    new_fee = reserved_book.book.value * 0.05 + delta.days * (0.002 * reserved_book.book.value)
                    print(f"Taxa de atraso. Acima 3 dias (5% 0.4%):{new_fee}")
                    reserved_book.fees = new_fee
                    reserved_book.save()

                elif delta.days > 5:
                    """Acima 5 dias 7% 0.6%"""
                    new_fee = reserved_book.book.value * 0.07 + delta.days * (0.006 * reserved_book.book.value)
                    print(f"Taxa de atraso. Acima 5 dias (7% 0.6%):{new_fee}")
                    reserved_book.fees = new_fee
                    reserved_book.save()
            else:
                print("Sem atraso!")

        return queryset

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
