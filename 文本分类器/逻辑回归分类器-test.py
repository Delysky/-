# -*- coding: utf-8 -*-
# @Time    : 2019/11/6 13:25
# @Author  : tian
# @Email   : zengdetian@eefung.com
# @File    : 逻辑回归分类器.py
# @Software: PyCharm
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

def constructDataset(path):
    """
    path: file path 分别构建标签和语料数据集
    rtype: lable_list and corpus_list
    """
    label_list = []
    corpus_list = []
    with open(path, 'r', encoding="utf8") as p:
        for line in p.readlines():
            label_list.append(line.split('\t')[0])
            corpus_list.append(line.split('\t')[1])
    return label_list, corpus_list


Train_cut_path = "D:\数据\DATA\重敏感与非敏感的数据_train_cut.txt"
Val_cut_path = "D:\数据\DATA\重敏感与非敏感的数据_val_cut.txt"

Tf_idf_Model_save_path = "./tfidf_model.m"

write_list = [Train_cut_path, Val_cut_path]
train_label, train_set = constructDataset(write_list[0])  # 50000
val_label, val_set = constructDataset(write_list[1])

train_num = len(train_set)
val_num = len(val_set)

# 计算tf-idf
corpus_set = train_set + val_set  # + test_set  # 全量计算tf-idf
print("length of corpus is: " + str(len(corpus_set)))

#用TF-IDF算法来抽取短信的特征向量
vectorizer = TfidfVectorizer(max_df=1.0, min_df=1e-3)


Total_train = vectorizer.fit_transform(corpus_set)
X_train = Total_train[:train_num]
X_val = Total_train[train_num:]
# # 取X的后两句用上句生成的tfidf做转换
joblib.dump(vectorizer, Tf_idf_Model_save_path)


print("tf-idf shape: ({0},{1})".format(X_train.shape[0], X_train.shape[1]))

# lr是一个LogisticRegression模型
lr_model = LogisticRegression(penalty="l2")  # 'balanced' class_weight={0:0.75,1:0.25}  , max_iter=100000, tol=1e-11,
lr_model.fit(X_train, train_label)
# print("val mean accuracy: {0}".format(lr_model.score(val_set, val_label)))
y_pred_train = lr_model.predict(X_train)
print("-----------------train训练集------------------------")
print(classification_report(train_label, y_pred_train))
print(confusion_matrix(train_label, y_pred_train))
# print(lr_model.score(X, y))

print("-----------------val验证集--------------------------")
y_pred = lr_model.predict(X_val)
print(classification_report(val_label, y_pred))
print(confusion_matrix(val_label, y_pred))

joblib.dump(lr_model, '逻辑回归文本分类.model')



# 0---敏感   1---非敏感   将分类的结果分别写入四个不同的文件
fw1 = open("分类结果/正确分类的敏感文本.txt", "w", encoding="utf8")
fw2 = open("分类结果/错误分成敏感文本的非敏感文本.txt", "w", encoding="utf8")
fw3 = open("分类结果/错误分成非敏感文本的敏感文本.txt", "w", encoding="utf8")
fw4 = open("分类结果/正确分类的非敏感文本", "w", encoding="utf8")


for i, item in enumerate(y_pred):
    # if i == 1:
    #     print("debug")
    if item == "重敏感" and val_label[i] == "重敏感":   # 正确分类的敏感文本
        fw1.write(str(i+1) + " " + val_set[i])
        fw1.flush()
    elif item == "重敏感" and val_label[i] == "非敏感":  # 错误分成敏感文本的非敏感文本
        fw2.write(str(i+1) + " " + val_set[i])
        fw2.flush()
    elif item == "非敏感" and val_label[i] == "重敏感":  # 错误分成非敏感文本的敏感文本
        fw3.write(val_set[i])
        fw3.flush()
    elif item == "非敏感" and val_label[i] == "非敏感":  # 正确分类的非敏感文本
        # print(i)
        fw4.write(str(i) + " " + val_set[i])
        fw4.flush()


'''
y_preds = lr_model.predict(X_test)
print(y_preds)

f_result = open("competition_result.csv", "w", encoding="utf8")
test_label_list

i = 0
for i, item in enumerate(y_preds):
    f_result.write(test_label_list[i]+'\t'+item+'\n')
# print(i)
'''

if __name__ == "__main__":
    pass




