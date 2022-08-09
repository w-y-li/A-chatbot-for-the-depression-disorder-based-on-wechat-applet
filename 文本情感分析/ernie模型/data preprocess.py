import pandas as pd

# 转成tsv格式
file_path = r"E:\sdd chatbot\sentiment analysis\sentiment analysis -FINAL\dataset\抑郁患者语录-训练.txt"
text = open(file_path,'r', encoding='utf-8')
text=text.read().splitlines()

for i in range(len(text)):
    text[i]=text[i].split('，',1)
    text[i][1].replace(text[0][1][-1],'')
print(text)

result=pd.DataFrame(text)
for i in range(200):
    result[1][i].replace(result[1][i][-1],'',1)

result.to_csv(r'\sdd chatbot\sentiment analysis\sentiment analysis -FINAL\dataset\抑郁患者语录-验证.tsv',sep='\t',index=False, header=False)