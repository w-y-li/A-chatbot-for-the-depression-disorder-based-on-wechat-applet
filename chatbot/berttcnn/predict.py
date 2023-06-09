from berttcnn.model import BertTextModel_last_layer
from berttcnn.utils import MyDataset
from transformers import BertTokenizer
from torch.utils.data import DataLoader
import torch
from berttcnn.config import parsers
import time
import math
import argparse
import os.path


def load_model(model_path, device):
    model = BertTextModel_last_layer().to(device)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model


# def text_class_name(texts, pred, args):
#     results = torch.argmax(pred, dim=1)
#     results = results.cpu().numpy().tolist()
#     classification = open(args.classification, "r", encoding="utf-8").read().split("\n")
#     classification_dict = dict(zip(range(len(classification)), classification))
#     classname = " "
#     if len(results) != 1:
#         for i in range(len(results)):
#             print(f"文本：{texts[i]}\t预测的类别为：{classification_dict[results[i]]}")
#             classname = classification_dict[results[i]]
#     else:
#         print(f"文本：{texts}\t预测的类别为：{classification_dict[results[0]]}")
#         classname = classification_dict[results[0]]
#     return classname
def text_class_name(texts, pred, args):
    results = torch.argmax(pred, dim=1)
    continue_results = []
    for i in range(len(pred)):
        max_index = torch.argmax(pred[i])
        if max_index == 4:
            continue_results.append(-1)
        elif max_index == 0:
            dis1 = math.exp(pred[i][0]) / (math.exp(pred[i][0]) + math.exp(pred[i][1]))
            dis2 = math.exp(pred[i][1]) / (math.exp(pred[i][0]) + math.exp(pred[i][1]))
            if dis1 > 0.9:  # 0.9为超参数，待调。
                continue_results.append(0)
            elif dis2 > 0.9:
                continue_results.append(1)
            continue_results.append(0 * dis1 + 1 * dis2)
        elif max_index == 3:
            dis1 = math.exp(pred[i][3]) / (math.exp(pred[i][3]) + math.exp(pred[i][2]))
            dis2 = math.exp(pred[i][2]) / (math.exp(pred[i][3]) + math.exp(pred[i][2]))
            if dis1 > 0.9:
                continue_results.append(3)
            elif dis2 > 0.9:
                continue_results.append(2)
            continue_results.append(3 * dis1 + 2 * dis2)
        elif pred[i][max_index - 1] > pred[i][max_index + 1]:
            dis1 = math.exp(pred[i][max_index]) / (math.exp(pred[i][max_index]) + math.exp(pred[i][max_index - 1]))
            dis2 = math.exp(pred[i][max_index - 1]) / (math.exp(pred[i][max_index]) + math.exp(pred[i][max_index - 1]))
            if dis1 > 0.9:
                continue_results.append(max_index)
            elif dis2 > 0.9:
                continue_results.append(max_index - 1)
            continue_results.append(max_index * dis1 + (max_index - 1) * dis2)
        else:
            dis1 = math.exp(pred[i][max_index]) / (math.exp(pred[i][max_index]) + math.exp(pred[i][max_index + 1]))
            dis2 = math.exp(pred[i][max_index + 1]) / (math.exp(pred[i][max_index]) + math.exp(pred[i][max_index + 1]))
            if dis1 > 0.9:
                continue_results.append(max_index)
            elif dis2 > 0.9:
                continue_results.append(max_index + 1)
            continue_results.append(max_index * dis1 + (max_index + 1) * dis2)
    return continue_results


def pred_one(args, model, device, start):
    tokenizer = BertTokenizer.from_pretrained(parsers(0).bert_pred)
    text = "我们一起去打篮球吧！"
    encoded_pair = tokenizer(text, padding='max_length', truncation=True, max_length=args.max_len, return_tensors='pt')
    token_ids = encoded_pair['input_ids']
    attn_masks = encoded_pair['attention_mask']
    token_type_ids = encoded_pair['token_type_ids']

    all_con = tuple(p.to(device) for p in [token_ids, attn_masks, token_type_ids])
    pred = model(all_con)
    text_class_name(text, pred, args)
    end = time.time()
    print(f"耗时为：{end - start} s")


def scorepre(text, qnum):
    start = time.time()
    args = parsers(qnum)
    model = load_model(args.save_model_best, torch.device('cpu'))
    texts = text
    classname = []
    # print("模型预测结果：")
    # pred_one(args, model, device, start)  # 预测一条文本
    x = MyDataset(texts, 0, with_labels=False)
    xDataloader = DataLoader(x, batch_size=len(texts), shuffle=False)
    for batch_index, batch_con in enumerate(xDataloader):
        batch_con = tuple(p.to(torch.device('cpu')) for p in batch_con)
        pred = model(batch_con)
        # print(pred)
        classname.append(text_class_name(texts, pred, args))
    end = time.time()
    # print(f"耗时为：{end - start} s")
    return classname


def getpoint():
    sdspoint = {}
    for i in range(1, 21):
        sdspoint[f'{i}'] = 0
    sdsans_file = open(r"D:\sdsQA\chatbot\berttcnn\sdsans.txt", "r", encoding='utf8')
    for line in sdsans_file.readlines():
        if line == '':
            continue
        sdspoint[line[0]] = float(scorepre([line[2:].strip()], int(line[0]))[0][0])
    return sdspoint


# print(getpoint())
# print(int(scorepre(["有时候会"], 1)[0][0]))

