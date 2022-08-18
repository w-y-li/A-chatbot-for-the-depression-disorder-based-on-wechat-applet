predict=[]
with open(r"C:\Users\dell\Desktop\ERNIE\applications\tasks\text_classification\output\predict_result.txt", "r" )as f:
    f=f.readlines()
    for i in range(len(f)):
        f[i]=f[i].strip()
        f[i]=f[i].split('\t')
        cls1=f[i][1].split(',')[0][1:]
        cls2 = f[i][1].split(',')[1][:-1]
        if(float(cls1)>float(cls2)):
            predict.append('0')
        else:
            predict.append('1')
real=[]
with open(r"C:\Users\dell\Desktop\ERNIE\applications\tasks\text_classification\data\test_data\test.txt",encoding='utf-8') as f:
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