# -*- coding: utf-8 -*-
# @Time    : 2019/11/6 11:39
# @Author  : tian
# @Email   : zengdetian@eefung.com
# @File    : 构建向量空间.py
# @Software: PyCharm

import re
import jieba

Train_path = "D:\数据\DATA\重敏感与非敏感的数据_train.txt"
Val_path = "D:\数据\DATA\重敏感与非敏感的数据_val.txt"
stop_words = [line.strip() for line in open("stop_words.txt", "r", encoding="utf8") if line != ""]
Train_cut_path = "D:\数据\DATA\重敏感与非敏感的数据_train_cut.txt"
Val_cut_path = "D:\数据\DATA\重敏感与非敏感的数据_val_cut.txt"

def tokenFile(file_path, write_path):
    # 构建词的tf-idf向量空间
    with open(write_path, 'w', encoding="utf8") as w:
        with open(file_path, 'r', encoding="utf8") as f:
            for line in f.readlines():
                line = line.strip()
                if len(line.split('\t')) > 1:
                    # 将一篇文章分句子，来进行分词
                    token_sen = []
                    content = line.split('\t')[1]

                    pattern = r'；|？|!|。|；|！|…| |  '
                    contents = re.split(pattern, content)

                    # contents = content.split("(。|.|?| )")
                    for temp in contents:
                        if len(temp) > 0:
                            token_sen.extend(jieba.cut(temp))

                    res= ""
                    temp1 = []
                    for word in token_sen:
                        if word not in stop_words:
                            # res = " ".join(word)
                            temp1.append(word)
                    for word1 in temp1:
                        res += word1+ " "
                    print(res)
                    w.write(line.split('\t')[0] + '\t' + res + '\n')
    print(file_path + ' has been token and token_file_name is ' + write_path)


if __name__ == "__main__":
    tokenFile(Train_path, Train_cut_path)
    tokenFile(Val_path, Val_cut_path)
