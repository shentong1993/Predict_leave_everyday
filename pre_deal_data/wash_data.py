#第二个运行 洗数据  , 生成  w.csv
import csv
import numpy as np

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

# 洗数据
def wash():
    #  data/weight_dataset
    data_list = processData('./data/weight_dataset/trainData.csv')


    speak_num_list = []
    not_zero = 0

    for person in data_list:
        num = 0
        for day in range(28):
            num += person['speak%d' % (day + 1)]

        speak_num_list.append(num)
        if num != 0:
            not_zero += 1

    # print('说话人 的百分比', not_zero / len(speak_num_list) * 100)

    weight_list = []
    weight1_list = []
    weight2_list = []
    weight3_list = []
    weight4_list = []

    delta_week1_list = []
    delta_week2_list = []
    delta_week3_list = []
    delta_week4_list = []

    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0

    id_list = []

    for person in data_list:
        weight_list.append(person['week0Weight'])
        weight1_list.append(person['week1Weight'])
        weight2_list.append(person['week2Weight'])
        weight3_list.append(person['week3Weight'])
        weight4_list.append(person['week4Weight'])

        if person['week1Weight'] != 0 and person['week0Weight'] != 0:
            delta1 = person['week0Weight'] - person['week1Weight']
            if delta1 > -10 and delta1 < 10:
                delta_week1_list.append(delta1)
            else:
                count1 += 1
                # print(person)
                data_list.remove(person)
                continue
        else:
            delta_week1_list.append(0)

        if person['week1Weight'] != 0 and person['week2Weight'] != 0:
            delta2 = person['week1Weight'] - person['week2Weight']

            if delta2 > -10 and delta2 < 10:
                delta_week2_list.append(delta2)
            else:
                count2 += 1
                data_list.remove(person)
                continue

        else:
            delta_week2_list.append(0)

        if person['week2Weight'] != 0 and person['week3Weight'] != 0:
            delta3 = person['week2Weight'] - person['week3Weight']

            if delta3 > -10 and delta3 < 10:
                delta_week3_list.append(delta3)
            else:
                count3 += 1
                data_list.remove(person)
                continue

        else:
            delta_week3_list.append(0)

        if person['week3Weight'] != 0 and person['week4Weight'] != 0:

            delta4 = person['week3Weight'] - person['week4Weight']
            if delta4 > -10 and delta4 < 10:
                delta_week4_list.append(delta4)
            else:
                count4 += 1
                data_list.remove(person)
                continue

        else:
            delta_week4_list.append(0)

    weight_array = np.array(weight_list)
    weight1_array = np.array(weight1_list)
    weight2_array = np.array(weight2_list)
    weight3_array = np.array(weight3_list)
    weight4_array = np.array(weight4_list)

    delta_week1_array = np.array(delta_week1_list)
    delta_week2_array = np.array(delta_week2_list)
    delta_week3_array = np.array(delta_week3_list)
    delta_week4_array = np.array(delta_week4_list)

    # print('week1 max = ', np.max(delta_week1_array), ' min = ', np.min(delta_week1_array))
    # print('week2 max = ', np.max(delta_week2_array), ' min = ', np.min(delta_week2_array))
    # print('week3 max = ', np.max(delta_week3_array), ' min = ', np.min(delta_week3_array))
    # print('week4 max = ', np.max(delta_week4_array), ' min = ', np.min(delta_week4_array))
    #
    # print(count1)
    # print(count2)
    # print(count3)
    # print(count4)
    #
    # print('len = ', len(data_list))
    # n, bins, patches = plt.hist(delta_week4_array, bins=30, facecolor='green', alpha=0.75)
    # n, bins, patches = plt.hist(weight1_array, bins=30, facecolor='b', alpha=0.75)

    # plt.show()

    with open("./data/weight_dataset/w.csv", "w+", encoding='utf8') as csvfile:
        writer = csv.writer(csvfile)
        # 先写入columns_name

        writer.writerow([
            'apply_Id',
            'age',
            'gender',
            'week0Height',
            'week0Weight',
            'week1Weight',
            'week2Weight',
            'week3Weight',
            'week4Weight',

            'check1',
            'check2',
            'check3',
            'check4',
            'check5',
            'check6',
            'check7',
            'check8',
            'check9',
            'check10',
            'check11',
            'check12',
            'check13',
            'check14',
            'check15',
            'check16',
            'check17',
            'check18',
            'check19',
            'check20',
            'check21',
            'check22',
            'check23',
            'check24',
            'check25',
            'check26',
            'check27',
            'check28',

            'breakfast1',
            'breakfast2',
            'breakfast3',
            'breakfast4',
            'breakfast5',
            'breakfast6',
            'breakfast7',
            'breakfast8',
            'breakfast9',
            'breakfast10',
            'breakfast11',
            'breakfast12',
            'breakfast13',
            'breakfast14',
            'breakfast15',
            'breakfast16',
            'breakfast17',
            'breakfast18',
            'breakfast19',
            'breakfast20',
            'breakfast21',
            'breakfast22',
            'breakfast23',
            'breakfast24',
            'breakfast25',
            'breakfast26',
            'breakfast27',
            'breakfast28',

            'lunch1',
            'lunch2',
            'lunch3',
            'lunch4',
            'lunch5',
            'lunch6',
            'lunch7',
            'lunch8',
            'lunch9',
            'lunch10',
            'lunch11',
            'lunch12',
            'lunch13',
            'lunch14',
            'lunch15',
            'lunch16',
            'lunch17',
            'lunch18',
            'lunch19',
            'lunch20',
            'lunch21',
            'lunch22',
            'lunch23',
            'lunch24',
            'lunch25',
            'lunch26',
            'lunch27',
            'lunch28',

            'dinner1',
            'dinner2',
            'dinner3',
            'dinner4',
            'dinner5',
            'dinner6',
            'dinner7',
            'dinner8',
            'dinner9',
            'dinner10',
            'dinner11',
            'dinner12',
            'dinner13',
            'dinner14',
            'dinner15',
            'dinner16',
            'dinner17',
            'dinner18',
            'dinner19',
            'dinner20',
            'dinner21',
            'dinner22',
            'dinner23',
            'dinner24',
            'dinner25',
            'dinner26',
            'dinner27',
            'dinner28',

            'trainning1',
            'trainning2',
            'trainning3',
            'trainning4',
            'trainning5',
            'trainning6',
            'trainning7',
            'trainning8',
            'trainning9',
            'trainning10',
            'trainning11',
            'trainning12',
            'trainning13',
            'trainning14',
            'trainning15',
            'trainning16',
            'trainning17',
            'trainning18',
            'trainning19',
            'trainning20',
            'trainning21',
            'trainning22',
            'trainning23',
            'trainning24',
            'trainning25',
            'trainning26',
            'trainning27',
            'trainning28',

            'speak1',
            'speak2',
            'speak3',
            'speak4',
            'speak5',
            'speak6',
            'speak7',
            'speak8',
            'speak9',
            'speak10',
            'speak11',
            'speak12',
            'speak13',
            'speak14',
            'speak15',
            'speak16',
            'speak17',
            'speak18',
            'speak19',
            'speak20',
            'speak21',
            'speak22',
            'speak23',
            'speak24',
            'speak25',
            'speak26',
            'speak27',
            'speak28',

            'greed1',
            'greed2',
            'greed3',
            'greed4',
            'greed5',
            'greed6',
            'greed7',
            'greed8',
            'greed9',
            'greed10',
            'greed11',
            'greed12',
            'greed13',
            'greed14',
            'greed15',
            'greed16',
            'greed17',
            'greed18',
            'greed19',
            'greed20',
            'greed21',
            'greed22',
            'greed23',
            'greed24',
            'greed25',
            'greed26',
            'greed27',
            'greed28',

            'pressure1',
            'pressure2',
            'pressure3',
            'pressure4',
            'pressure5',
            'pressure6',
            'pressure7',
            'pressure8',
            'pressure9',
            'pressure10',
            'pressure11',
            'pressure12',
            'pressure13',
            'pressure14',
            'pressure15',
            'pressure16',
            'pressure17',
            'pressure18',
            'pressure19',
            'pressure20',
            'pressure21',
            'pressure22',
            'pressure23',
            'pressure24',
            'pressure25',
            'pressure26',
            'pressure27',
            'pressure28',

            'menstrual1',
            'menstrual2',
            'menstrual3',
            'menstrual4',
            'menstrual5',
            'menstrual6',
            'menstrual7',
            'menstrual8',
            'menstrual9',
            'menstrual10',
            'menstrual11',
            'menstrual12',
            'menstrual13',
            'menstrual14',
            'menstrual15',
            'menstrual16',
            'menstrual17',
            'menstrual18',
            'menstrual19',
            'menstrual20',
            'menstrual21',
            'menstrual22',
            'menstrual23',
            'menstrual24',
            'menstrual25',
            'menstrual26',
            'menstrual27',
            'menstrual28'

        ])

        for i in data_list:
            writer.writerow([
                i['apply_Id'],
                i['age'],
                i['gender'],
                i['week0Height'],
                i['week0Weight'],
                i['week1Weight'],
                i['week2Weight'],
                i['week3Weight'],
                i['week4Weight'],

                i['check1'],
                i['check2'],
                i['check3'],
                i['check4'],
                i['check5'],
                i['check6'],
                i['check7'],
                i['check8'],
                i['check9'],
                i['check10'],
                i['check11'],
                i['check12'],
                i['check13'],
                i['check14'],
                i['check15'],
                i['check16'],
                i['check17'],
                i['check18'],
                i['check19'],
                i['check20'],
                i['check21'],
                i['check22'],
                i['check23'],
                i['check24'],
                i['check25'],
                i['check26'],
                i['check27'],
                i['check28'],

                i['breakfast1'],
                i['breakfast2'],
                i['breakfast3'],
                i['breakfast4'],
                i['breakfast5'],
                i['breakfast6'],
                i['breakfast7'],
                i['breakfast8'],
                i['breakfast9'],
                i['breakfast10'],
                i['breakfast11'],
                i['breakfast12'],
                i['breakfast13'],
                i['breakfast14'],
                i['breakfast15'],
                i['breakfast16'],
                i['breakfast17'],
                i['breakfast18'],
                i['breakfast19'],
                i['breakfast20'],
                i['breakfast21'],
                i['breakfast22'],
                i['breakfast23'],
                i['breakfast24'],
                i['breakfast25'],
                i['breakfast26'],
                i['breakfast27'],
                i['breakfast28'],

                i['lunch1'],
                i['lunch2'],
                i['lunch3'],
                i['lunch4'],
                i['lunch5'],
                i['lunch6'],
                i['lunch7'],
                i['lunch8'],
                i['lunch9'],
                i['lunch10'],
                i['lunch11'],
                i['lunch12'],
                i['lunch13'],
                i['lunch14'],
                i['lunch15'],
                i['lunch16'],
                i['lunch17'],
                i['lunch18'],
                i['lunch19'],
                i['lunch20'],
                i['lunch21'],
                i['lunch22'],
                i['lunch23'],
                i['lunch24'],
                i['lunch25'],
                i['lunch26'],
                i['lunch27'],
                i['lunch28'],

                i['dinner1'],
                i['dinner2'],
                i['dinner3'],
                i['dinner4'],
                i['dinner5'],
                i['dinner6'],
                i['dinner7'],
                i['dinner8'],
                i['dinner9'],
                i['dinner10'],
                i['dinner11'],
                i['dinner12'],
                i['dinner13'],
                i['dinner14'],
                i['dinner15'],
                i['dinner16'],
                i['dinner17'],
                i['dinner18'],
                i['dinner19'],
                i['dinner20'],
                i['dinner21'],
                i['dinner22'],
                i['dinner23'],
                i['dinner24'],
                i['dinner25'],
                i['dinner26'],
                i['dinner27'],
                i['dinner28'],

                i['trainning1'],
                i['trainning2'],
                i['trainning3'],
                i['trainning4'],
                i['trainning5'],
                i['trainning6'],
                i['trainning7'],
                i['trainning8'],
                i['trainning9'],
                i['trainning10'],
                i['trainning11'],
                i['trainning12'],
                i['trainning13'],
                i['trainning14'],
                i['trainning15'],
                i['trainning16'],
                i['trainning17'],
                i['trainning18'],
                i['trainning19'],
                i['trainning20'],
                i['trainning21'],
                i['trainning22'],
                i['trainning23'],
                i['trainning24'],
                i['trainning25'],
                i['trainning26'],
                i['trainning27'],
                i['trainning28'],

                i['speak1'],
                i['speak2'],
                i['speak3'],
                i['speak4'],
                i['speak5'],
                i['speak6'],
                i['speak7'],
                i['speak8'],
                i['speak9'],
                i['speak10'],
                i['speak11'],
                i['speak12'],
                i['speak13'],
                i['speak14'],
                i['speak15'],
                i['speak16'],
                i['speak17'],
                i['speak18'],
                i['speak19'],
                i['speak20'],
                i['speak21'],
                i['speak22'],
                i['speak23'],
                i['speak24'],
                i['speak25'],
                i['speak26'],
                i['speak27'],
                i['speak28'],
                i['greed1'],
                i['greed2'],
                i['greed3'],
                i['greed4'],
                i['greed5'],
                i['greed6'],
                i['greed7'],
                i['greed8'],
                i['greed9'],
                i['greed10'],
                i['greed11'],
                i['greed12'],
                i['greed13'],
                i['greed14'],
                i['greed15'],
                i['greed16'],
                i['greed17'],
                i['greed18'],
                i['greed19'],
                i['greed20'],
                i['greed21'],
                i['greed22'],
                i['greed23'],
                i['greed24'],
                i['greed25'],
                i['greed26'],
                i['greed27'],
                i['greed28'],

                i['pressure1'],
                i['pressure2'],
                i['pressure3'],
                i['pressure4'],
                i['pressure5'],
                i['pressure6'],
                i['pressure7'],
                i['pressure8'],
                i['pressure9'],
                i['pressure10'],
                i['pressure11'],
                i['pressure12'],
                i['pressure13'],
                i['pressure14'],
                i['pressure15'],
                i['pressure16'],
                i['pressure17'],
                i['pressure18'],
                i['pressure19'],
                i['pressure20'],
                i['pressure21'],
                i['pressure22'],
                i['pressure23'],
                i['pressure24'],
                i['pressure25'],
                i['pressure26'],
                i['pressure27'],
                i['pressure28'],

                i['menstrual1'],
                i['menstrual2'],
                i['menstrual3'],
                i['menstrual4'],
                i['menstrual5'],
                i['menstrual6'],
                i['menstrual7'],
                i['menstrual8'],
                i['menstrual9'],
                i['menstrual10'],
                i['menstrual11'],
                i['menstrual12'],
                i['menstrual13'],
                i['menstrual14'],
                i['menstrual15'],
                i['menstrual16'],
                i['menstrual17'],
                i['menstrual18'],
                i['menstrual19'],
                i['menstrual20'],
                i['menstrual21'],
                i['menstrual22'],
                i['menstrual23'],
                i['menstrual24'],
                i['menstrual25'],
                i['menstrual26'],
                i['menstrual27'],
                i['menstrual28']
            ])

