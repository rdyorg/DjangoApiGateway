import httpx
import asyncio
import time

async def request(client):
    resp = await client.get('http://39.103.236.234:10001/async/')
    print(resp)


async def main():
    async with httpx.AsyncClient() as client:
        # # 开始
        # start = time.time()

        # 1000 次调用
        task_list = []
        for _ in range(40):
            req = request(client)
            task = asyncio.get_event_loop().create_task(req)
            task_list.append(task)
        await asyncio.gather(*task_list)



if __name__ == "__main__":
    #开始
    start = time.time()
    asyncio.get_event_loop().run_until_complete(main())
    # 结束
    end = time.time()
    print(f'异步：发送1000次请求，耗时：{end - start}')


# 同步调用
# import time
# import httpx
#
#
# def make_request(client):
#     resp = client.get('http://39.103.236.234:10001/async/')
#     print(resp)
#
#
# def main():
#     session = httpx.Client()
#
#     # 1000 次调用
#     for _ in range(40):
#         make_request(session)
#
#
# if __name__ == '__main__':
#     # 开始
#     start = time.time()
#     main()
#     # 结束
#     end = time.time()
#     print(f'同步：发送1000次请求，耗时：{end - start}')
