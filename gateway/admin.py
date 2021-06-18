from django.contrib import admin
from gateway.models import Api, Server, Step, Arrangement, Router, Gateway, StepApi


class BaseAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]


@admin.register(Api)
class ApiAdmin(BaseAdmin):
    pass


@admin.register(Server)
class ServerAdmin(BaseAdmin):
    pass


@admin.register(Step)
class StepAdmin(BaseAdmin):
    pass


@admin.register(StepApi)
class StepApiAdmin(BaseAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]


@admin.register(Arrangement)
class ArrangementAdmin(BaseAdmin):
    pass


@admin.register(Router)
class RouterAdmin(BaseAdmin):
    pass


@admin.register(Gateway)
class GatewayAdmin(BaseAdmin):
    pass
