import copy

a = {
    "step1.resp": {
        "data": {
            "data": {
                "data": {
                    "day": [
                        {
                            "count": 52,
                            "cardinality_primeID": 37,
                            "time_fm": "2021-06-01"
                        },
                        {
                            "count": 167,
                            "cardinality_primeID": 42,
                            "time_fm": "2021-06-02"
                        },
                        {
                            "count": 181,
                            "cardinality_primeID": 42,
                            "time_fm": "2021-06-03"
                        },
                        {
                            "count": 109,
                            "cardinality_primeID": 41,
                            "time_fm": "2021-06-04"
                        }
                    ]
                },
                "result": "success"
            }
        },
        "scripts": []
    },
    "step2.resp": {
        "data": {
            "data": {
                "data": [
                    {
                        "activityPercent": 0,
                        "areaID": "豫园街道",
                        "activityDeviceNum": "0",
                        "day": "2021-05-18",
                        "totalDeviceNum": "4"
                    },
                    {
                        "activityPercent": 0.25,
                        "areaID": "豫园街道",
                        "activityDeviceNum": "1",
                        "day": "2021-05-19",
                        "totalDeviceNum": "4"
                    },
                    {
                        "activityPercent": 0.75,
                        "areaID": "豫园街道",
                        "activityDeviceNum": "3",
                        "day": "2021-05-20",
                        "totalDeviceNum": "4"
                    }
                ],
                "result": "success"
            }
        },
        "scripts": []
    }
}


# 简化结果
def easy_resp(resp_data):
    for key, i in resp_data.items():
        if isinstance(i, list):
            # 把列表对象进行简化
            resp_data[key] = [i[0]] if len(i) else []
            for j in i:
                if isinstance(j, dict):
                    easy_resp(j)
            continue
        if isinstance(i, dict):
            easy_resp(i)
    return resp_data


# 组装结果
def format_resp(parent_key, index, resp_data, filed_list):
    res = []
    for key, i in resp_data.items():
        filed = (parent_key + "||" + key) if parent_key else key
        field_type = "str"
        if isinstance(i, dict):
            field_type = "dict"
        elif isinstance(i, list):
            field_type = "list"
            # 统计列表长度，方便后续组装时，针对该字段的循环次数
            filed_list[filed] = len(i)
        now_res = dict(
            id=index,
            label=key,
            filed=filed,
            filed_name=key,
            field_type=field_type
        )
        index += 1
        if isinstance(i, dict):
            index, now_res["children"], filed_list = format_resp(filed, index, i, filed_list)
        if isinstance(i, list):
            if len(i):
                index, now_res["children"], filed_list = format_resp(filed, index, i[0], filed_list)
        res.append(now_res)
    return index, res, filed_list


def main(a):
    e = format_resp("", 1, a, {})
    print(e[2])
    c = easy_resp(a)
    print(c)
    d = format_resp("", 1, c, {})
    print(d[1])
    return ""


if __name__ == '__main__':
    print(main(a))
