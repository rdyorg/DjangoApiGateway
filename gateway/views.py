import json

from django.db.models import Prefetch
from django.http import JsonResponse

import logging
from gateway.models import Router, Step, StepApi
from operator import methodcaller
import grequests

logger = logging.getLogger(__name__)


def get_request(url_list):
    res = []
    req_list = []
    for i in url_list:
        # 请求方法pop出去
        methods = i.pop("methods")
        existence = i.pop("existence")
        req_list.append(methodcaller(methods, **i)(grequests))
    res_list = grequests.map(req_list)  # 并行发送，等最后一个运行完后返回
    for i in res_list:
        res.append(get_response(json.loads(i.text), existence))
    return res


def get_response(resp, existence):
    return resp


def get_req_url_list(step_instance):
    url_list = []
    for instance in step_instance:
        # 组装步骤下的api对象
        service_instance = instance.api.server
        api_instance = instance.api
        # 请求体和响应体组装
        involve = json.loads(api_instance.involve)
        existence = json.loads(api_instance.existence)
        # 组装请求链接
        to_url = api_instance.protocol.lower() + "://" + service_instance.instances + api_instance.path
        print(to_url)
        url_list.append(dict(
            url=to_url,
            methods=api_instance.method.lower(),
            headers=involve["headers"],
            params=involve["args"],
            json=involve["data"],
            existence=existence
        ))
    return url_list


def router_page(request, path='/'):
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
        # 请求接口
        for step_instance in step_queryset:
            url_list = get_req_url_list(step_instance.step_api_cache)
            res_data.append(
                {step_instance.id: get_request(url_list)}
            )
    return JsonResponse({"data": res_data})


import time


async def main(request):
    import asyncio
    from aiohttp import ClientSession
    import aiohttp

    urls = ['http://39.103.236.234:10003/', 'http://39.103.236.234:10003/']

    async def fetch(session, url):
        async with session.get(url) as response:
            return await response.text()

    async def get(url):
        async with aiohttp.ClientSession() as session:
            html = await fetch(session, url)
            print(html)

    tasks = [get(x) for x in urls]
    print("wwwwww")
    loop = asyncio.get_event_loop()
    print("wwwwww")
    loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()
    return JsonResponse({"data": ""})
