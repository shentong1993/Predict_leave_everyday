from database.TrainDataModel import sql_get_data
from pre_deal_data.wash_data import wash
from pre_deal_data.make_one_label_csv import getLabel
from pre_deal_data.add_null_weight import add_weight
from pre_deal_data.add_lastLabel1_csv import add_lastlasbel1
from pre_deal_data.make_train_data_with_lastLabel1 import make_every_day_train_data


def start():
    sql_get_data()
    print('make trainData.csv over')

    wash()
    print('洗数据 完毕')

    getLabel()
    print('label1-27 的1-0标签生成完毕')

    add_weight()
    print('添加每日空缺体重 完毕')

    add_lastlasbel1()
    print('生成最后一个标签是1的位置 完毕')

    make_every_day_train_data()
    print('生成从1-26天的时间 段 的训练数据 完毕')


if __name__ == '__main__':

    start()