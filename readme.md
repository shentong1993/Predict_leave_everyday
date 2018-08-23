1. 上线首先运行 pull.py, 这个文件必须先运行 ，生成的是数据集
  
  之后 , 每月1号00:01运行一次

# /Users/shen/PycharmProjects/Predict_leave/every_day_run/get_data_and_predict.py
2. 每天00:01点 ，运行 /every_day_run/get_data_and_predict.py 
  这个python 从当前减脂营在营的拉数据，预测跑不跑

3. 代码环境
# env: python3.7.0
csv
peewee
database
xlwt
numpy
sklearn


4. 各个目录内代码功能
  ./data/ 中装的是有体重从提取到生成数据集的数据
  
  ./data/train_data_with_lastLabel/ 
    中存的是有体重的最终数据集
    
  ./no_weight_data 中装的是无体重从提取到生成数据集的数据
  
  ./database/TrainDataModel.py 
    是从数据库抽取数据的第1步
  
  ./draw_data/ 中 draw1, draw2 ,draw3 
    是画柱状图分析算法效果
  
  ./pull.py
    每月00:01 运行这个制作数据集
  
  ./get_data_and_predict.py 
    每日00:01运行这个，从数据库拉取减脂营在营的学员，对昨天有动作的预测，其余统计
    
  ./every_day_result/ 
    存放的是get_data_and_predict 生成的预测和统计结果
  
  ./logistic_predict/analysis_add_real1_predict0/ 
    是对负样本预测对的 和 正样本预测错的进行聚类，以提升算法效果
  
  ./logistic_predict/predict/many_label1_predict/make_many_label1_analysis.py 
    是对有体重的人用1000个逻辑回归去预测
    
  ./logistic_predict/predict/no_weight_many_label1_predict/no_weight_make_many_label1_analysis.py
     是对无体重的人用1000个逻辑回归去预测
     
  ./logistic_predict/predict/balance_predict/make_real_predict_analysis.py
     是对有体重的人用1个逻辑回归去预测
  
  ./logistic_predict/predict/last_n_day_predict/last_day_predict.py
     用规则：后n天不打卡判断为离开，作为分类器
    
     
     
  ./pre_deal_data/wash_data.py  洗数据
  
  ./pre_deal_data/make_one_label_csv.py  对每个人做标签 ,label1-27, 代表从第1-27天消失
  
  ./pre_deal_data/add_null_weight.py 对数据集从前向后补体重
  
  ./pre_deal_data/add_lastLabel1_csv.py 生成最后一个标签(label)是1的位置
  
  ./pre_deal_data/make_train_data_with_lastLabel1.py  按天数生成对应的数据集
  
  
    

   
  


