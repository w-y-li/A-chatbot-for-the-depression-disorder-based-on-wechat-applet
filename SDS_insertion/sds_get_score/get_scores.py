data_=open("sds1_predict/test_results.tsv",encoding='utf-8')
data=data_.readlines()
scores=[]
for i in range(len(data)):
    data[i]=data[i].split("\t")
    del data[i][-1]
    for j in range(len(data[i])):
        data[i][j]=float(data[i][j])

for i in range(len(data)):
    if max(data[i])>=0.75:
        scores.append(data[i].index(max(data[i]))+1)
    else:
        temp=sorted(data[i])
        p1=temp[-1]/(temp[-1]+temp[-2])
        p2=temp[-2]/(temp[-1]+temp[-2])
        score=p1*(data[i].index(temp[-1])+1)
        score += p2 * (data[i].index(temp[-2])+1)
        scores.append(score)
        print(i)
print(scores)