# -*- coding: utf-8 -*-
# @Time    : 2019/11/8 11:17
# @Author  : tian
# @Email   : zengdetian@eefung.com
# @File    : 文本预测.py
# @Software: PyCharm
from sklearn.externals import joblib
import jieba

Data_path = "D:\数据\DATA\轻量敏感的数据_过滤.txt"

# 对新文本进行切词处理
stopwords = list()

with open("stop_words.txt", 'r', encoding='utf-8') as f:
    for word in f.readlines():
        stopwords.append(word[:-1])

Tf_idf_Model_save_path = "./tfidf_model.m"
tfidf_model = joblib.load(Tf_idf_Model_save_path)
lr_model = joblib.load('逻辑回归文本分类.model')   #加载模型

def predict_label(data):
    text_list = list()
    seg_text = jieba.cut(data)
    text = [word for word in seg_text if word not in stopwords]
    text_list.append(' '.join(text))

    X_test = tfidf_model.transform(text_list).toarray()
    result = lr_model.predict(X_test)
    print(result)
    return result


if __name__ == "__main__":
    Result_path = "分类结果/轻量敏感文本的分类结果.txt"
    f_w = open(Result_path, "w", encoding="utf8")

    Result_path1 = "分类结果/轻量敏感文本的分类结果-重敏感.txt"
    f_w1 = open(Result_path1, "w", encoding="utf8")

    Result_path2 = "分类结果/轻量敏感文本的分类结果-非敏感.txt"
    f_w2 = open(Result_path2, "w", encoding="utf8")

    for i, line in enumerate(open(Data_path, "r", encoding="utf8").readlines()):
        content = line.split("\t", maxsplit=1)[1]
        result = predict_label(content.strip())
        f_w.write(result[0] + "\t" + content)
        if result[0] == "重敏感":
            f_w1.write(result[0] + "\t" + content)
        else:
            f_w2.write(result[0] + "\t" + content)

    print("共处理完%d" % i)





