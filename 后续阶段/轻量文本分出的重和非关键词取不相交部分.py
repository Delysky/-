# -*- coding: utf-8 -*-
# @Time    : 2019/11/12 15:48
# @Author  : tian
# @Email   : zengdetian@eefung.com
# @File    : 轻量文本分出的重和非关键词取不相交部分.py
# @Software: PyCharm
import pickle
# 查看两部分的关键词
heaviy_text_path = "D:\代码库\-\后续阶段\轻量敏感文本分析\重敏感词1"
light_text_path = "D:\代码库\-\后续阶段\轻量敏感文本分析\非敏感词1"
# heaviy_content = open(heaviy_text_path, "r", encoding="utf8").readlines()
# light_content = open(light_text_path, "r", encoding="utf8").readlines()

f = open(heaviy_text_path,'rb')
heavily_words = pickle.load(f)
f1 = open(light_text_path,'rb')
light_words = pickle.load(f1)


heavily_words_sets = set()
# print(heavily_words)
# 暂时设定频数小于5的不计入
for item in heavily_words:
    if int(item[1]) >= 3:
        heavily_words_sets.add(item[0])
    # print(item[0])
    # print(item[1])


light_words_sets = set()
# 暂时设定频数小于5的不计入
for item in light_words:
    if int(item[1]) >= 3:
        light_words_sets.add(item[0])

all_have_set = heavily_words_sets & light_words_sets   # 求交集
result1 = heavily_words_sets - all_have_set  # 求不相交的部分
result2 = light_words_sets - all_have_set  # 求不相交的部分
print(result1)
print(result2)

print(all_have_set)
