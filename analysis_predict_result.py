import xlrd
import os


def open_excel(file_name ):

    file_path = os.path.join('./result_data/',file_name )
    try:
        workbook = xlrd.open_workbook(file_path)
        return workbook
    except Exception as e:
        print(str(e))


def change_xls_to_term_dic(file):
    workbook = open_excel(file)
    booksheet = workbook.sheet_by_index(0)  # 用索引取第一个sheet
    nrows = booksheet.nrows  # 拿到总共行数

    data_list = []
    term_list = []

    # 第1行是每列名字， 装进list
    col_name_list = booksheet.row_values(0)

    # print(col_name_list)

    for row in range(1, nrows):

        col_len = len(booksheet.row_values(row))
        person_dic = {}
        for col in range(col_len):
            person_dic[col_name_list[col]] = booksheet.cell_value(row , col)
        data_list.append(person_dic)

        term_list.append(booksheet.cell_value(row, 0))

    term_list = list(set(term_list))

    # 制作每学期预测要跑的字典 predict_dic = {115:[{}...]...}
    predict_dic = {}
    for term in term_list:
        predict_dic[term] = []


    for person in data_list:
        person_dic = {}
        person_dic['name'] = person['姓名']
        person_dic['use_n_day_predict'] = person['用1-n天数据预测']

        # 将每个学员插入 predict_dic 中对应的学期
        predict_dic[person['学期']].append(person_dic)


    return predict_dic ,term_list


def verify_if_predict_right_in_tommorrow(predic_file , real_file):
    predict_dic ,term_list = change_xls_to_term_dic(predic_file)

    real_dic , _ = change_xls_to_term_dic(real_file)

    print(predict_dic)
    print(real_dic)

    # acc_dic 是验证算法准确率的字典
    acc_dic = {}
    for term in term_list:
        acc_dic[term] = {'预测的天数':0,'总预测':0 , '预测对':0}
        acc_dic[term]['预测的天数'] = predict_dic[term][0]['use_n_day_predict']



    # 开始统计算法预测对了多少人
    for term , person_list in predict_dic.items():
        acc_dic[term]['总预测'] = len(person_list)

        for person in person_list:
            name = person['name']

            for find_person in real_dic[term]:
                if name == find_person['name']:
                    acc_dic[term]['预测对'] += 1
                    break

    print(acc_dic)

    return





if __name__ == '__main__':

    #/Users/shen/PycharmProjects/analysis_predict_leave_result/result_data/
    predic_file = '8月28日 today_run.xls'
    real_file = '8月29日 already_run.xls'

    verify_if_predict_right_in_tommorrow(predic_file , real_file)

