from nltk.corpus import stopwords
import string
from nltk.stem import SnowballStemmer
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import heapq
import math
import pandas as pd


def create_stop_words():
    stop = stopwords.words('english')
    for i in range(97, 123):
        stop.append(chr(i))
    file_object = open('common-english-words.txt')
    try:
        file_context = file_object.read()
    finally:
        file_object.close()
    stopwords_list = file_context.split(',')
    for s in stopwords_list:
        stop.append(s)
    stop = set(stop)
    return stop


def clean(data):
    # print(data)
    data = data.lower()
    # remove punctuation
    punc_free = []
    for ch in data:
        if ch not in string.punctuation:
            punc_free.append(ch)
        else:
            punc_free.append(' ')
    punc_free = ''.join(punc_free)
    # print("punc_free", punc_free)
    punc_free = punc_free.split()
    # get stop words
    stop = create_stop_words()
    # remove stop words

    stop_free = []
    for word in punc_free:
        if word not in stop:
            stop_free.append(word)
    stop_free = " ".join(stop_free)

    # print("stop_free", stop_free)

    # stemming
    snowball_stemmer = SnowballStemmer("english")
    stemming = " ".join(snowball_stemmer.stem(word) for word in stop_free.split())
    # print(stemming)
    return stemming


def vector_query(dic, queries):
    query_v = []
    for q in queries:
        query = np.zeros([1, len(dic)])
        for word in q:
            try:
                id = dic.index(word)
                query[0][id] += 1
            except:
                pass
        query_v.append(query)
    return query_v


def mapper_query(S, u, v, query_v):
    S = np.linalg.inv(S)
    query_m = []
    for q in query_v:
        q_m = np.dot(np.dot(q, u), S)
        query_m.append(q_m)
    return query_m


def vector_d(v):
    d_list = []
    for vector in v:
        d_list.append(vector)
    return np.array(d_list)


def cosine(q, d):
    # denominator = math.sqrt(np.sum([q[i] ** 2 for i in range(len(q))])) * math.sqrt(sum([d[i] ** 2 for i in range(len(d))]))
    denominator = np.linalg.norm(q) * np.linalg.norm(d)
    numerator = np.sum(np.multiply(q, d))
    # numerator = np.dot(q, d)
    return numerator / denominator


def SVD_decomposition(matrix):
    d = 25
    u, s, v = np.linalg.svd(matrix)
    u = u[:, :d]
    S = np.zeros([d, d])
    for i in range(d):
        S[i][i] = s[i]
    v = v[:d, :]
    # (d.shape)
    # print(np.dot(np.dot(u,S),v))
    # print(v.shape)
    return S, u, v


def term_document_matrix_query(data, query, type):
    vectorizer = None
    if type == 1:
        vectorizer = CountVectorizer()
    elif type == 2:
        vectorizer = TfidfVectorizer()

    X = vectorizer.fit_transform(data)  # TD Matrix
    X_dic = vectorizer.get_feature_names()
    TD_matrix = np.array(X.toarray()).T

    # vectorize query
    query_v = [vectorizer.transform([q]).toarray() for q in query]

    # SVD - 25d
    S, u, v = SVD_decomposition(TD_matrix)

    # mapper vector to new feature space
    query_m = mapper_query(S, u, v, query_v)

    d_list = vector_d(v.T)
    res = []
    for q in query_m:
        similarity = []
        for d in d_list:
            similarity.append(cosine(q, d))
        # find top 3
        top3max_index = list(map(similarity.index, heapq.nlargest(3, similarity)))
        top3max_index = [index + 1 for index in top3max_index]
        res.append(top3max_index)

    return TD_matrix, X_dic, res


def main():
    # load doc and query data
    data = load_data()
    query = load_query()

    # pre-processing
    data_clean = [clean(info) for info in data]

    # Count
    TD_matrix, dic_matrix, res = term_document_matrix_query(data_clean, query, 1)

    print(res)

    TD = pd.DataFrame(data=TD_matrix, index=dic_matrix, columns=range(1, 36))
    TD.to_csv('TD.csv')

    # TF-IDF
    TD_matrix, dic_matrix, res = term_document_matrix_query(data_clean, query, 2)

    print(res)

    TD_TFIDF = pd.DataFrame(data=TD_matrix, index=dic_matrix, columns=range(1, 36))
    TD_TFIDF.to_csv('TD-TFIDF.csv')


def load_data():
    path = ".\\files\\"
    s = []
    for i in range(35):
        filepath = path + "file-" + str(i + 1) + ".txt"
        with open(filepath, 'r') as file:
            s.append(file.read().replace('\n', ''))
    return s


def load_query():
    path = ".\\querys\\"  # 文件夹目录
    q = []
    for i in range(6):
        filepath = path + "query-" + str(i + 1) + ".txt"
        with open(filepath, 'r') as file:
            q.append(file.read().replace('\n', ''))
    return q


if __name__ == '__main__':
    main()

