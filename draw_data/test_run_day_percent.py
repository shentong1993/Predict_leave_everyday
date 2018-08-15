import csv
import numpy as np
import matplotlib.pyplot as plt
import math



def processData(filePath):
    dataList = []

    with open(filePath, 'r') as f:
        records = f.readlines()

        # 读第一行获取每一列的列名
        # strip() 去掉行尾的换行符

        print(records[0].strip().split(','))
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




def getLabel():

    data_list = processData('../data/add_lastLabel1.csv')

    run_day_list = []
    for person in data_list:

        person_label_list = []
        last_day_leave = 0

        for day in range(1, 28):
            person_label_list.append( person['label%d'%day])

        for last in range(26, -1 , -1 ):
            if person_label_list[last] == 0:
                last_day_leave += 1
            else:
                break
        # if (27 - last_day_leave) != 27 and (27 - last_day_leave) != 26:
        #     run_day_list.append(27 - last_day_leave)

        # 27-last_day_leave 代表最后一个label（1） 所在的位置
        run_day_list.append(27 - last_day_leave)


    return run_day_list



def draw(run_day_list):
    # n, bins, patches = plt.hist(run_day_list, bins=26,  facecolor='green',edgecolor='black')
    n, bins, patches = plt.hist(run_day_list,bins=28,facecolor='green',edgecolor='black' )

    plt.title('1-26 every day leave people')

    plt.show()


def count_list_num(run_day_list):

    c = 0
    for person in run_day_list:
        if person ==0:
            c+=1
    print(c)

    total_person = len(run_day_list)
    run_day_array = np.array(run_day_list)

    print(np.max(run_day_array), np.min(run_day_array))
    count_list = {}
    percent_list = {}

    for day in range(0, 28):
        count_list['%d'%day] = np.sum(run_day_array == day )
        percent_list['%d'%day] = \
            round((count_list['%d'%day] / total_person * 100), 2)

    print(count_list)
    print(percent_list)






if __name__ == '__main__':
    run_day_list = getLabel()

    count_list_num(run_day_list)

    draw(run_day_list)
    print(len(run_day_list))
