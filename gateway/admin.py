from django.contrib import admin
from gateway.models import Api, Service
# Register your models here.


@admin.register(Api)
class ApiAdmin(admin.ModelAdmin):
    pass


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass