import paddlehub as hub
import pandas as pd

if __name__ == '__main__':
    file_path = "dataset/抑郁患者语录-测试.tsv"
    text = pd.read_csv(file_path, sep="\t", header=None)
    data = [[i] for i in text[1]]
    label_map = {0: -1,1:0 ,2: 1}

    model = hub.Module(name='ernie', task='seq-cls',
                       load_checkpoint='ernie_checkpoint2/epoch_2/model.pdparams', label_map=label_map)
    results = model.predict(data, max_seq_len=128, batch_size=16)

    # 输出测试集准确率
    count = 0
    for i, j in zip(text[0], results):
        #print(i,j)
        if int(i) == int(j):
            count += 1

    print("测试集准确率", count / len(results))