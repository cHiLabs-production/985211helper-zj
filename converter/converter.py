# chiLabs 985211helper-zj 浙考小助手 (https://github.com/cHiLabs-production/985211helper-zj)
# Converter: Convert xls file from ZEEA to machine readable JSON file, adding 985, 211 and more tags.
# Powered by chihuo2104(c)2018-2024

import json

import math
import pandas as pd

# Reading Data
# Sources: ZEEA(https://zjzs.net/)
# 2024：https://www.zjzs.net/art/2024/7/21/art_155_9900.html
# 2023: https://www.zjzs.net/art/2023/7/19/art_155_2089.html
# 2022: https://www.zjzs.net/art/2022/7/19/art_155_7241.html
year2022 = pd.read_excel("./2022.xls")
year2023 = pd.read_excel("./2023.xls")
year2024 = pd.read_excel("./2024.xls")

# 去掉不需要的内容
year2022 = year2022.drop("专业代号", axis=1)
year2023 = year2023.drop("专业代号", axis=1)
year2024 = year2024.drop("专业代号", axis=1)

# 985大学(39)
university_985 = [
    "北京大学", "清华大学", "浙江大学", "上海交通大学", "复旦大学", "南京大学",
    "武汉大学", "四川大学", "中山大学", "山东大学", "吉林大学", "南开大学",
    "北京师范大学", "华东师范大学", "西安交通大学", "天津大学", "中国人民大学",
    "中国科学技术大学", "东南大学", "天津大学", "哈尔滨工业大学", "北京航空航天大学",
    "北京理工大学", "国防科技大学", "华南理工大学", "大连理工大学", "华中科技大学",
    "中南大学", "电子科技大学", "西北工业大学", "东北大学", "重庆大学",
    "湖南大学", "中国农业大学", "厦门大学", "中国海洋大学", "兰州大学",
    "中央民族大学", "西北农林科技大学"
]

# 211大学(71)
university_211 = [
    "南京师范大学", "东北师范大学", "华中师范大学", "华南师范大学", "陕西师范大学",
    "湖南师范大学", "海军军医大学", "空军军医大学", "北京中医药大学", "中国药科大学",
    "华中农业大学", "南京农业大学", "四川农业大学", "东北农业大学", "中央财经大学",
    "对外经济贸易大学", "上海财经大学", "中南财经政法大学", "西南财经大学", "北京外国语大学",
    "上海外国语大学", "中国政法大学", "中国传媒大学", "北京交通大学", "中国矿业大学",
    "北京科技大学", "北京邮电大学", "西安电子科技大学", "哈尔滨工程大学", "西南交通大学",
    "南京理工大学", "中国石油大学", "河海大学", "江南大学", "华东理工大学",
    "中国地质大学", "武汉理工大学", "东华大学", "北京工业大学", "华北电力大学",
    "北京化工大学", "合肥工业大学", "南京航空航天大学", "太原理工大学", "长安大学",
    "河北工业大学", "大连海事大学", "西北大学", "暨南大学", "苏州大学",
    "南昌大学", "辽宁大学", "贵州大学", "延边大学", "中央音乐学院",
    "北京体育大学", "广西大学", "安徽大学", "海南大学", "内蒙古大学",
    "石河子大学", "宁夏大学", "青海大学", "云南大学", "郑州大学",
    "新疆大学", "上海大学", "南昌大学", "福州大学"
]

# 制空0
year2022["985"] = [0] * len(year2022)
year2022["211"] = [0] * len(year2022)
year2022["双一流"] = [0] * len(year2022)
year2022["省重点"] = [0] * len(year2022)
year2022["民办"] = [0] * len(year2022)
year2022["中外合作"] = [0] * len(year2022)
year2022["独立学院"] = [0] * len(year2022)

year2023["985"] = [0] * len(year2023)
year2023["211"] = [0] * len(year2023)
year2023["双一流"] = [0] * len(year2023)
year2023["省重点"] = [0] * len(year2023)
year2023["民办"] = [0] * len(year2023)
year2023["中外合作"] = [0] * len(year2023)
year2023["独立学院"] = [0] * len(year2023)

year2024["985"] = [0] * len(year2024)
year2024["211"] = [0] * len(year2024)
year2024["双一流"] = [0] * len(year2024)
year2024["省重点"] = [0] * len(year2024)
year2024["民办"] = [0] * len(year2024)
year2024["中外合作"] = [0] * len(year2024)
year2024["独立学院"] = [0] * len(year2024)

# 记录schoolcode以方便2023/2024的数据查找
# 双一流
schoolcodes_syl = []
# 民办
schoolcodes_mb = []
# 独立学院
schoolcodes_dlxy = []
# 中外合作
schoolcodes_zwhz = []
# 省重点
schoolcodes_szd = []

# 使2022年数据与2023和2024年的数据格式保持一致
for i in range(len(year2022)):
    if year2022.at[i, "学校名称"].find("（一流大学建设高校）") != -1 or year2022.at[i, "学校名称"].find("（一流学科建设高校）") != -1 :
        year2022.at[i, "双一流"] = 1
        if year2022.at[i, "学校代号"] not in schoolcodes_syl:
            schoolcodes_syl.append(year2022.at[i, "学校代号"])
    if year2022.at[i, "学校名称"].find("（省重点建设高校）") != -1 or year2022.at[i, "学校名称"].find("（省市共建重点高校）") != -1 :
        year2022.at[i, "省重点"] = 1
        if year2022.at[i, "学校代号"] not in schoolcodes_szd:
            schoolcodes_szd.append(year2022.at[i, "学校代号"])
    if year2022.at[i, "学校名称"].find("(民办)") != -1:
        year2022.at[i, "民办"] = 1
        if year2022.at[i, "学校代号"] not in schoolcodes_mb:
            schoolcodes_mb.append(year2022.at[i, "学校代号"])
    if year2022.at[i, "学校名称"].find("(独立学院)") != -1:
        year2022.at[i, "独立学院"] = 1
        if year2022.at[i, "学校代号"] not in schoolcodes_dlxy:
            schoolcodes_dlxy.append(year2022.at[i, "学校代号"])
    if year2022.at[i, "学校名称"].find("(中外合作办学)") != -1:
        year2022.at[i, "中外合作"] = 1
        if year2022.at[i, "学校代号"] not in schoolcodes_zwhz:
            schoolcodes_zwhz.append(year2022.at[i, "学校代号"])
    if year2022.at[i, "专业名称"].find("(中外合作办学)") != -1:
        year2022.at[i, "中外合作"] = 1
    # 除去数据
    year2022.at[i, "学校名称"] = year2022.at[i, "学校名称"].replace("（一流大学建设高校）", "")
    year2022.at[i, "学校名称"] = year2022.at[i, "学校名称"].replace("（一流学科建设高校）", "")
    year2022.at[i, "学校名称"] = year2022.at[i, "学校名称"].replace("（省重点建设高校）", "")
    year2022.at[i, "学校名称"] = year2022.at[i, "学校名称"].replace("（省市共建重点高校）", "")
    year2022.at[i, "学校名称"] = year2022.at[i, "学校名称"].replace("（入选“2011计划”高校）", "")
    year2022.at[i, "学校名称"] = year2022.at[i, "学校名称"].replace("(民办)", "")
    year2022.at[i, "学校名称"] = year2022.at[i, "学校名称"].replace("(独立学院)", "")
    year2022.at[i, "学校名称"] = year2022.at[i, "学校名称"].replace("(中外合作办学)", "")
    year2022.at[i, "专业名称"] = year2022.at[i, "专业名称"].replace("(中外合作办学)", "")
    if year2022.at[i, "学校名称"] in university_985:
        year2022.at[i, "985"] = 1
        year2022.at[i, "211"] = 1
    if year2022.at[i, "学校名称"] in university_211:
        year2022.at[i, "211"] = 1

for i in range(len(year2023)):
    if year2023.at[i, "学校代号"] in schoolcodes_syl:
        year2023.at[i, "双一流"] = 1
    if year2023.at[i, "学校代号"] in schoolcodes_szd:
        year2023.at[i, "省重点"] = 1
    if year2023.at[i, "学校代号"] in schoolcodes_mb:
        year2023.at[i, "民办"] = 1
    if year2023.at[i, "学校代号"] in schoolcodes_dlxy:
        year2023.at[i, "独立学院"] = 1
    if year2023.at[i, "学校名称"].find("(中外合作办学)") != -1:
        year2023.at[i, "中外合作"] = 1
    if year2023.at[i, "专业名称"].find("(中外合作办学)") != -1:
        year2023.at[i, "中外合作"] = 1
    year2023.at[i, "学校名称"] = year2023.at[i, "学校名称"].replace("(中外合作办学)", "")
    year2023.at[i, "专业名称"] = year2023.at[i, "专业名称"].replace("(中外合作办学)", "")
    if year2023.at[i, "学校名称"] in university_985:
        year2023.at[i, "985"] = 1
        year2023.at[i, "211"] = 1
    if year2023.at[i, "学校名称"] in university_211:
        year2023.at[i, "211"] = 1

for i in range(len(year2024)):
    if year2024.at[i, "学校代号"] in schoolcodes_syl:
        year2024.at[i, "双一流"] = 1
    if year2024.at[i, "学校代号"] in schoolcodes_szd:
        year2024.at[i, "省重点"] = 1
    if year2024.at[i, "学校代号"] in schoolcodes_mb:
        year2024.at[i, "民办"] = 1
    if year2024.at[i, "学校代号"] in schoolcodes_dlxy:
        year2024.at[i, "独立学院"] = 1
    if year2024.at[i, "学校名称"].find("(中外合作办学)") != -1:
        year2024.at[i, "中外合作"] = 1
    if year2024.at[i, "专业名称"].find("(中外合作办学)") != -1:
        year2024.at[i, "中外合作"] = 1
    year2024.at[i, "学校名称"] = year2024.at[i, "学校名称"].replace("(中外合作办学)", "")
    year2024.at[i, "专业名称"] = year2024.at[i, "专业名称"].replace("(中外合作办学)", "")
    if year2024.at[i, "学校名称"] in university_985:
        year2024.at[i, "985"] = 1
        year2024.at[i, "211"] = 1
    if year2024.at[i, "学校名称"] in university_211:
        year2024.at[i, "211"] = 1


export = []

for i in range(len(year2022)):
    if math.isnan(year2022.at[i, "位次"]):
        year2022.at[i, "位次"] = -1
    export.append({
        "year": 2022,
        "code": int(year2022.at[i, "学校代号"]),
        "name": str(year2022.at[i, "学校名称"]),
        "profession": str(year2022.at[i, "专业名称"]),
        "is985": int(year2022.at[i, "985"]),
        "is211": int(year2022.at[i, "211"]),
        "syl": int(year2022.at[i, "双一流"]),
        "dlxy": int(year2022.at[i, "独立学院"]),
        "zwhz": int(year2022.at[i, "中外合作"]),
        "mb": int(year2022.at[i, "民办"]),
        "intention": int(year2022.at[i, "计划数"]),
        "score": int(year2022.at[i, "分数线"]),
        "ranking": int(year2022.at[i, "位次"])
    })

for i in range(len(year2023)):
    if math.isnan(year2023.at[i, "位次"]):
        year2023.at[i, "位次"] = -1
    export.append({
        "year": 2023,
        "code": int(year2023.at[i, "学校代号"]),
        "name": year2023.at[i, "学校名称"],
        "profession": year2023.at[i, "专业名称"],
        "is985": int(year2023.at[i, "985"]),
        "is211": int(year2023.at[i, "211"]),
        "syl": int(year2023.at[i, "双一流"]),
        "dlxy": int(year2023.at[i, "独立学院"]),
        "zwhz": int(year2023.at[i, "中外合作"]),
        "mb": int(year2023.at[i, "民办"]),
        "intention": int(year2023.at[i, "计划数"]),
        "score": int(year2023.at[i, "分数线"]),
        "ranking": int(year2023.at[i, "位次"])
    })

for i in range(len(year2024)):
    if math.isnan(year2024.at[i, "位次"]):
        year2024.at[i, "位次"] = -1
    export.append({
        "year": 2024,
        "code": int(year2024.at[i, "学校代号"]),
        "name": year2024.at[i, "学校名称"],
        "profession": year2024.at[i, "专业名称"],
        "is985": int(year2024.at[i, "985"]),
        "is211": int(year2024.at[i, "211"]),
        "syl": int(year2024.at[i, "双一流"]),
        "dlxy": int(year2024.at[i, "独立学院"]),
        "zwhz": int(year2024.at[i, "中外合作"]),
        "mb": int(year2024.at[i, "民办"]),
        "intention": int(year2024.at[i, "计划数"]),
        "score": int(year2024.at[i, "分数线"]),
        "ranking": int(year2024.at[i, "位次"])
    })

print(len(export))

with open('data.json', 'w') as file:
    json.dump(export, file)  # indent=4 is for pretty formatting