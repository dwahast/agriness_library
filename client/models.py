from django.db import models
from django.utils import timezone


class Client(models.Model):
    name = models.CharField(max_length=50)
    doc_id = models.CharField(max_length=12)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=20)
    reserved = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Reserve(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, models.CASCADE)
    client_name = models.CharField(default=client.name, blank=True, null=True, max_length=50)
    book_name = models.CharField(default=book.name, blank=True, null=True, max_length=20)
    reservation_date = models.DateTimeField(default=timezone.now, verbose_name='date reserved')
    return_date = models.DateTimeField(blank=True, null=True, verbose_name='date returned')

    def __str__(self):
        return self.client.name + " - " + self.book.name

