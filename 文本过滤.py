# -*- coding: utf-8 -*-
# @Time    : 2019/11/6 10:42
# @Author  : tian
# @Email   : zengdetian@eefung.com
# @File    : 文本过滤.py
# @Software: PyCharm

from xlrd import open_workbook
from random import randint
import re
import random

'''
对文本做过滤
'''
# 原始数据文件
Origin_data_path = "D:\数据\DATA\重敏感与非敏感的数据_去重.txt"
New_path = "D:\数据\DATA\重敏感与非敏感的数据_过滤.txt"
Train_path = "D:\数据\DATA\重敏感与非敏感的数据_train.txt"
Val_path = "D:\数据\DATA\重敏感与非敏感的数据_val.txt"

def url_filter(message):
    '''去除文本中的url'''
    results = re.sub("(?isu)((http|https)\://[a-zA-Z0-9\.\?/&\=\:]+)", '', message)
    p = re.compile('<[^>]+>')
    res = p.sub("", results)
    return res


def filter_punctuate(content):
    '''滤除标点符号和表情'''
    emojis = [line.strip() for line in open("emoji.txt", "r", encoding="utf-8").readlines()]
    for emoji in emojis:
        content = content.replace(emoji, "")  # 去除表情
    return content.replace('?', "").replace("#", "").\
        replace(" ", "").replace("？", "").replace("【", "").replace("】", "").\
        replace("！", "")

    # |！|，|。|；|！|,|…| |  |：|:|-|/|】|【|?|.


def filter_at(message):
    # 过滤掉  @某某某
    results = re.sub("@.{2,30}[ ]{1}", "", message)
    # results = re.sub("@.{2,30}\n", "\n", results)
    # print(results)

    new_message = ''
    # sample = u'I am from 美国。We should be friends. 朋友。'
    #只保留汉字
    for n in re.findall('[^(a-z)]+', results):
        new_message += n
    new_message2 = ''
    for n in re.findall('[^(A-Z)]+', new_message):
        new_message2 += n
    # print(new_message2)
    return new_message2


def static_rate_of_diff_part(path, label, typeforfasttext=False):
    '''统计一个文本中两个类别的个数及比列'''
    count = 0
    count1 = 0
    # 查看训练数据中的类别比列
    with open(path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if typeforfasttext:
                hang = line.split('\t__label__')
                if hang[1].strip() == label:  # 1
                    count += 1
                else:
                    count1 += 1
            else:
                hang = line.split('\t')
                if hang[0].strip() == label:   # 1
                    count += 1
                else:
                    count1 += 1
    print(label, ' count is', count)
    print('the other is', count1)
    print("the rate is=", float(count) / count1)


def split_the_text_to_two(source_text, train, percent1, val, percent2):
    '''打乱文本的顺序, 将一个文本中的行数按比例分割成为train val 两个部分
    对数据集做划分，分为训练集与测试集，按8:2的比例'''
    f1 = open(train, mode='w', encoding='utf-8')
    f2 = open(val, mode='w', encoding='utf-8')

    with open(source_text, mode='r', encoding='utf-8') as f:
        contents = f.readlines()
        random.shuffle(contents)     # 打乱文本的顺序
        for i, line in enumerate(contents):
            if i < len(contents)*percent1:
                f1.write(line)
            elif i < len(contents)*(percent1+percent2):
                f2.write(line)

    # close the file
    f1.close()
    f2.close()


def data_filter_new(old_path, path):
    f_w = open(path, "w", encoding="utf8")
    # 从txt中读取数据
    contents = open(old_path, "r", encoding="utf8").readlines()
    # 过滤文本
    for line in contents:
        contents = line.split("\t")
        # 过滤url
        content = url_filter(contents[1])
        # 过滤 @XXX
        content = filter_at(content)
        # 过滤表情和多余的标点符号
        content = filter_punctuate(content)
        # 写入新的文件中去
        f_w.write(contents[0] + "\t" + content)

    f_w.close()


if __name__ == "__main__":
    data_filter_new(old_path=Origin_data_path, path=New_path)
    static_rate_of_diff_part(New_path, "重敏感", typeforfasttext=False)
    split_the_text_to_two(New_path, Train_path, 0.8, Val_path, 0.2)
    # 查看分割后的比例
    print("============================================================")
    static_rate_of_diff_part(Train_path, "重敏感", typeforfasttext=False)
    print("============================================================")
    static_rate_of_diff_part(Val_path, "重敏感", typeforfasttext=False)

