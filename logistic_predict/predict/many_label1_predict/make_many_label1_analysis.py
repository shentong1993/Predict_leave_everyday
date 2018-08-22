import csv
import os
import numpy as np
import random
import math
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

# 形成数据和标签的数据结构
def generate_data_and_label(file_path, day_len):
    #label,week0Height,day1Weight,breakfast1,lunch1,dinner1,trainning1,speak1,greed1,pressure1,menstrual1
    # feature_map = ['week0Height','day1Weight','breakfast1','lunch1','dinner1','trainning1','speak1','greed1','pressure1','menstrual1']

    # data_list = processData('../../train_data/train_data_with_lastLabel/%dday_data.csv'%day_len)
    data_list = processData(file_path)


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


# 为多个分类器生成各自的数据集
def generate_balance_data(trainDatas, trainLabels,day_len, num_of_label1_list):

    trainDatas_array = np.array(trainDatas)
    trainLabels_array = np.array(trainLabels)

    print('label 1 = ',np.sum(trainLabels_array== 1))
    print('label 0 = ',np.sum(trainLabels_array== 0))

    label_1_position =  np.where(trainLabels_array == 1)[0]
    label_1_position_list = label_1_position.tolist()
    len_label_1 = len(label_1_position_list)

    label_0_position = np.where(trainLabels_array == 0)[0]
    label_0_position_list = label_0_position.tolist()
    len_label_0 = len(label_0_position_list)

    total_train_Datas_List = []
    total_train_Labels_List =[]

    random.seed(10)

    for i in range(num_of_label1_list):
        balance_label_1_position_list = random.sample(label_1_position_list , len_label_0)


        balance_position_of_1_and_0 = label_0_position_list + balance_label_1_position_list
        random.shuffle(balance_position_of_1_and_0)

        balance_train_datas = [trainDatas[pos] for pos in balance_position_of_1_and_0]
        balance_train_labels = [trainLabels[pos] for pos in balance_position_of_1_and_0]


        total_train_Datas_List.append(balance_train_datas)
        total_train_Labels_List.append(balance_train_labels)

    return total_train_Datas_List,total_train_Labels_List


# 生成多个分类器，并装入列表
def generateClf(total_train_Datas_List , total_train_Labels_List):

    clf_list = []

    clf_num = len(total_train_Datas_List)

    for i in range(clf_num):
        # 拿掉新加的 lastLabel 这个维度
        new_train_Datas_list = [person[6:] for person in total_train_Datas_List[i]]

        clf = linear_model.LogisticRegression()
        clf.fit(np.array(new_train_Datas_list), np.array(total_train_Labels_List[i] ))
        clf_list.append(clf)

    return clf_list


def logistic_self(x, w , b):
    y = 0
    for i in range(len(x)):
        y += w[0][i] * x[i]
    y += b[0]

    y = -y
    y = math.exp(y) + 1
    y = 1 / y

    return y

# 用多个分类器进行预测
def many_clf_predict(clf_list ,data):

    label_list = []

    clf_num = len(clf_list)

    for i in range(clf_num):
        label = clf_list[i].predict(data)[0]
        label_list.append(label)

    num_of_label1 = np.sum(np.array(label_list) == 1.0)
    num_of_label0 = np.sum(np.array(label_list) == 0.0)
    # print('0 = ',num_of_label0 ,'1 = ',num_of_label1 ,label_list)

    if num_of_label1 >=1:
        return 1.0

    if num_of_label1 >= num_of_label0 :
        return 1.0
    else:
        return 0.0

def test_accuracy(clf_list, trainDatas, trainLabels, day_len):
    analysis_name_dic = generate_analysis_name_dic()

    num_data = len(trainLabels)

    trainLabels_num_0 = np.sum(np.array(trainLabels) == 0)
    trainLabels_num_1 = np.sum(np.array(trainLabels) == 1)

    acc_count = 0
    acc_count_0 = 0
    acc_count_1 = 0

    real0_predict0_list = []
    real0_predict1_list = []
    real1_predict0_list = []
    real1_predict1_list = []
    all_real1_predict0_list = []


    for i in range(num_data):

        data = [trainDatas[i][6:]]
        predict_label = many_clf_predict(clf_list , data )

        person_list = []

        if predict_label == trainLabels[i]:
            acc_count += 1

            if trainLabels[i] == 0:
                acc_count_0 += 1

                person_list.append(trainLabels[i])
                person_list = person_list + trainDatas[i]
                real0_predict0_list.append(person_list)

            elif trainLabels[i] == 1:
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


#[{'termID': 261, 'term_num': 114, 'predict_day': 22 , 'camp_start_time': '2018-07-23 00:00:00', 'predict_data':[{'apply_Id':_ , 'term_num':_ ,}...]}, ,,]
def predict_leave(not_over_term_list):
    #predict0_list =[{'term_num':_ , 'name':_}, ,,]
    predict0_list =[]

    for term_num_dic in not_over_term_list:

        # print('预测',term_num_dic['term_num'],'期 =',len(term_num_dic['predict_data']),'人')


        day_len = term_num_dic['predict_day']
        #算法只能预测1-26天
        if day_len <=26 and day_len >=1:

            feature_map = []
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

            day = day_len
            file_path = '../data/train_data_with_lastLabel/%dday_data.csv'%day
            trainDatas, trainLabels = generate_data_and_label(file_path,day_len=day)
            total_train_Datas_List, total_train_Labels_List = generate_balance_data(trainDatas, trainLabels,day,num_of_label1_list=1000)

            clf_list = generateClf(total_train_Datas_List, total_train_Labels_List)

            #开始预测
            for person in term_num_dic['predict_data']:
                data = []
                for feature in feature_map:
                    data.append(person[feature])

                predict_label = many_clf_predict(clf_list , [data])

                # #全输出以查看
                # predict_label = 0

                if predict_label == 0:

                    predict_dic = {}
                    predict_dic['term'] = person['term_num']
                    predict_dic['name'] = person['name']
                    predict_dic['phone'] = person['phone']
                    predict_dic['camp_start_time'] = term_num_dic['camp_start_time']
                    predict_dic['day'] = term_num_dic['predict_day']
                    predict_dic['stay_day'] = term_num_dic['predict_day']


                    #把每个人的属性也输出出来
                    for feature in feature_map:
                        predict_dic[feature] = person[feature]

                    predict0_list.append(predict_dic)

    return predict0_list







if __name__ == '__main__':
    day_list  = [i for i in range(1,27)]
    for day in day_list:
        print('day = ',day)

        file_path = '../../../data/train_data_with_lastLabel/%dday_data.csv'%day
        trainDatas, trainLabels = generate_data_and_label(file_path,day_len=day)
        total_train_Datas_List, total_train_Labels_List = generate_balance_data(trainDatas, trainLabels,day,num_of_label1_list=1000)
        # total_train_Datas_List = [  [[129,11,22..],[... ]] , []*9]
        # total_train_Labels_List = [ [1,0,1...] ,[]*9

        clf_list = generateClf(total_train_Datas_List, total_train_Labels_List)

        test_accuracy(clf_list, trainDatas, trainLabels ,day_len= day)
        print("\n"*3)












