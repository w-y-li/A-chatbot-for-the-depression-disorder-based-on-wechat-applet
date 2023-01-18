'''
步骤一：根据用户回复选择合适的量表问题，实现方法：首先将二十个问题与用户回复进行分词，
去除停用词后每一句都变成了一串关键词的组合，再根据wiki中文百科数据训练一个word2vec
模型，利用该模型对每个关键词都进行向量转化，并计算每个用户回复关键词与sds问题关键词的
余弦相似度。由于反义仍代表其具有相关性，故对余弦相似度取绝对值并储存。最后采用如下策略
选定最终sds问题：对每个sds问题，将用户回复的每个关键词分别与该sds问题的所有关键词相
似度相比较取并最大值储存，作为该sds问题下用户该关键词的得分。将每个前述得分进行求均值
作为该sds问题的得分（注意没有对应向量的特殊情况），选择分数最高的sds问题即可。
'''

import jieba
from gensim.models.word2vec import LineSentence, Word2Vec

def sdstextprocess(file_path,stopwords):
    with open(file_path, encoding='utf-8') as f:
        file_data = f.readlines()
        for i in range(len(file_data)):
            file_data[i] = file_data[i].split('.')[1]
            file_data[i]=file_data[i].rstrip()
            for j in ',"，。；：！·？/\~%$#@——- ':
                file_data[i] = file_data[i].replace(j, '')
            a = jieba.lcut(file_data[i])
            file_data[i] = a

        for i in range(len(file_data)):
            for j in range(len(stopwords)):
                for k in range(len(file_data[i])):
                    if file_data[i][k] == stopwords[j]:
                        file_data[i][k] = ''
            j=0
            while (j < len(file_data[i])):
                if (file_data[i][j] == ''):
                    del file_data[i][j]
                else:
                    j += 1
        return file_data

def usertextprocess(user_data,stopwords):
    for i in ',"，。；：！·？/\~%$#@——- =[]{}()|^&*-+~`':
        user_data = user_data.replace(i, '')
    user_data = jieba.lcut(user_data)

    for j in range(len(stopwords)):
        for k in range(len(user_data)):
            if user_data[k] == stopwords[j]:
                user_data[k] = ''
    i=0
    while (i < len(user_data)):
        if (user_data[i] == ''):
            del user_data[i]
        else:
            i += 1

    return user_data

def get_custom_stopwords(stop_words_file):
    with open(stop_words_file,encoding='utf-8') as f:
        stopwords = f.read()
    stopwords_list = stopwords.split('\n')
    custom_stopwords_list = [i for i in stopwords_list]
    return custom_stopwords_list

def word2vec(path):
    sentences = LineSentence(path)# path为要训练的txt的路径,txt中语料要是分过词的，以空格分开
    # 对sentences表示的语料库进行训练，训练200维的词向量，窗口大小设置为5，最小词频设置为5
    model = Word2Vec(sentences, vector_size=200, window=5, min_count=2)
    model.save("word2vec_model.model")#model_path为模型路径。保存模型，通常采用pkl形式保存，以便下次直接加载即可

def get_sim(sdsq,user,sim_mat):
    # 加载模型
    model = Word2Vec.load("wiki.model")
    for i in range(len(sdsq)):
        for j in range(len(user)):
            for k in range(len(sdsq[i])):
                try:
                    sim=model.wv.similarity(user[j],sdsq[i][k])
                    sim_mat[i][j].append(abs(sim))
                    #print(user[k],'and',sdsq[i][j],':',sim)
                except:
                    sim_mat[i][j].append(-1)
                    #print(sdsq[i][k])

def get_sdsq(sim_mat):
    resultlist=[]
    for i in range(len(sim_mat)):
        q_scorelist=[]
        for j in range(len(sim_mat[i])):
            temp=[]
            for k in range(len(sim_mat[i][j])):
                temp.append(sim_mat[i][j][k])
            q_scorelist.append(max(temp))
        resultlist.append(sum(q_scorelist)/(len(q_scorelist)-q_scorelist.count(-1)))
    return resultlist.index(max(resultlist))


def sds_match():
    stop_words_file = "哈工大停用词表.txt"

    stopwords = get_custom_stopwords(stop_words_file)
    sdsq = sdstextprocess("SDS问题.txt", stopwords)
    user = usertextprocess('我现在心情有点难过，因为篮球比赛输掉了', stopwords)
    sim_mat=[]
    for i in range(20):
        sim_mat.append([])
        for j in range(len(user)):
            sim_mat[i].append([])

    get_sim(sdsq,user,sim_mat)
    sds_qnum=get_sdsq(sim_mat)

    return sds_qnum

sds_match()
#word2vec(r"C:\Users\dell\Desktop\tempw.txt")