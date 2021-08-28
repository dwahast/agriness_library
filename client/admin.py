from django.contrib import admin
from client.models import Client


# Register your models here.
class Clients(admin.ModelAdmin):
    list_display = ('id', 'name', 'doc_id')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


admin.site.register(Client, Clients)
