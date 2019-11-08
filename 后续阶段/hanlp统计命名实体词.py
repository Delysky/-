# -*- coding: utf-8 -*-
# @Time    : 2019/11/7 9:46
# @Author  : tian
# @Email   : zengdetian@eefung.com
# @File    : ner测试.py
# @Software: PyCharm
# 看敏感文本和非敏感文本中nt的词能占多少
from pyhanlp import *

# content = "济南市历下区人民法院徇私枉法法官周广军、华勇、张维红、王雪；"
NLPTokenizer = JClass('com.hankcs.hanlp.tokenizer.NLPTokenizer')
# print(NLPTokenizer.segment(content))

Data_path = "D:\数据\DATA\重敏感与非敏感的数据_train.txt"

data_part1 = []
data_part2 = []

for line in open(Data_path, "r", encoding="utf8").readlines():
    contents = line.split("\t", maxsplit=1)
    label = contents[0]
    content = contents[1]
    if label == "重敏感":
        data_part1.append(content)
    else:
        data_part2.append(content)

f_temp = open("实体词统计/重敏感.txt", "w", encoding="utf8")
[f_temp.write(item) for item in data_part1]

# 将重敏感和非敏感分开，同时分割句子，进行序列标注
import re
# 对data_part1进行处理
f_w = open("实体词统计/实体词.txt", "w", encoding="utf8")
for item in data_part1:
    entitys = []
    separate_lines = re.split('。|？|！|；', item.strip())
    # 遍历分割后的句子
    for sentence in separate_lines:
        results = NLPTokenizer.segment(sentence)
        for result in results:
            # print(type(result.nature))
            if "nt" in str(result.nature) or "ns" in str(result.nature) or "nr" in str(result.nature):
                entitys.append(result)
    # 将实体词写入文件中
    if len(entitys) != 0:
        for entity in entitys:
            f_w.write(str(entity)+"\t")
        f_w.write("\n")
    else:
        f_w.write("\n")


# 对data_part2进行处理
f_w1 = open("实体词统计/实体词-hanlp-非敏感.txt", "w", encoding="utf8")
for item in data_part2:
    entitys = []
    separate_lines = re.split('。|？|！|；', item.strip())
    # 遍历分割后的句子
    for sentence in separate_lines:
        results = NLPTokenizer.segment(sentence)
        for result in results:
            # print(type(result.nature))
            if "nt" in str(result.nature) or "ns" in str(result.nature) or "nr" in str(result.nature):
                entitys.append(result)
    # 将实体词写入文件中
    if len(entitys) != 0:
        for entity in entitys:
            f_w1.write(str(entity)+"\t")
        f_w1.write("\n")
    else:
        f_w1.write("\n")




