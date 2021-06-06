import json

from django.db.models import Prefetch
from django.http import JsonResponse

import logging
from gateway.models import Router, Step, StepApi
import requests
from operator import methodcaller

logger = logging.getLogger(__name__)


def router_page(request, path='/'):
    # 根据当前路径获取路由对象，关联查询api或者step编排
    router_instance = Router.objects.select_related(
        "arrangement").select_related("api__server").get(path="/" + path)
    # 获取关联数据对象
    res_data = []
    if router_instance.api:
        res_data.append(get_request(router_instance))
    if router_instance.arrangement:
        # 路由对应的编排对象
        arrangement_instance = router_instance.arrangement
        # 获取当前编排下的所有步骤数据
        step_queryset = Step.objects.prefetch_related(
            Prefetch("steps", to_attr="step_api_cache")
        ).filter(arrangement=arrangement_instance).order_by("sort")

        for step_instance in step_queryset:
            res_data = []
            for step_api_instance in step_instance.step_api_cache:
                resp = get_request(step_api_instance)
                res_data.append(resp)
    return JsonResponse({"data": res_data})


def get_request(instance):
    # req_data = {
    #     "headers": {},
    #     "args": {},
    #     "data": {},
    #     "script": {}
    # }
    service_instance = instance.api.server
    api_instance = instance.api
    req_params = json.loads(api_instance.involve)
    to_url = api_instance.protocol.lower() + "://" + service_instance.instances + api_instance.path
    print(to_url)
    resp = methodcaller(
        api_instance.method.lower(),
        url=to_url,
        headers=req_params["headers"],
        params=req_params["args"],
        json=req_params["data"]
    )(requests)
    if resp.status_code != 200:
        return
    # 根据配置的出参获取对应的值
    existence = json.loads(api_instance.existence)
    # 获取所有的需要组装的参数
    data_list = []
    for i in existence.get("data", []):
        data_list.append(i["key"])
    """
    {
    "headers": {},
    "data": {
    	[{"name": "统计信息", "key": "count"}]
    	[{"name": "详情地址信息", "key": "data.address"}]
    },
    "script": {}
    }
    """
    resp = resp.json()
    return resp
