a = {
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
        "total": 4
    },
    "result": "success"
}


# 简化结果
def easy_resp(a):
    for key, i in a.items():
        if isinstance(i, list):
            a[key] = [i[0]] if len(i) else []
            continue
        if isinstance(i, dict):
            easy_resp(i)
    return a


# 组装结果
def format_resp(index, a):
    res = []
    for key, i in a.items():
        now_res = dict(
            id=index,
            label="{}  --  {}  --  {}".format(key, index, key),
        )
        index += 1
        if isinstance(i, dict):
            index, now_res["children"] = format_resp(index, i)
        if isinstance(i, list):
            if len(i):
                index, now_res["children"] = format_resp(index, i[0])
        res.append(now_res)
    return index, res

def main(a):
    c = easy_resp(a)
    print(c)
    print(format_resp(1, c)[1])

b = {
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

if __name__ == '__main__':
    main(a)
    main(b)