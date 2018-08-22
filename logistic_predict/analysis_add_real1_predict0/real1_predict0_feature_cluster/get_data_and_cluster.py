import csv
import numpy as np
import os
from sklearn.cluster import  KMeans


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


def make_day_dict(data_list):

    #[[lastLabel1 , applyId ], ... ]
    lastLabel1_and_applyId_list = []
    for person in data_list:
        person_list = []
        person_list.append(person['lastLabel1'])
        person_list.append(person['apply_Id'])

        lastLabel1_and_applyId_list.append(person_list)

    #把所有人的 lastLabel1 做成一个set
    lastLabel1_list = []
    for person in lastLabel1_and_applyId_list:
        lastLabel1_list.append(person[0])

    lastLabel1_set = set(lastLabel1_list)

    lastLabel1_list = list(lastLabel1_set)

    set_len = len(lastLabel1_list)

    # {8:[applyId ,applyId...], 13:[...], 26:[...]} 字典装每天的applyId
    day_dic = {}
    for day in lastLabel1_list:
        day_dic[day] = []

    for person_list in lastLabel1_and_applyId_list:
        day_dic[person_list[0]].append(person_list[1])

    return day_dic, lastLabel1_list



def change_applyId_to_feature(day_dic, lastLabel1_list, time):
    #/Users/shen/PycharmProjects/Predict_leave/data/add_lastLabel1.csv
    file_path = '../../../data/add_lastLabel1.csv'
    data_list = processData(file_path)

    # day_dic = {8:[applyId ,applyId...], 13:[...], 26:[...]} 字典装每天的applyId
    # day_dic_feature_list = {8:[[----],[-----]], 13:[],26:[]}
    day_dic_feature_list = {}
    for day in lastLabel1_list:
        day_dic_feature_list[day] = []



    for day in lastLabel1_list:

        day = int(day)

        feature_map = ['lastLabel1', 'apply_Id', 'age', 'gender', 'week0Weight', 'week0Height']
        for time in range(1, time + 1):
            feature_map.append('day%dWeight' % time)
            feature_map.append('breakfast%d' % time)
            feature_map.append('lunch%d' % time)
            feature_map.append('dinner%d' % time)
            feature_map.append('trainning%d' % time)
            feature_map.append('speak%d' % time)
            feature_map.append('greed%d' % time)
            feature_map.append('pressure%d' % time)
            feature_map.append('menstrual%d' % time)


        for apply_Id in day_dic[day]:
            person_feature = []
            for person in data_list:
                if person['apply_Id'] == apply_Id:
                    for feature in feature_map:
                        person_feature.append(person[feature])
                    break
            day_dic_feature_list[day].append(person_feature)

    # print(day_dic_feature_list)

    return day_dic_feature_list


def cluster(day_dic_feature_list, day_len):
    # day_dic_feature_list = {8:[[----],[-----]], 13:[],26:[]}
    for day, feature_list in day_dic_feature_list.items():
        day = int(day)
        feature_map = ['lastLabel1', 'apply_Id', 'age', 'gender', 'week0Weight', 'week0Height']
        for time in range(1, day_len + 1):
            feature_map.append('day%dWeight' % time)
            feature_map.append('breakfast%d' % time)
            feature_map.append('lunch%d' % time)
            feature_map.append('dinner%d' % time)
            feature_map.append('trainning%d' % time)
            feature_map.append('speak%d' % time)
            feature_map.append('greed%d' % time)
            feature_map.append('pressure%d' % time)
            feature_map.append('menstrual%d' % time)

        feature_map_samll = [ 'lastLabel1', 'apply_Id', 'age', 'gender', 'week0Weight', 'week0Height']
        for time in range(1, day_len + 1):
            feature_map_samll.append('breakfast%d' % time)
            feature_map_samll.append('lunch%d' % time)
            feature_map_samll.append('dinner%d' % time)
            feature_map_samll.append('trainning%d' % time)

        trainDatas_small = []
        for person in feature_list:
            data = []
            data.extend(person[0:6])
            step =7
            for i in range(day_len):
                data.extend(person[ step : step+4 ])
                step += 9

            trainDatas_small.append(data)

        trainDatas_cut = [person[6:] for person in trainDatas_small]

        X_person_array = np.array(trainDatas_cut)



        # Compute Affinity Propagation
        # af = AffinityPropagation().fit(X_person_array)
        #
        # cluster_centers_indices = af.cluster_centers_indices_
        # y_pred = af.labels_
        # clusters_num = len(cluster_centers_indices)
        y_pred = KMeans(n_clusters=10, random_state=10).fit_predict(X_person_array)
        clusters_num = 10



        # {0:[[data...], ...]] ,1:[], ..}
        cluster_dic = {}
        for c in range(clusters_num):
            cluster_dic[c] = []

        for i, c in enumerate(y_pred):
            cluster_dic[c].append(feature_list[i])


        print()
        for c in range(clusters_num):
            #计算每个聚类的均值

            # 计算每一个分类的均值 体重是无意义的统计
            temp_list = cluster_dic[c]
            temp_cut_list = [p[6:] for p in temp_list]

            temp_cut_list_array = np.array(temp_cut_list)
            mean = np.mean(temp_cut_list_array, axis=0)
            mean_list = mean.tolist()
            mean_list = [round(number, 2) for number in mean_list]

            # # 1.我们把均值列表 转化成 每天字典的形式 ，以方便观察
            # mean_dic = {}
            # step = 1
            # for time in range(day+1):
            #     mean_dic['%d' % (time + 1)] = mean_list[step:step + 4]
            #     step += 9
            # print('待的天数 =',day+1 ,'  第',c + 1,'类 ', len(cluster_dic[c]),'人', mean_dic)

            #2. 四舍五入用
            mean_dic = {}
            step = 1
            for time in range(day_len):
                temp_list =  mean_list[ step:step +4 ]
                temp_list = [1 if number>=0.5 else 0 for number in temp_list]
                mean_dic['%d'%(time+1)] = temp_list
                step +=9
            print('待的天数 =',day+1 ,'  第',c + 1,'类  ', len(cluster_dic[c]),'人', mean_dic)


            #/Users/shen/PycharmProjects/Predict_leave/logistic_predict/analysis_add_real1_predict0/real1_predict0_feature_cluster/cluster_data
            dir_path = './cluster_data/{0}day/keep_{1}_day'.format(day_len, (day+1))
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            save_path = './cluster_data/{0}day/keep_{1}_day/{2}.csv'.format(day_len, (day+1) ,c)
            with open(save_path, "w+", encoding='utf8') as csvfile:
                writer = csv.writer(csvfile)

                writer.writerow(feature_map)

                for i in range(len(cluster_dic[c])):
                    writer.writerow(cluster_dic[c][i])


if __name__ == '__main__':
    # day_list = [day for day in range(1,27)]
    day_list = [21]
    for day in day_list:
        #/Users/shen/PycharmProjects/Predict_leave/logistic_predict/predict/balance_predict/data/day1/real1_predict0_list.csv
        data_list = processData('../../predict/balance_predict/data/day%d/real1_predict0_list.csv'%day)

        # {8:[applyId ,applyId...], 13:[...], 26:[...]} 字典装每天的applyId
        day_dic ,lastLabel1_list= make_day_dict(data_list)

        # day_dic_feature_list = {8:[[----],[-----]], 13:[],26:[]}
        day_dic_feature_list = change_applyId_to_feature(day_dic, lastLabel1_list ,time = day)

        cluster(day_dic_feature_list,day_len= day)





