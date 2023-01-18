#自己写的，非自带，用于计算测试集准确度。
data_=open("sds1_predict/test_results.tsv",encoding='utf-8')
data=data_.readlines()
a=[]
for i in data:
    i=i.split("\t")
    i[4]=i[4].replace("\n","")
    if float(i[0])==max(float(i[0]),float(i[1]),float(i[2]),float(i[3]),float(i[4])):
        a.append('1')
    elif float(i[1])==max(float(i[0]),float(i[1]),float(i[2]),float(i[3]),float(i[4])):
        a.append('2')
    elif float(i[2]) == max(float(i[0]), float(i[1]),float(i[2]),float(i[3]),float(i[4])):
        a.append('3')
    elif float(i[3]) == max(float(i[0]), float(i[1]), float(i[2]),float(i[3]),float(i[4])):
        a.append('4')
    elif float(i[4]) == max(float(i[0]), float(i[1]), float(i[2]), float(i[3]),float(i[4])):
        a.append('5')
data2=open("data_set/sds_q1_test.txt",encoding='utf-8')
data2=data2.readlines()
b=[]
for i in range(len(data2)):
    data2[i]=data2[i].replace('\n','')
for i in data2:
    b.append(i[-1])
c=0
#print(a,b)
for i in range(len(a)):
    if a[i]==b[i]:
        c+=1
    else:
        print(i,",",a[i],b[i])
data_.close()
print(c/1040)
