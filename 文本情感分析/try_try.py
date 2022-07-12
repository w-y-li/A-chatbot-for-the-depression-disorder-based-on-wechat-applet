with open(r'C:\Users\dell\Desktop\bert-master\data_set\抑郁患者语录-测试.txt',encoding='utf-8')as f:
    readdata=f.readlines()
for i in range(len(readdata)):
    readdata[i]=readdata[i].split("，",1)
    if readdata[i][0]=='1':
        readdata[i][0]='positive'
    else:
        readdata[i][0]='negative'
with open(r'C:\Users\dell\Desktop\bert-master\data_set\test1.txt','w',encoding='utf-8') as F:
    for i in readdata:
        F.writelines(i[0]+','+i[1])
print(readdata)