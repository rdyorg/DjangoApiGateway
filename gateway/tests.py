import grequests
import time

urls = [
    'https://envprotection.chinadigitalcity.com/service/dust_monitoring/?type=%E5%B7%A5%E5%9C%B0',
    'https://envprotection.chinadigitalcity.com/service/dust_monitoring/',
]
start_time = time.time()
rs = (grequests.get(u) for u in urls)
res = grequests.map(rs)
print(res)
print(time.time() - start_time)