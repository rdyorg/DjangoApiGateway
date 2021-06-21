a = {
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
def format_resp(parent_key, index, a):
    res = []
    for key, i in a.items():
        filed = (parent_key + "||" + key) if parent_key else key
        now_res = dict(
            id=index,
            label=key,
            filed=filed
        )
        index += 1
        if isinstance(i, dict):
            index, now_res["children"] = format_resp(filed, index, i)
        if isinstance(i, list):
            if len(i):
                index, now_res["children"] = format_resp(filed, index, i[0])
        res.append(now_res)
    return index, res


def main(a):
    c = easy_resp(a)
    print(c)
    print(format_resp("", 1, c)[1])
    return format_resp("", 1, c)[1]


res = [
    {"id": 1, "label": "step1.resp", "filed": "step1.resp", "children": [
        {"id": 2, "label": "data", "filed": "step1.resp||data",
         "children": [{"id": 7, "label": "total", "filed": "step1.resp||data||total"}]},
        {"id": 8, "label": "result", "filed": "step1.resp||result"}]},
    {"id": 9, "label": "step2.resp", "filed": "step2.resp", "children": [
        {"id": 10, "label": "data", "filed": "step2.resp||data",
         "children": [{"id": 11, "label": "numHits", "filed": "step2.resp||data||numHits"},
                      {"id": 12, "label": "messages", "filed": "step2.resp||data||messages"},
                      {"id": 13, "label": "aggResults", "filed": "step2.resp||data||aggResults", "children": []}]},
        {"id": 17, "label": "result", "filed": "step2.resp||result"}]},
    {"id": 0, "label": "res.resp", "filed": "res.resp", "children": [
        {"id": 14, "label": "simple.messageType", "filed": "step2.resp||data||aggResults||simple.messageType",
         "children": [
             {"id": 15, "label": "count", "filed": "step2.resp||data||aggResults||simple.messageType||count"},
             {"id": 16, "label": "messageType",
              "filed": "step2.resp||data||aggResults||simple.messageType||messageType"}]},
        {"id": 3, "label": "aggResults", "filed": "step1.resp||data||aggResults", "children": [
            {"id": 4, "label": "openTS.day", "filed": "step1.resp||data||aggResults||openTS.day",
             "children": [{"id": 5, "label": "count", "filed": "step1.resp||data||aggResults||openTS.day||count"},
                          {"id": 6, "label": "time_fm",
                           "filed": "step1.resp||data||aggResults||openTS.day||time_fm"}]}]}]}]


def get_res_format():
    res_resp = []
    for i in res:
        if i.get("id") == 0:
            res_resp = i.get("children", [])
            break
    return res_resp


def get_res_resp(result, a, res_resp):
    for item in res_resp:
        if item.get("children"):
            result[item["label"]] = get_res_resp(a, item["children"])
        fields = item["filed"].split("||")
        for i in fields:
            print(a)
            a = a.get(i)
        result[fields[-1]] = a
    return result


if __name__ == '__main__':
    print(main(a))
    res = get_res_format()
    data = get_res_resp(a, res)
    print(data)
