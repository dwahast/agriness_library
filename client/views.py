# from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from client.models import Client, Book, Reserve
from client.serializer import ClientSerializer, BookSerializer, ReserveSerializer
from rest_framework_extensions.mixins import NestedViewSetMixin

RETURN_LIMIT = 7
# Create your views here.
class ClientViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class BookViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# class ReturnViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
#     queryset = Reserve.objects.all()
#     serializer_class = ReserveSerializer
#     print("\n\nEstoy aka\n\n")
#
#     @action(methods=["PUT"], detail=True)
#     def put(self, request, parent_lookup_client, pk):
#         print("\n\nEstoy aki\n\n")
#         client = Client.objects.get(id=parent_lookup_client)
#         book = Book.objects.get(id=pk)
#         return Response(data={"resultCode": 0, "message": f"livro {book.name} reservado com sucesso!"})


class ReserveViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Reserve.objects.all()
    serializer_class = ReserveSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset()
        for reserved_book in queryset.all():
            print(f"Book: {reserved_book.book.name}")
            print(f"Reserved days: {(timezone.now() - reserved_book.reservation_date).days}")
            print(f"Returned: {reserved_book.return_date is not None}")

            due_date = reserved_book.reservation_date + timezone.timedelta(days=RETURN_LIMIT)
            if timezone.now() > due_date \
                    or reserved_book.return_date is not None:
                print(f"Até: {due_date}")
                delta = timezone.now() - due_date
                print(f"Lateness days: {delta.days}")
                if delta.days <= 3:
                    """Até 3 dias 3% 0.2%"""
                    new_fee = reserved_book.book.value * 0.03 + delta.days * (0.002 * reserved_book.book.value)
                    print(f"Taxa de atraso. Up to 3 days (3% 0.2%):{new_fee}")
                    reserved_book.fees = new_fee
                    reserved_book.save()

                elif 3 < delta.days <= 5:
                    """Acima 3 dias 5% 0.4%"""
                    new_fee = reserved_book.book.value * 0.05 + delta.days * (0.002 * reserved_book.book.value)
                    print(f"Lateness Fees. Higher than 3 days (5% 0.4%):{new_fee}")
                    reserved_book.fees = new_fee
                    reserved_book.save()

                elif delta.days > 5:
                    """Acima 5 dias 7% 0.6%"""
                    new_fee = reserved_book.book.value * 0.07 + delta.days * (0.006 * reserved_book.book.value)
                    print(f"Taxa de atraso. Higher than 5 days (7% 0.6%):{new_fee}")
                    reserved_book.fees = new_fee
                    reserved_book.save()
            else:
                print("Sem atraso!")

        return queryset

    def put(self, request, parent_lookup_id, parent_lookup_book_id):
        print(parent_lookup_id, parent_lookup_book_id)
        queryset = super().get_queryset()
        reserves = queryset.filter(client_id=parent_lookup_id, book_id=parent_lookup_book_id, return_date=None)

        book = Book.objects.get(id=parent_lookup_book_id)
        book.reserved = False
        book.save()

        print(reserves)
        reserve = reserves.first()
        if len(reserves) > 1:
            print("[ERROR] Mais de uma reserva do mesmo livro!")

        if len(reserves) == 0:
            return Response(
                data={
                    "resultCode": 0,
                    "message": f"livro já entregue ou nunca alugado com sucesso!"
                })

        reserve.return_date = timezone.now()
        reserve.save()

        return Response(data={"resultCode": 0, "message": f"livro {reserve.book_name} entregue com sucesso!"})

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
