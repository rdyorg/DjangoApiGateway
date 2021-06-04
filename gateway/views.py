from django.http import JsonResponse

import logging
from gateway.models import Router, Step
import requests
from operator import methodcaller

logger = logging.getLogger(__name__)


def router_page(request, path='/'):
    # 根据当前路径获取路由对象，关联查询api或者step编排
    router_instance = Router.objects.select_related(
        "arrangement").select_related("api__server").get(path="/" + path)
    # 获取关联数据对象
    if router_instance.api:
        api_instance = router_instance.api
        service_instance = router_instance.api.server
        to_url = api_instance.protocol + "://" + service_instance.instances + api_instance.path
        res_data = methodcaller(api_instance.method.lower(), url=to_url)(requests).json()
    if router_instance.arrangement:
        arrangement_instance = router_instance.arrangement
        # 获取当前编排下的所有步骤数据
        res_data = []
        step_queryset = Step.objects.prefetch_related(
            "api__server"
        ).filter(arrangement=arrangement_instance)
        for step_instance in step_queryset:
            api_instance = step_instance.api
            service_instance = step_instance.api.server
            to_url = api_instance.protocol + "://" + service_instance.instances + api_instance.path
            res_data.append(methodcaller(api_instance.method.lower(), url=to_url)(requests).json())
    return JsonResponse({"data": res_data})
