# import numpy as np
# import matplotlib.pyplot as plt
# '''
#     day  负样本个数  正样本个数     负样本预测对的个数  负样本召回率  所有正样本验证错的个数  正样本召回率  正样本预测错的n-23天离开  正样本预测错的剩余人数
#     (413,120,124,123,129,74,237,143,147,147,162,176,96,368,195,237,243,264,245,150,1133,440,484,606,776,1089)
#
# '''
#
# real1 = (21894,21774,21650,21527,21398,21324,21087,20944,20797,20650,20488,20312,20216,19848,19653,19416,19173,18909,18664,18514,17381,16941,16457,15851,15075,13986)
#
# real1_predict0 =  (6809,2306,2134,1935,1616,1134,1444,1015,1073,775,851,613,214,1081,644,680,448,512,319,123,1215,475,588,630,672,726)
#
# N = len(real1_predict0)
# # print(len(real1_predict0), len(real1))
# real1_predict1 = tuple(real1[i]-real1_predict0[i] for i in range(26))
# # print(real1_predict1)
# real0 = (413,120,124,123,129,74,237,143,147,147,162,176,96,368,195,237,243,264,245,150,1133,440,484,606,776,1089)
#
#
# ind = np.arange(N)    # the x locations for the groups
# print(ind)
#
# width = 0.35       # the width of the bars: can also be len(x) sequence
#
# p1 = plt.bar(ind, real1_predict1,width)
# p2 = plt.bar(ind, real1_predict0, width,bottom=real1_predict1)
# p3 = plt.bar(ind, real0,width,bottom = real1)
#
# plt.ylabel('people number')
# plt.title('day and people ')
# x_day = (str(i) for i in range(1,27))
# plt.xticks(ind, x_day)
# plt.yticks(np.arange(0, 24000, 1000))
# plt.legend((p1[0], p2[0],p3[0]), ('real1_predict1','real1_predict0','real0'))
#
# plt.show()
