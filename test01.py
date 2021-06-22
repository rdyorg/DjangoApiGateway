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
                    "num": "101"
                },
                {
                    "name": "张",
                    "num": "101"
                },
                {
                    "name": "张",
                    "num": "101"
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

format_data = {
    "id": 0,
    "label": "res.resp",
    "filed": "res.resp",
    "children": [
        {
            "id": 2,
            "label": "data",
            "filed": "step1.resp||data",
            "children": [
                {
                    "id": 14,
                    "label": "simple.messageType",
                    "filed": "step2.resp||data||aggResults||simple.messageType",
                    "children": [
                        {
                            "id": 15,
                            "label": "count",
                            "filed": "step2.resp||data||aggResults||simple.messageType||count"
                        },
                        {
                            "id": 16,
                            "label": "messageType",
                            "filed": "step2.resp||data||aggResults||simple.messageType||messageType"
                        }
                    ]
                },
                {
                    "id": 3,
                    "label": "aggResults",
                    "filed": "step1.resp||data||aggResults",
                    "children": [
                        {
                            "id": 4,
                            "label": "openTS.day",
                            "filed": "step1.resp||data||aggResults||openTS.day",
                            "children": [
                                {
                                    "id": 5,
                                    "label": "count",
                                    "filed": "step1.resp||data||aggResults||openTS.day||count"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    ]
}


"""
需求：根据format_data的格式，label作为key，filed表示所在位置上取原始数据的值，将old_data数据转换为format格式的数据 
|| 双竖线表示 对象的层级
"""