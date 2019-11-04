# -*- coding: utf-8 -*-
# @Time    : 2019/11/4 18:22
# @Author  : tian
# @Email   : zengdetian@eefung.com
# @File    : 抽取数据.py
# @Software: PyCharm

from xlrd import open_workbook
import random

# 原始数据文件
origin_data_path = "D:\chrome\\5000测试数据.xlsx"   # 第一批训练数据
origin_test_data_path = "D:\\chrome\\测试数据.et"  # 第一批测试数据，1400条

# excel文件中是有页数的指定
page_num = 35
test_page_num = 2

def getdata_from_xlsx(path, page_num):
    '''
    从excel文件中读取数据
    :return:
    '''
    excelFile = open_workbook(path)    # D:\\chrome\\测试数据.et

    content_set = set()   # 集合可以排除重复的数据

    for i in range(page_num):  # 遍历page_num个页
        if i == 1:
            sheet = excelFile.sheet_by_index(i)

            cols = sheet.col_values(3)  # 内容
            cols1 = sheet.col_values(4)  # 标签

            for index, line in enumerate(cols):
                if index > 0:
                    content_set.add(cols1[index]+"\t"+line.replace("\n", "")+"\n")
    # 返回相应的集合
    print("集合的长度为%d" % len(content_set))
    return content_set


def shuffle_data(path, new_path):
    '''打乱文本数据'''
    res = open(path, "r", encoding="utf8").readlines()
    random.shuffle(res)

    f_w = open(new_path, "w", encoding="utf8")
    for line in res:
        f_w.write(line)

def get_all_data():
    '''
    从excel文件中读取数据，放入txt文件中去
    :return:
    '''
    result1 = getdata_from_xlsx("C:\\Users\\eefung\\Desktop\\test.et", page_num=2)
    # result2 = getdata_from_xlsx("D:\chrome\测试数据2.xlsx", page_num=19)

    # result = [item for item in result2 if item not in result1]
    f_w = open("抽取的测试数据.txt", "w", encoding="utf8")
    [f_w.write(i) for i in result1]

def get_wanted_data():
    # 得到所有的数据
    get_all_data()
    f_w = open("重敏感与非敏感的测试数据.txt", "w", encoding="utf8")
    # 只得到重敏感与非敏感的数据
    f_w1 = open("轻量敏感的测试数据.txt", "w", encoding="utf8")
    f_r = open("抽取的测试数据.txt", "r", encoding="utf8")
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










