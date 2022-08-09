#自己写的，非自带，用于计算测试集准确度。
data_=open(r"C:\Users\dell\Desktop\bert-master\senti_predict\test_results.tsv",encoding='utf-8')
data=data_.readlines()
a=[]
for i in data:
    i=i.split("\t")
    i[2]=i[2].replace("\n","")
    if float(i[0])==max(float(i[0]),float(i[1]),float(i[2])):
        a.append('-1')
    elif float(i[1])==max(float(i[0]),float(i[1]),float(i[2])):
        a.append('0')
    elif float(i[2]) == max(float(i[0]), float(i[1]),float(i[2])):
        a.append('1')
data2=open(r"C:\Users\dell\Desktop\bert-master\data_set\抑郁患者语录-测试.txt",encoding='utf-8')
data2=data2.readlines()
b=[]
for i in data2:
    i=i.split("，",1)
    b.append(i[0])
c=0
#print(a,b)
for i in range(len(a)):
    if a[i]==b[i]:
        c+=1
data_.close()
print(c/200)
