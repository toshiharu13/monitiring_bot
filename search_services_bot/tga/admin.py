from django.contrib import admin
from .models import TypeOfService, Service, Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    ...


@admin.register(TypeOfService)
class TypeOfServiceAdmin(admin.ModelAdmin):
    ...


@admin.register(Service)
class ClientAdmin(admin.ModelAdmin):
    ...
