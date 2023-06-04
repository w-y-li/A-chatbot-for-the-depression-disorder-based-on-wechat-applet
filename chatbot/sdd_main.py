import openai
import sds_match.sds_match as sds
import csv
from datetime import datetime
import time
from gensim.models.word2vec import LineSentence, Word2Vec
from berttcnn import predict
import jieba
import warnings
import os
import situational_chat as sc

warnings.filterwarnings("ignore")


def gpt3(texts, usersname, flag):
    dfile = open(os.path.join(r"txt", usersname + ".txt"), "r", encoding='utf-8-sig')
    data = dfile.read().splitlines()
    dlist = []
    for i in range(0, len(data)):
        if i == 20:
            break
        if flag == 0:
            if data[len(data) - i - 1] == '' or data[len(data) - i - 1][0] == "聊" or data[len(data) - i - 1][0] == "b":
                continue
        dlist.insert(0, data[len(data) - i - 1])
    dfile.close()
    # openai.api_key = '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'
    openai.api_key = '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'
    completion = openai.ChatCompletion.create(  # Change the function Completion to ChatCompletion
        model='gpt-3.5-turbo',
        messages=[  # Change the prompt parameter to the messages parameter
            {'role': 'user',
             'content': f'现在你是一个名为爱小伴的情感聊天机器人，你的所有回复统一以bot：作为开头，下面是聊天历史记录:{dlist}，你要结合聊天历史记录进行回复，接下来你将会收到一句用户的话语，你将要对这句话进行回复, user：' + texts}
        ],
        temperature=0.9
    )
    if completion['choices'][0]['message']['content'][0] == "b":
        return completion['choices'][0]['message']['content']
    elif completion['choices'][0]['message']['content'][0] == "B":
        return completion['choices'][0]['message']['content']
    else:
        return "bot:" + completion['choices'][0]['message']['content']  # Change how you access the message content


jieba_preload = jieba.lcut("提前加载jieba")
model = Word2Vec.load(r"sds_match\wiki.model")
usersname = input("请输入用户名:")
hdfile = open(os.path.join(r"txt", usersname + ".txt"), "a+", encoding='utf-8-sig')
hdfile.write("聊天记录{}:\n".format(datetime.now()))
hdfile.close()
sdsfile = open(os.path.join(r"txt", "sds" + usersname + ".txt"), "a+", encoding='utf-8-sig')
sdsfile.close()
record_file = open(os.path.join(r"txt", "situ_" + usersname + ".txt"), "a+", encoding='utf-8-sig')
record_file.close()
ifsds = 1
ifans = 0
qnum = 0
ifask2 = 0
match_time = 0
re = 0
rd = 0
print("现在开始聊天，输入Z以退出")
while 1:
    sdsfile = open(os.path.join(r"txt", "sds" + usersname + ".txt"), "r", encoding='utf-8-sig')
    hdfile = open(os.path.join(r"txt", usersname + ".txt"), "a+", encoding='utf-8-sig')
    sdslist = sdsfile.read().splitlines()
    sdscount = []
    for i in range(len(sdslist)):
        if sdslist[i] == '':
            continue
        sdscount.append(sdslist[i].split(':', 1)[0])
    sdsfile.close()
    sdsfile = open(os.path.join(r"txt", "sds" + usersname + ".txt"), "a+", encoding='utf-8-sig')
    starttime = datetime.now()
    text = input("user：")
    endtime = datetime.now()
    duringtime = starttime - endtime
    if text == "Z":
        hdfile.close()
        sdsfile.close()
        break
    hdfile.write("user:" + text + "\n")
    if len(text) < 10 and match_time >= 10:   #duringtime.seconds >= 7 and
        botans = gpt3(text, usersname, ifans)
        response, re = sc.conversation(botans, sdscount, re, usersname)
        match_time=0
        print(response)
        hdfile.write(response + "\n")
        hdfile.close()
        sdsfile.close()
        continue
    if ifans == 1:
        checkans = int(predict.scorepre([text], qnum)[0][0])
        if checkans == -1 and ifask2 == 0:
            ifans = 1
            num = qnum - 1
            rdnum = rd % 6 + 3
            rd += 1
            with open(r"sds量表及回复改写\SDS.csv", encoding='gb2312') as f:
                reader = csv.reader(f, skipinitialspace=True)
                for row in reader:
                    num -= 1
                    if num == -2:
                        qlist = row
            qtext = qlist[rdnum]
            time.sleep(3)
            print("bot:" + qtext)
            hdfile.write("bot:" + qtext + "\n")
            hdfile.close()
            sdsfile.close()
            # ifsds = 0
            ifask2 = 1
            f.close()
            continue
        else:
            if checkans != -1:
                sdsfile.write(f"{qnum}:" + text + "\n")
            ifans = 0
            ifsds = 0
    if ifsds == 1:
        ifsame = 0
        qsim, num = sds.sds_match(text, model)
        qnum = num + 1
        for i in range(len(sdscount)):
            if qnum == int(sdscount[i]):
                ifsame = 1
        if qsim > 0.5 and ifsame == 0:
            botans = gpt3(text, usersname, ifans)
            rdnum = rd % 6 + 3
            rd += 1
            with open(r"sds量表及回复改写\SDS.csv", encoding='gb2312') as f:
                reader = csv.reader(f, skipinitialspace=True)
                for row in reader:
                    num -= 1
                    if num == -2:
                        qlist = row
            qtext = qlist[rdnum]
            time.sleep(5)
            print('bot:' + qtext)
            hdfile.write('bot:' + qtext + "\n")
            hdfile.close()
            sdsfile.close()
            ifans = 1
            match_time = 0
            # ifsds = 0
            ifask2 = 0
            f.close()
            continue
    botans = gpt3(text, usersname, ifans)
    print(botans)
    ifsds = 1
    match_time += 1
    hdfile.write(botans + "\n")
    hdfile.close()
    sdsfile.close()
