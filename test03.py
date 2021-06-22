# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : Friday
# @FILE     : test03.py
# @Time     : 2021/6/22 16:07
# @Software : PyCharm
import time

import pydash as pydash

import pydash

old_data = {
    "step1.resp": {
        "data": {
            "aggResults": {
                "openTS.day": [
                    {
                        "count": 1,
                        "time_fm": "2021-06-07"
                    },
                    {
                        "count": 1,
                        "time_fm": "2021-06-08"
                    },
                    {
                        "count": 1,
                        "time_fm": "2021-06-16"
                    },
                    {
                        "count": 1,
                        "time_fm": "2021-06-17"
                    }
                ]
            },
            "class": [
                {
                    "name": "张",
                    "num": "101",
                    "stu_list": [
                        {"name": "我333问问", "age": 3330},
                        {"name": "我问问", "age": 3330},
                        {"name": "我问问", "age": 30}
                    ]
                },
                {
                    "name": "张",
                    "num": "101",
                    "stu_list": [
                        {"name": "我问问", "age": 30},
                        {"name": "我问问", "age": 30},
                        {"name": "我问问", "age": 30}
                    ]
                },
                {
                    "name": "张",
                    "num": "101",
                    "stu_list": [
                        {"name": "我问问", "age": 30},
                        {"name": "我问问", "age": 30},
                        {"name": "我问问", "age": 30}
                    ]
                }
            ],
            "total": 4
        },
        "result": "success"
    },
    "step2.resp": {
        "data": {
            "numHits": 4,
            "messages": [],
            "aggResults": {
                "simple.messageType": [
                    {
                        "count": 3,
                        "messageType": "ProtectiveBuildingShakeDetection"
                    },
                    {
                        "count": 1,
                        "messageType": "inclinometer"
                    }
                ]
            }
        },
        "result": "success"
    }
}
# todo: 要求，如果是列表元素的重组，必须要保证新列表结构内的元素本来就是在同一个列表内


ee = [
    {
        "id": 3,
        "label": "aggResults",
        "filed": "step1.resp||data||aggResults",
        "field_type": "dict",
        "children": [
            {
                "id": 4,
                "label": "openTS.day",
                "filed": "step1.resp||data||aggResults||openTS.day",
                "field_type": "list",
                "children": [
                    {
                        "id": 5,
                        "label": "count",
                        "filed": "step1.resp||data||aggResults||openTS.day||count",
                        "field_type": "str"
                    },
                    {
                        "id": 6,
                        "label": "time_fm",
                        "filed": "step1.resp||data||aggResults||openTS.day||time_fm",
                        "field_type": "str"
                    }
                ]
            }
        ]
    }
]


def get_rrr(res, ee):
    for j in ee:
        lins = []
        if j["field_type"] == "list":
            for i in j["children"]:
                ddd = get_s(i["label"], i["filed"])
                lins.append(ddd)
        elif j["field_type"] == "dict":
            res[j["label"]] = get_rrr({}, j["children"])
        res[j["label"]] = lins
    return res


filed_dict = {
    'step1.resp||data||aggResults||openTS.day': 4,
    'step1.resp||data||class': 3,
    'step1.resp||data||class||stu_list': 3,
    'step2.resp||data||messages': 0,
    'step2.resp||data||aggResults||simple.messageType': 2}


def get_resp():
    result = {}
    for i in ee:
        if i.get("children"):
            pass
        else:
            result[i["label"]] = ""
    return result


# step1.resp||data||class||stu_list||name

def get_get_list(lins_str, get_list):
    # 说明当前结果是一个列表值，需要对列表值长度进行循环
    if get_list:
        new_list = []
        for i in get_list:
            field = lins_str.split("||")[-1]
            for j in range(filed_dict[lins_str]):
                new_list.append(i + "||" + field + "||" + str(j))
        get_list = new_list
    else:
        for j in range(filed_dict[lins_str]):
            get_list.append(lins_str + "||" + str(j))
    return get_list


def get_field_data(old_data, filed):
    filed_list = filed.split("||")
    lins_str = filed_list[0]
    get_list = []
    for i in range(len(filed_list)):
        if i != len(filed_list) - 1:
            if i != 0:
                lins_str = lins_str + "||" + filed_list[i]
            if lins_str in filed_dict:
                get_list = get_get_list(lins_str, get_list)
    res = [i + "||" + filed_list[-1] for i in get_list]
    print(res)
    # pydash.get(old_data, ['step1.resp', 'data', 'class', 0, 'stu_list', 0, 'name'])
    return res


def get_dash(field):
    field_list = field.split("||")
    return pydash.get(old_data, field_list)


# 计算时间函数
def print_run_time(func):
    def wrapper(*args, **kw):
        local_time = time.time()
        func(*args, **kw)
        print('current Function [%s] run time is %.2f' % (func.__name__, time.time() - local_time))

    return wrapper


# @print_run_time
def get_s(label, filed):
    new_res = []
    res = get_field_data(old_data, filed)
    for i in res:
        new_res.append(
            {label: get_dash(i)}
        )
    return new_res


if __name__ == '__main__':
    print(get_rrr({}, ee))
