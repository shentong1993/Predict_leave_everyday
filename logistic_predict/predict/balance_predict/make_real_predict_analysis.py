import csv
import numpy as np
import random
import os
from sklearn import linear_model

def generate_analysis_name_dic():

    analysis_name_dic= {}

    for day_len in range(1,27):
        temp_list = []
        temp_list.append('label')

        feature_map = ['lastLabel1', 'apply_Id', 'age', 'gender', 'week0Weight', 'week0Height']

        for day in range(1, day_len + 1):
            feature_map.append('day%dWeight' % day)
            feature_map.append('breakfast%d' % day)
            feature_map.append('lunch%d' % day)
            feature_map.append('dinner%d' % day)
            feature_map.append('trainning%d' % day)
            feature_map.append('speak%d' % day)
            feature_map.append('greed%d' % day)
            feature_map.append('pressure%d' % day)
            feature_map.append('menstrual%d' % day)
        temp_list += feature_map
        analysis_name_dic['day%d'%day_len] = temp_list

    return analysis_name_dic




# analysis_name_dic={'day1':[]}


def processData(filePath):
    dataList = []

    with open(filePath, 'r') as f:
        records = f.readlines()

        # 读第一行获取每一列的列名
        # strip() 去掉行尾的换行符

        # print(records[0].strip().split(','))
        # print(type(records[0]))

        keys = records[0].strip().split(',')

        for i, record in enumerate(records):
            if i > 0:
                dic = {}
                values = record.strip().split(',')
                for index, key in enumerate(keys):
                    dic[key] = float(values[index])

                dataList.append(dic)

    return dataList

# 形成 数据 和 标签 的数据结构
def generate_data_and_label( file_path,day_len):
    #label,week0Height,day1Weight,breakfast1,lunch1,dinner1,trainning1,speak1,greed1,pressure1,menstrual1
    # feature_map = ['week0Height','day1Weight','breakfast1','lunch1','dinner1','trainning1','speak1','greed1','pressure1','menstrual1']

    #/train_data/train_data_with_lastLabel/1day_data.csv
    # data_list = processData('../../train_data/train_data_with_lastLabel/%dday_data.csv'%day_len)
    data_list = processData(file_path)


#label,lastLabel1,apply_Id,age,gender,week0Weight,week0Height,day1Weight,breakfast1,lunch1,dinner1,trainning1,speak1,greed1,pressure1,menstrual1

    feature_map = ['lastLabel1','apply_Id','age','gender','week0Weight','week0Height']

    for day in range(1,day_len+1):
        feature_map.append('day%dWeight'%day)
        feature_map.append('breakfast%d'%day)
        feature_map.append('lunch%d'%day)
        feature_map.append('dinner%d'%day)
        feature_map.append('trainning%d'%day)
        feature_map.append('speak%d'%day)
        feature_map.append('greed%d'%day)
        feature_map.append('pressure%d'%day)
        feature_map.append('menstrual%d'%day)

    trainDatas = []
    trainLabels = []

    for person in data_list:
        data = []
        for feature in feature_map:
            data.append(person[feature])

        trainDatas.append(data)
        trainLabels.append(person['label'])



    return trainDatas, trainLabels



def generate_balance_data(trainDatas, trainLabels,day_len):

    trainDatas_array = np.array(trainDatas)
    trainLabels_array = np.array(trainLabels)

    # print('label 1 = ',np.sum(trainLabels_array== 1))
    # print('label 0 = ',np.sum(trainLabels_array== 0))



    label_1_position =  np.where(trainLabels_array == 1)[0]
    label_1_position_list = label_1_position.tolist()
    len_label_1 = len(label_1_position_list)

    label_0_position = np.where(trainLabels_array == 0)[0]
    label_0_position_list = label_0_position.tolist()
    len_label_0 = len(label_0_position_list)

    random.seed(10)
    balance_label_1_position_list = random.sample(label_1_position_list , len_label_0)



    balance_position_of_1_and_0 = label_0_position_list +balance_label_1_position_list

    random.shuffle(balance_position_of_1_and_0)

    balance_train_datas = [trainDatas[pos] for pos in balance_position_of_1_and_0]
    balance_train_labels = [trainLabels[pos] for pos in balance_position_of_1_and_0]



    return balance_train_datas , balance_train_labels




def generateClf(trainDatas , trainLabels):

    trainDatas = [person[6:] for person in trainDatas]

    clf = linear_model.LogisticRegression()
    clf.fit(trainDatas, trainLabels)

    return clf




def test_accuracy1(clf, trainDatas, trainLabels, day_len):
    analysis_name_dic = generate_analysis_name_dic()

    num_data = len(trainLabels)

    trainLabels_num_0 = np.sum(np.array(trainLabels) == 0)
    trainLabels_num_1 = np.sum(np.array(trainLabels)==1)


    acc_count = 0
    acc_count_0 =0
    acc_count_1 = 0

    real0_predict0_list = []
    real0_predict1_list = []
    real1_predict0_list = []
    real1_predict1_list = []
    all_real1_predict0_list = []

    for i in range(num_data):
        predict_label = clf.predict(  [trainDatas[i][6:]])

        person_list = []

        if predict_label == trainLabels[i]:
            acc_count += 1

            if trainLabels[i]==0:
                acc_count_0 += 1

                person_list.append(trainLabels[i])
                person_list = person_list + trainDatas[i]
                real0_predict0_list.append(person_list)

            elif trainLabels[i] ==1 :
                acc_count_1 += 1

                person_list.append(trainLabels[i])
                person_list = person_list + trainDatas[i]
                real1_predict1_list.append(person_list)
        else:

            if trainLabels[i] == 0:
                person_list.append(trainLabels[i])
                person_list = person_list + trainDatas[i]
                real0_predict1_list.append(person_list)
            else:
                person_list.append(trainLabels[i])
                person_list = person_list + trainDatas[i]
                all_real1_predict0_list.append(person_list)

                #只有lastLabel1 >=22 , 也就是待到23-28天的 ，才开始分析 ,1-22天跑的不分析
                if trainDatas[i][0] >=22:
                    person_list = []
                    person_list.append(trainLabels[i])
                    person_list = person_list + trainDatas[i]
                    real1_predict0_list.append(person_list)

    file_path = './data/day%d'%day_len
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    with open(os.path.join(file_path,"real0_predict0_list.csv"), "w+", encoding='utf8') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(analysis_name_dic['day%d'%day_len])

        for i in range(len(real0_predict0_list)):
            writer.writerow(real0_predict0_list[i])

    with open(os.path.join(file_path, "real0_predict1_list.csv"), "w+",encoding='utf8') as csvfile:

        writer = csv.writer(csvfile)
        writer.writerow(analysis_name_dic['day%d'%day_len])


        for i in range(len(real0_predict1_list)):
            writer.writerow(real0_predict1_list[i])

    with open(os.path.join(file_path, "real1_predict0_list.csv"), "w+", encoding='utf8') as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow(analysis_name_dic['day%d'%day_len])


        for i in range(len(real1_predict0_list)):
            writer.writerow(real1_predict0_list[i])

    with open(os.path.join(file_path, "real1_predict1_list.csv"), "w+", encoding='utf8') as csvfile:

        writer = csv.writer(csvfile)

        writer.writerow(analysis_name_dic['day%d'%day_len])


        for i in range(len(real1_predict1_list)):
            writer.writerow(real1_predict1_list[i])

    # print ('accuracy = ', acc_count / num_data *100 ,'%')
    print('负样本预测对了 = ',acc_count_0,'负样本召回率 = ', round(acc_count_0/ trainLabels_num_0 *100,2) ,'%')
    print('正样本预测错了 = ',trainLabels_num_1 - acc_count_1 ,'正样本召回率 = ',round(acc_count_1/trainLabels_num_1 *100 ,2),'%' )

    #统计正样本预测错的 ，都是真正哪一天离开的 ， 1-23 天不算预测错
    num_real1_predict0 = len(all_real1_predict0_list)
    leave_dic ={}
    for time in range(28):
        leave_dic[time] = 0

    for person in all_real1_predict0_list:
        leave_day = person[1]
        leave_dic[leave_day] += 1
    #这是聊起来有价值的人 ,1-23天跑
    value = 0
    for time in range(22):
        value += leave_dic[time]

    not_value = num_real1_predict0 - value

    print('正样本预测错的%d-23天离开的 ='%day_len,value,'人','剩余人数 =',not_value,'人， 正样本有价值的召回率 =',round((acc_count_1+value)/trainLabels_num_1 *100 ,2),'%')





if __name__ == '__main__':

    # for day_len in range(1,27):
    for day_len in range(1, 27):

        print('day = ',day_len)
        # data_list = processData('../../train_data/train_data_with_lastLabel/%dday_data.csv'%day_len)
        #/Users/shen/PycharmProjects/Predict_leave/data/train_data_with_lastLabel/1day_data.csv
        file_path = '../../../data/weight_dataset/train_data_with_lastLabel/%dday_data.csv'%day_len

        trainDatas, trainLabels = generate_data_and_label(file_path, day_len)

        #使正样本和负样本同样多
        balance_trainDatas , balance_trainLabels  = generate_balance_data(trainDatas, trainLabels, day_len)


        clf = generateClf(balance_trainDatas , balance_trainLabels)

        test_accuracy1(clf,  trainDatas, trainLabels , day_len)

        print('\n'*3)











