# -*- coding: utf-8 -*-
# @Time    : 2019/11/4 18:22
# @Author  : tian
# @Email   : zengdetian@eefung.com
# @File    : 抽取数据.py
# @Software: PyCharm

from xlrd import open_workbook
import random

# 原始数据文件
Origin_data_path = "D:\数据\\test.et"   # 第一批训练数据
# excel文件中是有页数的指定
Page_num = 9
TEMP_PATH = "D:\数据\DATA\抽取的数据.txt"
USED_PATH = "D:\数据\DATA\重敏感与非敏感的数据.txt"
UNUSED_PATH = "D:\数据\DATA\轻量敏感的数据.txt"

def getdata_from_xlsx(path, page_num):
    '''
    从excel文件中读取数据
    :return:
    '''
    excelFile = open_workbook(path)    # D:\\chrome\\测试数据.et

    content_set = set()   # 集合可以排除重复的数据

    for i in range(page_num):  # 遍历page_num个页

        sheet = excelFile.sheet_by_index(i)

        cols = sheet.col_values(3)  # 内容
        cols1 = sheet.col_values(4)  # 标签

        for index, line in enumerate(cols):
            if index > 0:
                content_set.add(cols1[index]+"\t"+line.replace("\n", "")+"\n")
    # 返回相应的集合
    print("集合的长度为%d" % len(content_set))
    return content_set


def get_all_data():
    '''
    从excel文件中读取数据，放入txt文件中去
    :return:
    '''
    result1 = getdata_from_xlsx(Origin_data_path, page_num=Page_num)

    # result = [item for item in result2 if item not in result1]
    f_w = open(TEMP_PATH, "w", encoding="utf8")
    [f_w.write(i) for i in result1]

def get_wanted_data():
    # 得到所有的数据
    get_all_data()
    f_w = open(USED_PATH, "w", encoding="utf8")
    # 只得到重敏感与非敏感的数据
    f_w1 = open(UNUSED_PATH, "w", encoding="utf8")
    f_r = open(TEMP_PATH, "r", encoding="utf8")
    for line in f_r.readlines():
        content = line.split("\t")
        if content[0] == "重敏感" or content[0] == "非敏感":
            f_w.write(line)
        elif content[0] == "轻量敏感":
            f_w1.write(line)
    f_w.close()
    f_w1.close()


if __name__ == "__main__":
    get_wanted_data()
    pass










