# import asyncio
# from aiohttp import ClientSession
#
#
# async def fetch(url):
#     async with ClientSession() as session:
#         async with session.get(url) as response:
#             return await response.read()
#
#
# async def run(loop, r):
#     url = "http://39.103.236.234:10003/"
#     tasks = []
#     for i in range(r):
#         task = asyncio.ensure_future(fetch(url.format(i)))
#         tasks.append(task)
#         responses = await asyncio.gather(*tasks)
#         # you now have all response bodies in this variable
#         print(responses)
#
#
# def print_responses(result):
#     print(result)
#
#
# loop = asyncio.get_event_loop()
# future = asyncio.ensure_future(run(loop, 4))
# loop.run_until_complete(future)


import grequests

req_list = [  # 请求列表
    grequests.get('http://39.103.236.234:10003/'),
    grequests.get('http://39.103.236.234:10003/'),
    grequests.get('http://39.103.236.234:10003/'),
]

res_list = grequests.map(req_list)  # 并行发送，等最后一个运行完后返回
for i in res_list:
    print(i.text)
