import random

data_=open("data_set/sds_q1_train.txt",encoding='utf-8')
data=data_.readlines()
random.shuffle(data)
wdata=open("data_set/1.txt",'w',encoding='utf-8')
for i in range(len(data)):
    wdata.write(data[i])