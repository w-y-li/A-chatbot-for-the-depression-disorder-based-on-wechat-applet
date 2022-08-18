predict=[]
with open(r"output\predict_result.txt", "r" )as f:
    f=f.readlines()
    for i in range(len(f)):
        f[i]=f[i].strip()
        f[i]=f[i].split('\t')
        cls1=f[i][1].split(',')[0][1:]
        cls2 = f[i][1].split(',')[1]
        cls3 = f[i][1].split(',')[2][:-1]
        if(float(cls1)>float(cls2) and float(cls1)>float(cls3)):
            predict.append('0')
        elif (float(cls2)>float(cls1) and float(cls2)>float(cls3)):
            predict.append('1')
        else:
            predict.append('2')
real=[]
with open(r"data\test_data\test.txt",encoding='utf-8') as f:
    f=f.readlines()
    for i in range(len(f)):
        f[i]=f[i].strip()
        f[i] = f[i].split('\t')
        real.append(f[i][1])
        print(real)
right=0
for i in range(len(real)):
    if real[i]==predict[i]:
        right+=1
print(right/200)