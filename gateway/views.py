import asyncio
import json

import httpx
from asgiref.sync import sync_to_async, async_to_sync
from django.db.models import Prefetch
from django.http import JsonResponse, HttpResponse

import logging
from gateway.models import Router, Step, StepApi
import requests
from operator import methodcaller
import grequests
import time

logger = logging.getLogger(__name__)

urls = [
    'https://envprotection.chinadigitalcity.com/service/dust_monitoring/?type=%E5%B7%A5%E5%9C%B0',
    'https://envprotection.chinadigitalcity.com/service/dust_monitoring/',
]


def test(request):
    urls = [
        'https://envprotection.chinadigitalcity.com/service/dust_monitoring/?type=%E5%B7%A5%E5%9C%B0',
        'https://envprotection.chinadigitalcity.com/service/dust_monitoring/',
    ]
    start_time = time.time()
    rs = [grequests.get(urls[0], callback="get_resp")]
    print(time.time() - start_time)
    print(rs)
    res = async_to_sync(grequests.map(rs))
    print(res)
    # get_blog = sync_to_async(_get_router_queryset, thread_sensitive=True)
    # print(get_blog)
    print(time.time() - start_time)
    return JsonResponse({"data": ""})


def get_resp(r, *args, **kwargs):
    print("2222")
    print(r)


# 异步升级版
async def async_home(request):
    """Display homepage by calling two services asynchronously (proper concurrency)"""
    context = {}
    try:
        async with httpx.AsyncClient() as client:
            # 使用asyncio.gather 并发执行协程
            response_p, response_r = await asyncio.gather(client.get(urls[0]), client.get(urls[1]))
            print(response_p)
            print(response_r)
            if response_p.status_code == httpx.codes.OK:
                context["promo"] = response_p.json()
            if response_r.status_code == httpx.codes.OK:
                context["recco"] = response_r.json()
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}.")
    return HttpResponse(context)


# 异步任务
async def http_call_async():
    async with httpx.AsyncClient() as client:
        r = await client.get(
            'https://envprotection.chinadigitalcity.com/service/dust_monitoring/?type=%E5%B7%A5%E5%9C%B0')
        print(r)
        # r = await client.get(
        #     'https://envprotection.chinadigitalcity.com/service/dust_monitoring/?type=%E5%B7%A5%E5%9C%B0')
        # print(r)


# 异步视图 - 调用异步任务
async def async_view(request):
    loop = asyncio.get_event_loop()
    loop.create_task(http_call_async())
    return HttpResponse("Non-blocking HTTP request")


def _get_router_queryset():
    return Router.objects.all()


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
