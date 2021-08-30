from django.contrib import admin
from client.models import Client, Book, Reserve


class Clients(admin.ModelAdmin):
    list_display = ('id', 'name', 'doc_id')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


class Books(admin.ModelAdmin):
    list_display = ('id', 'name', 'reserved')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'reserved')


class Reserves(admin.ModelAdmin):
    list_display = ('id', 'client_id', 'book_id', 'client_name', 'book_name', 'reservation_date', 'return_date', 'fees')
    list_display_links = ('id', 'client_id', 'book_id')
    search_fields = ('id',)


admin.site.register(Client, Clients)
admin.site.register(Book, Books)
admin.site.register(Reserve, Reserves)
