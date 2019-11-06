# -*- coding: utf-8 -*-
# @Time    : 2019/11/5 13:41
# @Author  : tian
# @Email   : zengdetian@eefung.com
# @File    : 相似文本去重.py
# @Software: PyCharm
import Levenshtein
import copy

USED_PATH = "D:\数据\DATA\重敏感与非敏感的数据.txt"
CONTENT_DICT = dict()
for line in open(USED_PATH, "r", encoding="UTF8").readlines():
    # 遍历所有的文本，计算文本的编辑距离
    result = line.split("\t", maxsplit=1)
    if len(result[1]) > 20:    # 去除较短的文本
        CONTENT_DICT[result[1]] = result[0]  # content为key ，label为内容；

print(len(CONTENT_DICT))
CONTENT_DICT1 = copy.deepcopy(CONTENT_DICT)
compare_contents = list(CONTENT_DICT1.keys())
CONTENT_DICT2 = copy.deepcopy(CONTENT_DICT)

# 使用编辑距离对比文本的相似性
for j, item in enumerate(CONTENT_DICT.keys()):
    min_value = 9999999999999999999
    index = 0
    for i, item_1 in enumerate(CONTENT_DICT1.keys()):
        if i != j:
            temp = Levenshtein.distance(item, item_1)
            if temp < min_value:
                min_value = temp
                index = i

    # print(index)

    if min_value < 10:
        print("文本---" + item)
        print("文本编辑距离为：%d" % min_value)
        print("最相似的文本为：" + compare_contents[index])
        # 从CONTENT_DICT2中删除相应的相似性文本
        if compare_contents[index] in CONTENT_DICT2:
            CONTENT_DICT2.pop(compare_contents[index])

# 将CONTENT_DICT2写入到新的文件中
f_w = open("D:\数据\DATA\重敏感与非敏感的数据_去重.txt", "w", encoding="utf8")
for key, value in CONTENT_DICT2.items():
    f_w.write(value+"\t"+key)

print("处理完成！")