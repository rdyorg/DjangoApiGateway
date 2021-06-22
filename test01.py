# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# @Author   : Friday
# @FILE     : test01.py
# @Time     : 2021/6/22 10:04
# @Software : PyCharm

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

ee = {
    "id": 0,
    "label": "res.resp",
    "filed": "res.resp",
    "children": [
        {
            "id": 10,
            "label": "stu_list",
            "filed": "step1.resp||data||class||stu_list",
            "field_type": "list",
            "children": [
                {
                    "id": 11,
                    "label": "name",
                    "filed": "step1.resp||data||class||stu_list||name",
                    "field_type": "str"
                }
            ]
        }
    ]
}
# get(ee,'step1.resp.data.class.stu_list[0].name')
format_data = {
    "id": 0,
    "label": "res.resp",
    "filed": "res.resp",
    "children": [
        {
            "id": 19,
            "label": "aggResults",
            "filed": "step2.resp||data||aggResults",
            "field_type": "dict",
            "children": [
                {
                    "id": 20,
                    "label": "simple.messageType",
                    "filed": "step2.resp||data||aggResults||simple.messageType",
                    "field_type": "list",
                    "children": [
                        {
                            "id": 21,
                            "label": "count",
                            "filed": "step2.resp||data||aggResults||simple.messageType||count",
                            "field_type": "str"
                        },
                        {
                            "id": 22,
                            "label": "messageType",
                            "filed": "step2.resp||data||aggResults||simple.messageType||messageType",
                            "field_type": "str"
                        }
                    ]
                }
            ]
        },
        {
            "id": 7,
            "label": "class",
            "filed": "step1.resp||data||class",
            "field_type": "list",
            "children": [
                {
                    "id": 8,
                    "label": "name",
                    "filed": "step1.resp||data||class||name",
                    "field_type": "str"
                },
                {
                    "id": 9,
                    "label": "num",
                    "filed": "step1.resp||data||class||num",
                    "field_type": "str"
                },
                {
                    "id": 10,
                    "label": "stu_list",
                    "filed": "step1.resp||data||class||stu_list",
                    "field_type": "list",
                    "children": [
                        {
                            "id": 11,
                            "label": "name",
                            "filed": "step1.resp||data||class||stu_list||name",
                            "field_type": "str"
                        },
                        {
                            "id": 12,
                            "label": "age",
                            "filed": "step1.resp||data||class||stu_list||age",
                            "field_type": "str"
                        }
                    ]
                }
            ]
        },
        {
            "id": 3,
            "label": "aggResults",
            "filed": "step1.resp||data||aggResults",
            "field_type": "dict",
            "children": []
        }
    ]
}


def get_filed_list():
    filed = "step1.resp||data||class||stu_list||name"
    field_list = filed.split("||")
    return field_list


def get_result(field_list, old_data):
    for i in range(len(field_list)):
        if isinstance(old_data, list):
            break
        old_data = old_data.get(field_list[i])
    return old_data


# def test(old_data):
#     for i in range(len(field_list)):
#         # 如果当前值是列表，则需要取当前列表内的每个对象的值
#         if isinstance(old_data, list):
#             if i == len(field_list) - 1:
#                 lins = test22(old_data, field_list[i])
#                 return lins
#         old_data = old_data.get(field_list[i])
#     return old_data
#
#
# def test22(data_list, name):
#     return [{name: i.get(name)} for i in data_list]
#

c = {
    "aggResults": {
        "simple.messageType": [
            {"count": 3, "messageType": "ProtectiveBuildingShakeDetection"},
            {"count": 1, "messageType": "inclinometer"}
        ]
    }
}

"""
需求：根据format_data的格式，label作为key，filed表示所在位置上取原始数据的值，将old_data数据转换为format格式的数据 
|| 双竖线表示 对象的层级
"""


def get_resp(old_data, now_data):
    res = {}
    for i in now_data:
        if i.get("children"):
            get_resp(old_data, i["children"])
        # 当前结果已经是最底层结果了
        field_list = i["filed"].split("||")
        for j in field_list:
            print(old_data)
            if isinstance(old_data, list):
                break
            old_data = old_data.get(j, {})
        res[i["label"]] = old_data
    return res


ee = [{'stu_list': [{'name': '我问问', 'age': 30}, {'name': '我问问', 'age': 30}, {'name': '我问问', 'age': 30}]},
      {'stu_list': [{'name': '我问问', 'age': 30}, {'name': '我问问', 'age': 30}, {'name': '我问问', 'age': 30}]},
      {'stu_list': [{'name': '我问问', 'age': 30}, {'name': '我问问', 'age': 30}, {'name': '我问问', 'age': 30}]}]

if __name__ == '__main__':
    # c = get_resp(old_data, format_data["children"])
    # print(c)
    # print(test(old_data))
    print(get_result(get_filed_list(), old_data))
