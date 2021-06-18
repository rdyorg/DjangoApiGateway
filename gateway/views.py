import json

from asgiref.sync import sync_to_async
from django.db.models import Prefetch
from django.http import JsonResponse

import logging
from gateway.models import Router, Step, StepApi
import requests
from operator import methodcaller
import grequests

logger = logging.getLogger(__name__)

import aiohttp


async def main(request):
    # res = await async_get_request(urls)
    res = []
    req_list = [  # 请求列表
        grequests.get('http://39.103.236.234:10003/'),
        grequests.get('http://39.103.236.234:10003/'),
        grequests.get('http://39.103.236.234:10003/'),
    ]
    res_list = grequests.map(req_list)  # 并行发送，等最后一个运行完后返回
    for i in res_list:
        print(i.text)
        res.append(i.text)
    return JsonResponse({"data": res})


def sync_main(request):
    # res = await async_get_request(urls)
    res = []
    import grequests
    req_list = [  # 请求列表
        grequests.get('http://39.103.236.234:10003/'),
        grequests.get('http://39.103.236.234:10003/'),
        grequests.get('http://39.103.236.234:10003/'),
    ]
    res_list = grequests.map(req_list)  # 并行发送，等最后一个运行完后返回
    for i in res_list:
        print(i.text)
        res.append(i.text)
    return JsonResponse({"data": res})


async def async_get_request(urls):
    res = []
    async with aiohttp.ClientSession() as session:
        for i in urls:
            async with session.get(i) as response:
                print(await response.text())
                res.append(await response.text())
    return res


@sync_to_async
def _get_router_instance(path):
    try:
        instance = Router.objects.select_related("arrangement").select_related("api__server").get(path=path)
    except Router.DoesNotExist as e:
        return None
    return instance


@sync_to_async
def _get_step_queryset(arrangement_instance):
    return Step.objects.prefetch_related(
        Prefetch("steps", to_attr="step_api_cache")
    ).filter(arrangement=arrangement_instance).order_by("sort")


async def async_router_page(request, path='/'):
    print(path)
    # 根据当前路径获取路由对象，关联查询api或者step编排
    router_instance = await _get_router_instance("/" + path)
    # 获取关联数据对象
    res_data = []
    if router_instance.api:
        res_data.append(get_request(router_instance))
    if router_instance.arrangement:
        # 路由对应的编排对象
        arrangement_instance = router_instance.arrangement
        # 获取当前编排下的所有步骤数据
        step_queryset = await _get_step_queryset(arrangement_instance)
        # 循环每个步骤下的所有api接口
        for step_instance in step_queryset:
            url_list = get_req_url_list(step_instance.step_api_cache)
            print(url_list)
            res_data = get_request(url_list)
            # for step_api_instance in step_instance.step_api_cache:
            #     resp = get_request(step_api_instance)
            #     res_data.append(resp)
    return JsonResponse({"data": res_data})


def get_request(url_list):
    res = []
    req_list = []
    for i in url_list:
        methods = i.pop("methods")
        req_list.append(methodcaller(methods, **i)(grequests))
    res_list = grequests.map(req_list)  # 并行发送，等最后一个运行完后返回
    for i in res_list:
        print(i.text)
        res.append(i.text)
    return res


async def async_request(url_list):
    res = []
    async with aiohttp.ClientSession() as session:
        for i in url_list:
            methods = i.pop("methods")
            async with methodcaller(methods, **i)(session) as response:
                print(await response.text())
                res.append(await response.text())

    return res


def get_req_url_list(step_instance):
    url_list = []
    for instance in step_instance:
        service_instance = instance.api.server
        api_instance = instance.api
        req_params = json.loads(api_instance.involve)
        to_url = api_instance.protocol.lower() + "://" + service_instance.instances + api_instance.path
        url_list.append(dict(
            url=to_url,
            methods=api_instance.method.lower(),
            headers=req_params["headers"],
            params=req_params["args"],
            json=req_params["data"]
        ))
    return url_list


async def async_get_request1(instance):
    service_instance = instance.api.server
    api_instance = instance.api
    req_params = json.loads(api_instance.involve)
    to_url = api_instance.protocol.lower() + "://" + service_instance.instances + api_instance.path
    print(to_url)

    resp = methodcaller(api_instance.method.lower(), url=to_url, headers=req_params["headers"],
                        params=req_params["args"], json=req_params["data"])(requests)
    if resp.status_code != 200:
        return str(resp.status_code)
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


def router_page(request, path='/'):
    print(path)
    # 根据当前路径获取路由对象，关联查询api或者step编排
    router_instance = Router.objects.select_related("arrangement").select_related("api__server").get(path="/" + path)
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
            url_list = get_req_url_list(step_instance.step_api_cache)
            print(url_list)
            res_data = get_request(url_list)
    return JsonResponse({"data": res_data})


#
# def get_request(instance):
#     # req_data = {
#     #     "headers": {},
#     #     "args": {},
#     #     "data": {},
#     #     "script": {}
#     # }
#     service_instance = instance.api.server
#     api_instance = instance.api
#     req_params = json.loads(api_instance.involve)
#     to_url = api_instance.protocol.lower() + "://" + service_instance.instances + api_instance.path
#     print(to_url)
#     resp = methodcaller(
#         api_instance.method.lower(),
#         url=to_url,
#         headers=req_params["headers"],
#         params=req_params["args"],
#         json=req_params["data"]
#     )(requests)
#     if resp.status_code != 200:
#         return str(resp.status_code)
#     # 根据配置的出参获取对应的值
#     existence = json.loads(api_instance.existence)
#     # 获取所有的需要组装的参数
#     data_list = []
#     for i in existence.get("data", []):
#         data_list.append(i["key"])
#     """
#     {
#     "headers": {},
#     "data": {
#     	[{"name": "统计信息", "key": "count"}]
#     	[{"name": "详情地址信息", "key": "data.address"}]
#     },
#     "script": {}
#     }
#     """
#     resp = resp.json()
#     return resp


"""
{
        "headers": {},
        "args": {},
        "data": {},
        "script": {}
    }
"""
