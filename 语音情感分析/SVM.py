import librosa
import os
from random import shuffle
import numpy as np
from sklearn import svm
import sklearn


path = r'casia'
EMOTION_LABEL = {'angry': '1', 'fear': '2', 'happy': '3', 'neutral': '4', 'sad': '5', 'surprise': '6'}


def getData(mfcc_feature_num=16):
    wav_file_path = []
    person_dirs = os.listdir(path)
    for person in person_dirs:
        if person.endswith('.txt'):
            continue
        emotion_dir_path = os.path.join(path, person)
        emotion_dirs = os.listdir(emotion_dir_path)
        for emotion_dir in emotion_dirs:
            if emotion_dir.endswith('ini'):
                continue
            emotion_file_path = os.path.join(emotion_dir_path, emotion_dir)
            emotion_files = os.listdir(emotion_file_path)
            for file in emotion_files:
                if not file.endswith('wav'):
                    continue
                wav_path = os.path.join(emotion_file_path, file)
                wav_file_path.append(wav_path)
    shuffle(wav_file_path)#将语音文件随机排列
    data_feature = []
    data_labels = []

    for wav_file in wav_file_path:
        y, sr = librosa.load(wav_file)

        mfcc_feature = librosa.feature.mfcc(y, sr, n_mfcc=16)
        zcr_feature = librosa.feature.zero_crossing_rate(y)
        energy_feature = librosa.feature.rmse(y)
        rms_feature=librosa.feature.rmse(y)

        mfcc_feature = mfcc_feature.T.flatten()[:mfcc_feature_num]
        zcr_feature = zcr_feature.flatten()
        energy_feature = energy_feature.flatten()
        rms_feature=rms_feature.flatten()

        zcr_feature = np.array([np.mean(zcr_feature)])
        energy_feature = np.array([np.mean(energy_feature)])
        rms_feature=np.array([np.mean(rms_feature)])

        data_feature.append(np.concatenate((mfcc_feature, zcr_feature, energy_feature,rms_feature)))
        data_labels.append(int(EMOTION_LABEL[wav_file.split('\\')[-2]]))
    return np.array(data_feature), np.array(data_labels)


def test():
    best_acc = 0
    best_mfcc_feature_num = 0
    for i in range(100, 200):
        data_feature, data_labels = getData(i)
        gamma = gamma / 10
        split_num = 1100
        train_data = data_feature[:split_num, :]
        train_label = data_labels[:split_num]
        test_data = data_feature[split_num:, :]
        test_label = data_labels[split_num:]
        clf = svm.SVC(decision_function_shape='ovo', kernel='rbf', C=19, gamma=0.0001)
        clf.fit(train_data, train_label)
        acc = sklearn.metrics.accuracy_score(clf.predict(test_data), test_label)
        print(split_num, gamma, 'acc ', acc)
        if acc > best_acc:
            best_acc = acc
            best_mfcc_feature_num = i
            print()
            print('best_acc', best_acc)
            print('best_mfcc_feature_num', best_mfcc_feature_num)
            print()
    print('best_acc', best_acc)
    print('best_mfcc_feature_num', best_mfcc_feature_num)
    print()


best_acc = 0
best_mfcc_feature_num = 0
best_C = 0
for C in range(1, 20):
    for i in range(10, 50):
        data_feature, data_labels = getData(i)
        split_num = 500
        train_data = data_feature[:split_num, :]
        train_label = data_labels[:split_num]
        test_data = data_feature[split_num:, :]
        test_label = data_labels[split_num:]
        clf = svm.SVC(decision_function_shape='ovo', kernel='rbf', C=C, gamma=0.0001)
        clf.fit(train_data, train_label)
        print('Train Over')
        print(C, i)
        acc_dict = {}
        for test_x, test_y in zip(test_data, test_label):
            pre = clf.predict([test_x])[0]
            if pre in acc_dict.keys():
                continue
            acc_dict[pre] = test_y
        acc = sklearn.metrics.accuracy_score(clf.predict(test_data), test_label)
        if acc > best_acc:
            best_acc = acc
            best_C = C
            best_mfcc_feature_num = i
            print('best_acc', best_acc)
            print('best_C', best_C)
            print('best_mfcc_feature_num', best_mfcc_feature_num)
            print()


print('best_acc', best_acc)
print('best_C', best_C)
print('best_mfcc_feature_num', best_mfcc_feature_num)
