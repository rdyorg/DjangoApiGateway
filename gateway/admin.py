from django.contrib import admin
from gateway.models import Api, Server, Step, Arrangement, Router, Gateway, StepApi


@admin.register(Api)
class ApiAdmin(admin.ModelAdmin):
    pass


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    pass


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    pass


@admin.register(StepApi)
class StepApiAdmin(admin.ModelAdmin):
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
