# -*- coding: utf-8 -*-
# @Time    : 2019/11/7 14:04
# @Author  : tian
# @Email   : zengdetian@eefung.com
# @File    : test2.py
# @Software: PyCharm

LTP_DATA_DIR = 'D:\BAK\LTP_3.4\ltp_data'  # ltp模型目录的路径
#分词
import os
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
from pyltp import Segmentor
segmentor = Segmentor()  # 初始化实例
segmentor.load(cws_model_path)  # 加载模型

# 词性标注
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
from pyltp import Postagger
postagger = Postagger()  # 初始化实例
postagger.load(pos_model_path)  # 加载模型

# 命名实体识别
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`
from pyltp import NamedEntityRecognizer
recognizer = NamedEntityRecognizer()  # 初始化实例
recognizer.load(ner_model_path)  # 加载模型

Data_path = "D:\代码库\-\文本分类器\分类结果\轻量敏感文本的分类结果.txt"

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

f_temp = open("实体词统计/重敏感-轻量敏感处理得来.txt", "w", encoding="utf8")
[f_temp.write(item) for item in data_part1]
f_temp1 = open("实体词统计/非敏感-轻量敏感处理得来.txt", "w", encoding="utf8")
[f_temp1.write(item) for item in data_part2]

def find_entity(content):
    words = segmentor.segment(content)  # 分词
    words_list = list(words)  # words_list列表保存着分词的结果
    postags = postagger.postag(words)  # 词性标注
    postags_list = list(postags)  # postags_list保存着词性标注的结果
    netags = recognizer.recognize(words, postags)  # 命名实体识别
    netags_list = list(netags)  # netags_list保存着命名实体识别的结果

    # 去除非命名实体
    a = len(words_list)
    words_list_1 = []
    postags_list_1 = []
    netags_list_1 = []
    i = 0
    while i < a:
        if netags_list[i] != 'O':
            words_list_1.append(words_list[i])
            postags_list_1.append(postags_list[i])
            netags_list_1.append(netags_list[i])
        i += 1

    a1 = len(words_list_1)
    # 提取机构名
    i = 0
    orignizations = []
    while i < a1:
        if netags_list_1[i] == 'S-Ni':
            orignizations.append(words_list_1[i])
        elif netags_list_1[i] == 'B-Ni':
            temp_s = ''
            temp_s += words_list_1[i]
            j = i + 1
            while j < a1 and (netags_list_1[j] == 'I-Ni' or netags_list_1[j] == 'E-Ni'):
                temp_s += words_list_1[j]
                j += 1
            orignizations.append(temp_s)
        i += 1
    # 删除重重出现的机构名
    orignizations_1 = set(orignizations)
    orignizations_2 = list(orignizations_1)


    # 提取地名
    i = 0
    places = []
    while i < a1:
        if netags_list_1[i] == 'S-Ns':
            places.append(words_list_1[i])
        elif netags_list_1[i] == 'B-Ns':
            temp_s = ''
            temp_s += words_list_1[i]
            j = i + 1
            while j < a1 and (netags_list_1[j] == 'I-Ns' or netags_list_1[j] == 'E-Ns'):
                temp_s += words_list_1[j]
                j += 1
            places.append(temp_s)
        i += 1
    # 删除重复出现的地名
    places_1 = set(places)
    places_2 = list(places_1)
    # f_5 = open('地名.txt', 'w', encoding='UTF-8', errors='ignore')
    # for place in places_2:
    #     f_5.write(place + '\r\n')

    #设计一些规则去除一些不符合要求的实体
    places_len2 = len(places_2)
    j = 0
    places_3 = []  #places_3存在最终的地名
    while j < places_len2:
        flag = 0
        len_2 = len(places_2[j])
        if len_2 <= 1 :
            flag = 1
        else:
            i = 0
            len_2 = len(places_2[j])
            while i < len_2:
                if places_2[j][i] =='。' or places_2[j][i]=='.' or places_2[j][i] == '\n':
                    flag = 1
                if places_2[j][i]>='a' and places_2[j][i]<='z':
                    flag = 1
                if places_2[j][i]>='0' and places_2[j][i]<='9':
                    flag = 1
                i += 1
        if flag == 0:
            places_3.append(places_2[j])
        j += 1


    # 提取人名
    i = 0
    names = []
    while i < a1:
        if netags_list_1[i] == 'S-Nh':
            names.append(words_list_1[i])
        elif netags_list_1[i] == 'B-Nh':
            temp_s3 = ''
            temp_s3 += words_list_1[i]
            j = i + 1
            while (j < a1) and (netags_list_1[j] == 'I-Nh' or netags_list_1[j] == 'E-Nh'):
                temp_s3 += words_list_1[j]
                j += 1
            names.append(temp_s3)
        i += 1
    # 去除重复的人名
    names_1 = set(names)
    names_2 = list(names_1)


    # 设计一些规则去除一些不符合要求的实体
    names_len2 = len(names_2)
    j = 0
    names_3 = []
    while j < names_len2:
        flag = 0
        len_2 = len(names_2[j])
        if len_2 <= 1 :
            flag = 1
        else:
            i = 0
            len_2 = len(names_2[j])
            while i < len_2:
                if names_2[j][i] =='。' or names_2[j][i]=='.' or names_2[j][i] == '\n':
                    flag = 1
                # if names_2[j][i]>='a' and names_2[j][i]<='z':
                #     flag = 1
                # if names_2[j][i]>='0' and names_2[j][i]<='9':
                #     flag = 1
                i += 1
        if flag == 0:
            names_3.append(names_2[j])
        j += 1

    # 舆情引导策略，是上升，还是下降；找拐点的原因；找热门的事件；舆情干预。

    # 将三个列表整合到一个字典中，写入文件
    shiti = {}
    for name in names_3:
        shiti[name] = '人名'
    for place in places_3:
        shiti[place] = '地名'
    for orignization in orignizations_2:
        shiti[orignization] = '机构名'

    if len(shiti) != 0:
        for key, value in shiti.items():
            f_shiti.write(key + '\t' + value + '\t')
        f_shiti.write('\n')
    else:
        f_shiti.write('\n')

# 对data_part1进行处理
# f_w = open("实体词统计/实体词.txt", "w", encoding="utf8")
f_shiti = open('实体词统计/实体词1-ltp-重敏感-轻量敏感处理得来.txt', 'a', encoding='UTF-8', errors='ignore')
for item in data_part1:
    entitys = []
    content = item.strip()
    find_entity(content)

# 对data_part2进行处理
# f_w = open("实体词统计/实体词.txt", "w", encoding="utf8")
f_shiti = open('实体词统计/实体词1-ltp-非敏感-轻量敏感处理得来.txt', 'a', encoding='UTF-8', errors='ignore')
for item in data_part2:
    entitys = []
    content = item.strip()
    find_entity(content)


segmentor.release()  # 释放模型
postagger.release()  # 释放模型
recognizer.release()  # 释放模型










