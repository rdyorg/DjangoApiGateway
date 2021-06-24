import pydash as pydash

old_data = {
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


# todo: 要求，如果是列表元素的重组，必须要保证新列表结构内的元素本来就是在同一个列表内


def get_format_resp(res, format_data):
    for j in format_data:
        if not j.get("children"):
            res[j["label"]] = get_dash_data(j["field"])
            continue
        if j["field_type"] == "list":
            tem_list = []
            for i in j["children"]:
                field_data = get_list_dash_data(i["label"], i["field"])
                tem_list.append(field_data)
            # 翻转数据结构对象
            tem_list = flip_data_structure(tem_list)
            res[j["label"]] = tem_list
        elif j["field_type"] == "dict":
            res[j["label"]] = get_format_resp({}, j["children"])
        else:
            res[j["label"]] = get_dash_data(j["field"])
    return res


field_dict = {'step1.resp||data||data||data||day': 4, 'step1.resp||scripts': 0, 'step2.resp||data||data||data': 3,
              'step2.resp||scripts': 0}


def get_list_field(tmp_str, get_list):
    # 说明当前结果是一个列表值，需要对列表值长度进行循环
    if get_list:
        new_list = []
        for i in get_list:
            field = tmp_str.split("||")[-1]
            for j in range(field_dict[tmp_str]):
                new_list.append(i + "||" + field + "||" + str(j))
        get_list = new_list
    else:
        for j in range(field_dict[tmp_str]):
            get_list.append(tmp_str + "||" + str(j))
    return get_list


def get_field_data(field):
    field_list = field.split("||")
    tmp_str = field_list[0]
    tmp_list = []
    for i in range(len(field_list)):
        if i != len(field_list) - 1:
            if i != 0:
                tmp_str = tmp_str + "||" + field_list[i]
            if tmp_str in field_dict:
                tmp_list = get_list_field(tmp_str, tmp_list)
    res = [i + "||" + field_list[-1] for i in tmp_list]
    return res


# pydash获取数据指定位置
def get_dash_data(field):
    field_list = field.split("||")
    return pydash.get(old_data, field_list)


# pydash获取指定位置包含数组的数据
def get_list_dash_data(label, field):
    new_res = []
    res = get_field_data(field)
    for i in res:
        new_res.append({label: get_dash_data(i)})
    return new_res


def flip_data_structure(ne_res):
    res = []
    for i in range(len(ne_res[0])):
        tem_dict = {}
        for j in ne_res:
            tem_dict.update(j[i])
        res.append(tem_dict)
    return res


sse = [
    {"id": 14, "label": "data", "field": "step2.resp||data||data||data", "field_type": "list", "children": [
        {"id": 15, "label": "activityPercent", "field": "step2.resp||data||data||data||activityPercent",
         "field_type": "str"},
        {"id": 16, "label": "areaID", "field": "step2.resp||data||data||data||areaID", "field_type": "str"},
        {"id": 17, "label": "activityDeviceNum", "field": "step2.resp||data||data||data||activityDeviceNum",
         "field_type": "str"},
        {"id": 18, "label": "day", "field": "step2.resp||data||data||data||day", "field_type": "str"},
        {"id": 19, "label": "totalDeviceNum", "field": "step2.resp||data||data||data||totalDeviceNum",
         "field_type": "str"}]},
    {"id": 5, "label": "day", "field": "step1.resp||data||data||data||day", "field_type": "list",
     "children": [{"id": 6, "label": "count", "field": "step1.resp||data||data||data||day||count", "field_type": "str"},
                  {"id": 7, "label": "cardinality_primeID",
                   "field": "step1.resp||data||data||data||day||cardinality_primeID", "field_type": "str"},
                  {"id": 8, "label": "time_fm", "field": "step1.resp||data||data||data||day||time_fm",
                   "field_type": "str"}]}]

if __name__ == '__main__':
    import time

    star_time = time.time()
    res = get_format_resp({}, sse)
    import json

    print(json.dumps(res))
    print(time.time() - star_time)
