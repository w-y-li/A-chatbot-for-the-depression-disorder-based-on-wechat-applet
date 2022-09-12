import run_infer
from erniekit.utils import args

def get_results(filepath):#-1为负向情感，0为中性，1为正向情感
    result=[]
    with open( filepath,"r") as f:#；此处路径为结果的保存路径
        f = f.readlines()
        for i in range(len(f)):
            f[i] = f[i].strip()
            f[i] = f[i].split('\t')
            cls1 = f[i][1].split(',')[0][1:]
            cls2 = f[i][1].split(',')[1]
            cls3 = f[i][1].split(',')[2][:-1]
            if (float(cls1) > float(cls2) and float(cls1) > float(cls3)):
                result.append({'sentiment':-1, 'degree':cls1})
            elif (float(cls2) > float(cls1) and float(cls2) > float(cls3)):
                result.append({'sentiment': 0, 'degree': cls2})
            else:
                result.append({'sentiment':1, 'degree':cls3})
    return result

def get_prediction():#一定要先运行此函数获取预测结果
    run_infer.main(args)
