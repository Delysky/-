# -*- coding: utf-8 -*-
# @Time    : 2019/11/11 16:38
# @Author  : tian
# @Email   : zengdetian@eefung.com
# @File    : tfidf统计关键词.py
# @Software: PyCharm

'''
计算文档的TF-IDF
'''
import math
import jieba.posseg
import jieba
import pickle
stop_words = [line.strip() for line in open("D:\代码库\-\文本分类器\stop_words.txt", "r", encoding="utf8") if line != ""]
stop_words.append("\u3000") # 统计词频
stop_words.append("\n")

def count_word(content):
    word_dic = {}
    words_list = jieba.cut(content)
    for word in words_list:
        if word not in stop_words:
            if word in word_dic:
                word_dic[word] = word_dic[word] + 1
            else:
                word_dic[word] = 1
    return word_dic


# 计算TF-IDF
def count_tfidf(word_dic, words_dic):
    word_idf = {}
    word_tfidf = {}
    num_files = len(words_dic)
    for word in word_dic:
        for words in words_dic:
            if word in words:
                # 统计idf值
                if word in word_idf:
                    word_idf[word] = word_idf[word] + 1
                else:
                    word_idf[word] = 1
    for key, value in word_dic.items():
        if key != " ":
            word_tfidf[key] = value * math.log(num_files / (word_idf[key] + 1))

    # 降序排序
    values_list = sorted(word_tfidf.items(), key=lambda item: item[1], reverse=True)
    return values_list


def main(option):
    word_dict_pos = dict()
    # 遍历文本，找到所有的词
    folder_path = "D:\代码库\-\后续阶段\轻量敏感文本分析\重敏感"
    word_dict_all = {}  # 存所有的词
    contents = []    # 存所有的内容
    for line in open(folder_path, "r", encoding="utf8").readlines():
        content = line.split("\t", maxsplit=1)[1]
        words_list = jieba.posseg.cut(content)
        contents.append(content)
        for word in words_list:  # x.word,x.flag
            if word.word not in stop_words:
                word_dict_pos[word.word] = word.flag
                if word.word in word_dict_all:
                    word_dict_all[word.word] = word_dict_all[word.word] + 1
                else:
                    word_dict_all[word.word] = 1
    print("共有词%d" % len(word_dict_all))
    words = set(word_dict_all.keys())
    word_doce = dict()
    if option == "DF":
        # DF特征项 先找到所有的词，
        # 再统计所有词出现过的文档数
        for word in words:
            for content in contents:
                if word in content:
                    if word in word_doce:
                        word_doce[word] = word_doce[word] + 1
                    else:
                        word_doce[word] = 1
        result = dict()
        for word in word_doce.keys():  # 找出长度大于2的关键词
            if len(word) >= 2 and word.isdigit() != True:
                result[word] = word_doce[word]
        result1 = dict()
        # 保留名词和动词
        for word in result.keys():
            if "n" in word_dict_pos[word] or word_dict_pos[word] == "v":
                result1[word] = result[word]

        a = sorted(result1.items(), key=lambda x: x[1], reverse=True)
        print(a)
        f_w = open("D:\代码库\-\后续阶段\轻量敏感文本分析\重敏感词1", "wb")
        pickle.dump(a, f_w)
    else:
        pass
    #     files_dic = []
    #     # 遍历文件夹
    #     folder_path = "D:\代码库\-\后续阶段\轻量敏感文本分析\非敏感"
    #     for line in open(folder_path, "r", encoding="utf8").readlines():
    #         content = line.split("\t", maxsplit=1)[1]
    #         # 生成语料库
    #         word_dic = count_word(content)
    #         files_dic.append(word_dic)
    #
    # # 计算tf-idf,并将结果存入txt
    # for file in files_dic:
    #     tf_idf = count_tfidf(file, files_dic)
    #     print(tf_idf[0:4])


if __name__ == '__main__':
    option = "DF"
    main(option)
