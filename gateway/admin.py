from django.contrib import admin
from gateway.models import Api, Service, Step, Arrangement, Router, Gateway


# Register your models here.


@admin.register(Api)
class ApiAdmin(admin.ModelAdmin):
    pass


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    pass


@admin.register(Arrangement)
class ArrangementAdmin(admin.ModelAdmin):
    pass


@admin.register(Router)
class RouterAdmin(admin.ModelAdmin):
    pass


@admin.register(Gateway)
class GatewayAdmin(admin.ModelAdmin):
    pass
