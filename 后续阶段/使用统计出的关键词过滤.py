# -*- coding: utf-8 -*-
# @Time    : 2019/11/13 14:49
# @Author  : tian
# @Email   : zengdetian@eefung.com
# @File    : 使用统计出的关键词过滤.py
# @Software: PyCharm

# 加载总结的重敏感词
words_path = "C:\\Users\eefung\Desktop\统计出的重敏感词.txt"
# 使用统计出的关键词对轻量敏感文本进行过滤
line = open(words_path, "r", encoding="utf8").readlines()[0]
heavily_words = line.strip().split(" ")
print(len(heavily_words))

# 加载总结的非敏感词
words_path1 = "C:\\Users\eefung\Desktop\统计出的非敏感词.txt"
# 使用统计出的关键词对轻量敏感文本进行过滤
line1 = open(words_path1, "r", encoding="utf8").readlines()[0]
light_words = line1.strip().split(" ")
print(len(light_words))


# 读入被model判为重敏感，且不含实体词的（或者只含一个实体词-中国）文本进行关键词过滤
first_texts = "D:\代码库\-\文本分类器\分类结果\轻量敏感文本的分类结果-重敏感.txt"
lines = open(first_texts, "r", encoding="utf8").readlines()
print(len(lines))
# 加载文本
content_result = dict()
final_result = dict()
for i, line in enumerate(lines):  # 通过两个字典记录每条文本初始的指示值
    final_result[i] = True
    content_result[i] = line
# 加载命名实体词
print(len(final_result))
entity_words_path = "D:\代码库\-\后续阶段\实体词统计\实体词1-ltp-重敏感-轻量敏感处理得来.txt"
entity_words = open(entity_words_path, "r", encoding="utf8").readlines()
# 遍历不含实体词的文本
for i, word in enumerate(entity_words):
    # print(i)
    # if i == 1244:
    #     print("debug!")
    # 如果实体词不存在，则将对应的文本行删除掉-将相应的开关函数置为False
    if word.strip() == "" or word.strip() == "中国	地名":
        final_result[i] = False
# 通过开关指示函数删除相应的不含实体词的文本
for i, value in final_result.items():
    if value == False:
        content_result.pop(i)

print("还有多少的文本需要判别%d" % len(content_result))
import copy
content_result1 = copy.deepcopy(content_result)

# 开始过滤，过滤掉非敏感的文本，
count1 = 0
f_light = open("实体词统计/可能为非敏感的文本.txt", "w", encoding="utf8")
for i, line in content_result1.items():
    flag = False
    for word in light_words:
        if word in line:
            flag = True
    if flag is True:
        count1 += 1
        print("可能为非敏感的文本：||||"+line.strip())
        f_light.write(line)
        content_result.pop(i)
print("一共找出%d条可能为非敏感的文本" % count1)

# 从提出了非敏感的文本中招敏感文本
final_content = dict()
count = 0
f_heavily = open("实体词统计/可能为重敏感的文本.txt", "w", encoding="utf8")
for i, line in content_result.items():
    flag = False
    for word in heavily_words:
        if word in line:
            flag = True

    if flag == True:
        count += 1
        print("可能为重敏感的文本：||||"+line.strip())
        f_heavily.write(line)
    else: # 写入final_content
        final_content[i] = line

print("一共找出%d条可能为重敏感的文本"%count)

f_final = open("实体词统计/还未处理的文本.txt", "w", encoding="utf8")
print("=================未处理的文本======================")
for item in final_content.values():
    f_final.write(item)

