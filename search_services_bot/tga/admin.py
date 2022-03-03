from django.contrib import admin
from .models import TypeOfService, Service, Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'master')
    list_filter = ('master',)


@admin.register(TypeOfService)
class TypeOfServiceAdmin(admin.ModelAdmin):
    ...


@admin.register(Service)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('type_of_service', 'master')
    list_filter = ('type_of_service', 'master')
