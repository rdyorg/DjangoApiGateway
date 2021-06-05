import asyncio

from django.db.models import Prefetch
from django.http import JsonResponse

import logging
from gateway.models import Router, Step, StepApi
import requests
import grequests
from operator import methodcaller

logger = logging.getLogger(__name__)
import httpx

from django.http import HttpResponse
from asgiref.sync import sync_to_async


async def index(request):
    return HttpResponse("Hello, async Django!")


async def http_call_async(url):
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        print(r)
        return r.json()


async def router_page(request, path='/'):
    urls = [
        'https://envprotection.chinadigitalcity.com/service/dust_monitoring/',
        'https://envprotection.chinadigitalcity.com/service/dust_monitoring/',
    ]
    res_data = []
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    for i in urls:
        asyncio.create_task(http_call_async(i))
    print(asyncio.all_tasks(asyncio.get_event_loop()))

    # 根据当前路径获取路由对象，关联查询api或者step编排
    # router_instance = sync_to_async(
    #     Router.objects.select_related(
    #         "arrangement").select_related("api__server").get(path="/" + path)
    # )
    # # 获取关联数据对象
    # res_data = []
    # if router_instance.api:
    #     api_instance = router_instance.api
    #     service_instance = router_instance.api.server
    #     to_url = api_instance.protocol + "://" + service_instance.instances + api_instance.path
    #     res_data = methodcaller(api_instance.method.lower(), url=to_url)(httpx).json()
    # if router_instance.arrangement:
    #     # 路由对应的编排对象
    #     arrangement_instance = router_instance.arrangement
    #     # 获取当前编排下的所有步骤数据
    #     step_queryset = Step.objects.prefetch_related(
    #         Prefetch("steps", to_attr="step_api_cache")
    #     ).filter(arrangement=arrangement_instance).order_by("sort")
    #
    #     # urls = [
    #     #     'https://envprotection.chinadigitalcity.com/service/dust_monitoring/',
    #     #     'https://envprotection.chinadigitalcity.com/service/dust_monitoring/',
    #     # ]
    #     # rs = (grequests.get(u) for u in urls)
    #     # print(grequests.map(rs))
    #
    #     for step_instance in step_queryset:
    #         req_list = []
    #         for step_api_instance in step_instance.step_api_cache:
    #             service_instance = step_api_instance.api.server
    #             api_instance = step_api_instance.api
    #             to_url = api_instance.protocol.lower() + "://" + service_instance.instances + api_instance.path
    #             print(to_url)
    #             # req_list.append(grequests.get(to_url))
    #             # req_list.append(methodcaller(api_instance.method.lower(), url=to_url)(grequests))
    #         # res_data = grequests.map(req_list)
    #         for i in res_data:
    #             print(i)
    return JsonResponse({"data": ""})
