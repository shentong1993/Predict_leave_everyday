# --------------------------------------------------------
# 每月1日 00:01 制作数据集
# Copyright (c) Fittime 2018
# Written by Shentong
# --------------------------------------------------------
from database.TrainDataModel import sql_get_data
from pre_deal_data.wash_data import wash
from pre_deal_data.make_one_label_csv import getLabel , no_weight_getLabel
from pre_deal_data.add_null_weight import add_weight
from pre_deal_data.add_lastLabel1_csv import add_lastlasbel1,no_weight_add_lastlasbel1
from pre_deal_data.make_train_data_with_lastLabel1 import make_every_day_train_data, no_weight_make_every_day_train_data


def start():

    print('开始制作数据集')
    sql_get_data()
    print('make trainData.csv over')

    wash()
    print('洗数据 完毕')

    getLabel()
    print('label1-27 的1-0标签生成 完毕')

    add_weight()
    print('添加每日空缺体重 完毕')

    add_lastlasbel1()
    print('生成最后一个标签是1的位置 完毕')

    make_every_day_train_data()
    print('生成从1-26天的时间段的训练数据 完毕')






    no_weight_getLabel()
    print('无体重 label1-27 的1-0标签生成 完毕')

    no_weight_add_lastlasbel1()
    print('无体重 生成最后一个标签是1的位置 完毕')

    no_weight_make_every_day_train_data()
    print('无体重 生成从1-26天的时间段的训练数据 完毕')

    print('数据集制作 完毕')


if __name__ == '__main__':
    start()
