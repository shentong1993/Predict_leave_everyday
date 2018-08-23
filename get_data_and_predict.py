# --------------------------------------------------------
# 每天 00:01 拉数据预测用户今天是否离开
# Copyright (c) Fittime 2018
# Written by Shentong
# --------------------------------------------------------
import operator
import time
from xlwt import *
from peewee import *
from database.baseModel import EshopBaseModel, camp_db
from logistic_predict.predict.many_label1_predict.make_many_label1_analysis import  predict_leave
from logistic_predict.predict.no_weight_many_label1_predict.no_weight_make_many_label1_analysis import no_weight_predict_leave


class RawModel(EshopBaseModel):
    rawID = IntegerField()



# 提取减脂营没有结营的所有营
def get_not_over_TermID():
    #[{'termID': 261, 'term_num': 114,'camp_start_time':___ , 'predict_day': 22 }, ,,]
    #predict_day 就是需要预测的天数
    not_over_term_list = []

    if camp_db.is_closed():
        camp_db.connect()

    #选取所有目前 在营的减脂营的 term_id
    record = RawModel.raw('''
        SELECT
          term.TERM_ID as termID,
          term.TERM_NUM term_num,
          term.CAMP_START_TIME  start_time,
          now()    now,
          datediff(now(),term.CAMP_START_TIME )      predict_day
        FROM eshop.TB_TERM term
        WHERE date_add(term.CAMP_START_TIME, INTERVAL term.DAYS DAY) > now()
              and term.CAMP_START_TIME < now()
              and datediff(now(),term.CAMP_START_TIME ) > 0
              AND term.TYPE = 1
''')

    for r in record:
        r_dic ={}
        r_dic['termID'] = r.termID
        r_dic['term_num'] = r.term_num
        r_dic['camp_start_time'] = str(r.start_time)
        r_dic['leave_time'] = str(r.now)
        r_dic['predict_day'] = r.predict_day

        not_over_term_list.append(r_dic)

    if not camp_db.is_closed():
        camp_db.close()

    return not_over_term_list



# 根据没结营的减脂营 ，提取每个营开营前记录体重的学员
# not_over_term_list = [{'termID': 261, 'term_num': 114, 'predict_day': 22}, {'termID': 265, 'term_num': 115, 'predict_day': 15}, {'termID': 268, 'term_num': 116, 'predict_day': 8}, {'termID': 274, 'term_num': 117, 'predict_day': 1}]
def get_day_weight(not_over_term_list):
    if camp_db.is_closed():
        camp_db.connect()

    for term_num_dic in not_over_term_list:
        term_num_dic['predict_data'] = []

        record = RawModel.raw('''        
select
  sub2.ai id,
  sub2.tn xueQi,
  sub2.n  mingZi,
  sub2.mo shouji,
  sub2.ag nianLing,
  sub2.gd xingBie,
  sub2.w0h shenGao,
  sub2.w0w tiZhong,
  max(case sub2.dy
        when 1
          then sub2.d
        else 0
        end)  d1,
  max(case sub2.dy
        when 2
          then sub2.d
        else 0
        end)  d2,

  max(case sub2.dy
        when 3
          then sub2.d
        else 0
        end)  d3,
  max(case sub2.dy
        when 4
          then sub2.d
        else 0
        end)  d4,


    max(case sub2.dy
        when 5
          then sub2.d
        else 0
        end)  d5,
  max(case sub2.dy
        when 6
          then sub2.d
        else 0
        end)  d6,

  max(case sub2.dy
        when 7
          then sub2.d
        else 0
        end)  d7,
  max(case sub2.dy
        when 8
          then sub2.d
        else 0
        end)  d8,

  max(case sub2.dy
        when 9
          then sub2.d
        else 0
        end)  d9,
  max(case sub2.dy
        when 10
          then sub2.d
        else 0
        end)  d10,

  max(case sub2.dy
        when 11
          then sub2.d
        else 0
        end)  d11,
  max(case sub2.dy
        when 12
          then sub2.d
        else 0
        end)  d12,


    max(case sub2.dy
        when 13
          then sub2.d
        else 0
        end)  d13,
  max(case sub2.dy
        when 14
          then sub2.d
        else 0
        end)  d14,

  max(case sub2.dy
        when 15
          then sub2.d
        else 0
        end)  d15,
  max(case sub2.dy
        when 16
          then sub2.d
        else 0
        end)  d16,




   max(case sub2.dy
        when 17
          then sub2.d
        else 0
        end)  d17,
  max(case sub2.dy
        when 18
          then sub2.d
        else 0
        end)  d18,

  max(case sub2.dy
        when 19
          then sub2.d
        else 0
        end)  d19,
  max(case sub2.dy
        when 20
          then sub2.d
        else 0
        end)  d20,


    max(case sub2.dy
        when 21
          then sub2.d
        else 0
        end)  d21,
  max(case sub2.dy
        when 22
          then sub2.d
        else 0
        end)  d22,

  max(case sub2.dy
        when 23
          then sub2.d
        else 0
        end)  d23,
  max(case sub2.dy
        when 24
          then sub2.d
        else 0
        end)  d24,

  max(case sub2.dy
        when 25
          then sub2.d
        else 0
        end)  d25,
  max(case sub2.dy
        when 26
          then sub2.d
        else 0
        end)  d26,

  max(case sub2.dy
        when 27
          then sub2.d
        else 0
        end)  d27,
  max(case sub2.dy
        when 28
          then sub2.d
        else 0
        end)  d28

from(
    select
    sub.term_num tn,
    sub.name   n,
    sub.apply_id ai,
    sub.mobile   mo,
    sub.age      ag,
    sub.gender   gd,
    sub.week0Height w0h,
    sub.week0Weight w0w,
    sub.datas d,
    sub.create_time ct,
    sub.day dy,
    count(*)    check_times_one_day


  from (
         select
           term.TERM_NUM                                  term_num,
           apply.NAME                                     name,
           wr.apply_id                                    apply_id,
           apply.MOBILE                                   mobile,
           apply.AGE age,
           case apply.GENDER
           when 'f'
             then 1
           ELSE 0 end   gender,
           sub_body.week0Weight                           week0Weight,
           sub_body.week0Height                           week0Height,
           wr.create_time                                 create_time,
           term.CAMP_START_TIME start_time,
           wr.datas                                       datas,
           DATEDIFF(wr.create_time, term.CAMP_START_TIME)+1  day


         from tb_weight_record wr
           left join TB_APPLY_RECORD apply on apply.APPLY_ID = wr.APPLY_ID
           LEFT JOIN TB_TERM term ON term.TERM_ID = apply.TERM_ID
           inner join (select
                        body.apply_id,
                        max(
                            case body.WEEK
                        when 0
                          then body.WEIGHT
                        else 0
                        end)    week0Weight,
                        max(
                        case body.WEEK
                        when 0
                          then body.HEIGHT
                        else 0
                        end
                        ) week0Height

                      from TB_BODY_DATA body
                      group by APPLY_ID
                      having week0Weight> 0 and week0Height > 0
                     ) sub_body on apply.APPLY_ID = sub_body.APPLY_ID
           LEFT JOIN TB_ORDER tborder ON apply.PACKAGE_ORDER_ID = tborder.ORDER_ID
           WHERE tborder.OUTER_ORIGIN != 'exchange_white_list_test'
               and  term.TERM_NUM = %s

         order by wr.apply_id, wr.create_time desc
       ) sub
  group by sub.apply_id, sub.day
    )sub2
group by sub2.ai
order by sub2.tn
        ''', term_num_dic['term_num'])

        for r in record:
            r_dic ={}
            r_dic['apply_Id'] = r.id
            r_dic['term_num'] = r.xueQi
            r_dic['name'] = r.mingZi
            r_dic['phone'] = str(r.shouji)
            r_dic['age'] = r.nianLing
            r_dic['gender'] = r.xingBie
            r_dic['week0Height']= r.shenGao
            r_dic['week0Weight']= r.tiZhong
            r_dic['day1Weight']= r.d1
            r_dic['day2Weight']= r.d2
            r_dic['day3Weight'] = r.d3
            r_dic['day4Weight'] = r.d4
            r_dic['day5Weight'] = r.d5
            r_dic['day6Weight'] = r.d6
            r_dic['day7Weight'] = r.d7
            r_dic['day8Weight'] = r.d8
            r_dic['day9Weight']= r.d9
            r_dic['day10Weight']= r.d10
            r_dic['day11Weight'] = r.d11
            r_dic['day12Weight'] = r.d12
            r_dic['day13Weight'] = r.d13
            r_dic['day14Weight'] = r.d14
            r_dic['day15Weight'] = r.d15
            r_dic['day16Weight'] = r.d16
            r_dic['day17Weight'] = r.d17
            r_dic['day18Weight'] = r.d18
            r_dic['day19Weight'] = r.d19
            r_dic['day20Weight'] = r.d20
            r_dic['day21Weight'] = r.d21
            r_dic['day22Weight'] = r.d22
            r_dic['day23Weight'] = r.d23
            r_dic['day24Weight'] = r.d24
            r_dic['day25Weight'] = r.d25
            r_dic['day26Weight'] = r.d26
            r_dic['day27Weight'] = r.d27
            r_dic['day28Weight'] = r.d28

            term_num_dic['predict_data'].append(r_dic)

    if not camp_db.is_closed():
        camp_db.close()

    return not_over_term_list



# 根据没结营的减脂营 ，提取每个营对应applyID
def get_day_all_applyID(not_over_term_list):
    if camp_db.is_closed():
        camp_db.connect()

    for term_num_dic in not_over_term_list:
        term_num_dic['predict_data'] = []

        record = RawModel.raw('''
        select
  apply.APPLY_ID apply_Id,
  term.TERM_NUM term_num,
  apply.NAME name,
  apply.MOBILE                                   mobile,
  apply.AGE age,
  apply.GENDER gender

from TB_APPLY_RECORD apply
  LEFT JOIN TB_TERM term ON term.TERM_ID = apply.TERM_ID
  LEFT JOIN TB_ORDER tborder ON apply.PACKAGE_ORDER_ID = tborder.ORDER_ID
WHERE tborder.OUTER_ORIGIN != 'exchange_white_list_test'
      and term.TERM_NUM = %s
        ''', term_num_dic['term_num'])

        for r in record:
            r_dic = {}
            r_dic['apply_Id'] = r.apply_Id
            r_dic['term_num'] = r.term_num
            r_dic['name'] = r.name
            r_dic['phone'] = str(r.mobile)
            r_dic['age'] = r.age
            r_dic['gender'] = r.gender

            term_num_dic['predict_data'].append(r_dic)

    if not camp_db.is_closed():
        camp_db.close()

    return not_over_term_list



# 提取所有未结营的打卡信息
def get_day_check():
    trainDatas = []

    if camp_db.is_closed():
        camp_db.connect()

    record = RawModel.raw('''
    select
    sub.APPLY_ID apply_Id,
    max(case sub.day
      when 1
        then sub.checkinTimes
      else 0
      end)  check1,

    max(case sub.day
        when 2
          then sub.checkinTimes
        else 0
        end)  check2,

    max(case sub.day
          when 3
            then sub.checkinTimes
          else 0
          end)  check3,

    max(case sub.day
        when 4
          then sub.checkinTimes
        else 0
        end)  check4,

    max(case sub.day
        when 5
          then sub.checkinTimes
        else 0
        end)  check5,

    max(case sub.day
        when 6
          then sub.checkinTimes
        else 0
        end)  check6,

    max(case sub.day
        when 7
          then sub.checkinTimes
        else 0
        end)  check7,

    max(case sub.day
        when 8
          then sub.checkinTimes
        else 0
        end)  check8,

    max(case sub.day
      when 9
        then sub.checkinTimes
      else 0
      end)  check9,

    max(case sub.day
        when 10
          then sub.checkinTimes
        else 0
        end)  check10,

    max(case sub.day
        when 11
          then sub.checkinTimes
        else 0
        end)  check11,

    max(case sub.day
        when 12
          then sub.checkinTimes
        else 0
        end)  check12,

    max(case sub.day
      when 13
        then sub.checkinTimes
      else 0
      end)  check13,

    max(case sub.day
        when 14
          then sub.checkinTimes
        else 0
        end)  check14,

    max(case sub.day
      when 15
        then sub.checkinTimes
      else 0
      end)  check15,

    max(case sub.day
        when 16
          then sub.checkinTimes
        else 0
        end)  check16,

    max(case sub.day
      when 17
        then sub.checkinTimes
      else 0
      end)  check17,

    max(case sub.day
        when 18
          then sub.checkinTimes
        else 0
        end)  check18,

    max(case sub.day
      when 19
        then sub.checkinTimes
      else 0
      end)  check19,

    max(case sub.day
        when 20
          then sub.checkinTimes
        else 0
        end)  check20,

    max(case sub.day
      when 21
        then sub.checkinTimes
      else 0
      end)  check21,

    max(case sub.day
        when 22
          then sub.checkinTimes
        else 0
        end)  check22,

    max(case sub.day
      when 23
        then sub.checkinTimes
      else 0
      end)  check23,

    max(case sub.day
        when 24
          then sub.checkinTimes
        else 0
        end)  check24,

    max(case sub.day
      when 25
        then sub.checkinTimes
      else 0
      end)  check25,

    max(case sub.day
        when 26
          then sub.checkinTimes
        else 0
        end)  check26,

    max(case sub.day
      when 27
        then sub.checkinTimes
      else 0
      end)  check27,

    max(case sub.day
        when 28
          then sub.checkinTimes
        else 0
        end)  check28,




    max(case sub.day
      when 1
        then sub.breakfast
      else 0
      end)  breakfast1,

    max(case sub.day
        when 2
          then sub.breakfast
        else 0
        end)  breakfast2,

      max(case sub.day
          when 3
            then sub.breakfast
          else 0
          end)  breakfast3,

    max(case sub.day
        when 4
          then sub.breakfast
        else 0
        end)  breakfast4,

    max(case sub.day
        when 5
          then sub.breakfast
        else 0
        end)  breakfast5,

    max(case sub.day
        when 6
          then sub.breakfast
        else 0
        end)  breakfast6,

    max(case sub.day
        when 7
          then sub.breakfast
        else 0
        end)  breakfast7,

    max(case sub.day
        when 8
          then sub.breakfast
        else 0
        end)  breakfast8,

    max(case sub.day
      when 9
        then sub.breakfast
      else 0
      end)  breakfast9,

    max(case sub.day
        when 10
          then sub.breakfast
        else 0
        end)  breakfast10,

    max(case sub.day
        when 11
          then sub.breakfast
        else 0
        end)  breakfast11,

    max(case sub.day
        when 12
          then sub.breakfast
        else 0
        end)  breakfast12,

    max(case sub.day
      when 13
        then sub.breakfast
      else 0
      end)  breakfast13,

    max(case sub.day
        when 14
          then sub.breakfast
        else 0
        end)  breakfast14,

    max(case sub.day
      when 15
        then sub.breakfast
      else 0
      end)  breakfast15,

    max(case sub.day
        when 16
          then sub.breakfast
        else 0
        end)  breakfast16,

    max(case sub.day
      when 17
        then sub.breakfast
      else 0
      end)  breakfast17,

    max(case sub.day
        when 18
          then sub.breakfast
        else 0
        end)  breakfast18,

    max(case sub.day
      when 19
        then sub.breakfast
      else 0
      end)  breakfast19,

    max(case sub.day
        when 20
          then sub.breakfast
        else 0
        end)  breakfast20,

    max(case sub.day
      when 21
        then sub.breakfast
      else 0
      end)  breakfast21,

    max(case sub.day
        when 22
          then sub.breakfast
        else 0
        end)  breakfast22,

    max(case sub.day
      when 23
        then sub.breakfast
      else 0
      end)  breakfast23,

    max(case sub.day
        when 24
          then sub.breakfast
        else 0
        end)  breakfast24,

    max(case sub.day
      when 25
        then sub.breakfast
      else 0
      end)  breakfast25,

    max(case sub.day
        when 26
          then sub.breakfast
        else 0
        end)  breakfast26,

    max(case sub.day
      when 27
        then sub.breakfast
      else 0
      end)  breakfast27,

    max(case sub.day
        when 28
          then sub.breakfast
        else 0
        end)  breakfast28,



    max(case sub.day
      when 1
        then sub.lunch
      else 0
      end)  lunch1,

    max(case sub.day
        when 2
          then sub.lunch
        else 0
        end)  lunch2,

      max(case sub.day
          when 3
            then sub.lunch
          else 0
          end)  lunch3,

    max(case sub.day
        when 4
          then sub.lunch
        else 0
        end)  lunch4,

    max(case sub.day
        when 5
          then sub.lunch
        else 0
        end)  lunch5,

    max(case sub.day
        when 6
          then sub.lunch
        else 0
        end)  lunch6,

    max(case sub.day
        when 7
          then sub.lunch
        else 0
        end)  lunch7,

    max(case sub.day
        when 8
          then sub.lunch
        else 0
        end)  lunch8,

    max(case sub.day
      when 9
        then sub.lunch
      else 0
      end)  lunch9,

    max(case sub.day
        when 10
          then sub.lunch
        else 0
        end)  lunch10,

    max(case sub.day
        when 11
          then sub.lunch
        else 0
        end)  lunch11,

    max(case sub.day
        when 12
          then sub.lunch
        else 0
        end)  lunch12,

    max(case sub.day
      when 13
        then sub.lunch
      else 0
      end)  lunch13,

    max(case sub.day
        when 14
          then sub.lunch
        else 0
        end)  lunch14,

    max(case sub.day
      when 15
        then sub.lunch
      else 0
      end)  lunch15,

    max(case sub.day
        when 16
          then sub.lunch
        else 0
        end)  lunch16,

    max(case sub.day
      when 17
        then sub.lunch
      else 0
      end)  lunch17,

    max(case sub.day
        when 18
          then sub.lunch
        else 0
        end)  lunch18,

    max(case sub.day
      when 19
        then sub.lunch
      else 0
      end)  lunch19,

    max(case sub.day
        when 20
          then sub.lunch
        else 0
        end)  lunch20,

    max(case sub.day
      when 21
        then sub.lunch
      else 0
      end)  lunch21,

    max(case sub.day
        when 22
          then sub.lunch
        else 0
        end)  lunch22,

    max(case sub.day
      when 23
        then sub.lunch
      else 0
      end)  lunch23,

    max(case sub.day
        when 24
          then sub.lunch
        else 0
        end)  lunch24,

    max(case sub.day
      when 25
        then sub.lunch
      else 0
      end)  lunch25,

    max(case sub.day
        when 26
          then sub.lunch
        else 0
        end)  lunch26,

    max(case sub.day
      when 27
        then sub.lunch
      else 0
      end)  lunch27,

    max(case sub.day
        when 28
          then sub.lunch
        else 0
        end)  lunch28,






    max(case sub.day
      when 1
        then sub.dinner
      else 0
      end)  dinner1,

    max(case sub.day
        when 2
          then sub.dinner
        else 0
        end)  dinner2,

      max(case sub.day
          when 3
            then sub.dinner
          else 0
          end)  dinner3,

    max(case sub.day
        when 4
          then sub.dinner
        else 0
        end)  dinner4,

    max(case sub.day
        when 5
          then sub.dinner
        else 0
        end)  dinner5,

    max(case sub.day
        when 6
          then sub.dinner
        else 0
        end)  dinner6,

    max(case sub.day
        when 7
          then sub.dinner
        else 0
        end)  dinner7,

    max(case sub.day
        when 8
          then sub.dinner
        else 0
        end)  dinner8,

    max(case sub.day
      when 9
        then sub.dinner
      else 0
      end)  dinner9,

    max(case sub.day
        when 10
          then sub.dinner
        else 0
        end)  dinner10,

    max(case sub.day
        when 11
          then sub.dinner
        else 0
        end)  dinner11,

    max(case sub.day
        when 12
          then sub.dinner
        else 0
        end)  dinner12,

    max(case sub.day
      when 13
        then sub.dinner
      else 0
      end)  dinner13,

    max(case sub.day
        when 14
          then sub.dinner
        else 0
        end)  dinner14,

    max(case sub.day
      when 15
        then sub.dinner
      else 0
      end)  dinner15,

    max(case sub.day
        when 16
          then sub.dinner
        else 0
        end)  dinner16,

    max(case sub.day
      when 17
        then sub.dinner
      else 0
      end)  dinner17,

    max(case sub.day
        when 18
          then sub.dinner
        else 0
        end)  dinner18,

    max(case sub.day
      when 19
        then sub.dinner
      else 0
      end)  dinner19,

    max(case sub.day
        when 20
          then sub.dinner
        else 0
        end)  dinner20,

    max(case sub.day
      when 21
        then sub.dinner
      else 0
      end)  dinner21,

    max(case sub.day
        when 22
          then sub.dinner
        else 0
        end)  dinner22,

    max(case sub.day
      when 23
        then sub.dinner
      else 0
      end)  dinner23,

    max(case sub.day
        when 24
          then sub.dinner
        else 0
        end)  dinner24,

    max(case sub.day
      when 25
        then sub.dinner
      else 0
      end)  dinner25,

    max(case sub.day
        when 26
          then sub.dinner
        else 0
        end)  dinner26,

    max(case sub.day
      when 27
        then sub.dinner
      else 0
      end)  dinner27,

    max(case sub.day
        when 28
          then sub.dinner
        else 0
        end)  dinner28,



    max(case sub.day
      when 1
        then sub.trainning
      else 0
      end)  trainning1,

    max(case sub.day
        when 2
          then sub.trainning
        else 0
        end)  trainning2,

      max(case sub.day
          when 3
            then sub.trainning
          else 0
          end)  trainning3,

    max(case sub.day
        when 4
          then sub.trainning
        else 0
        end)  trainning4,

    max(case sub.day
        when 5
          then sub.trainning
        else 0
        end)  trainning5,

    max(case sub.day
        when 6
          then sub.trainning
        else 0
        end)  trainning6,

    max(case sub.day
        when 7
          then sub.trainning
        else 0
        end)  trainning7,

    max(case sub.day
        when 8
          then sub.trainning
        else 0
        end)  trainning8,

    max(case sub.day
      when 9
        then sub.trainning
      else 0
      end)  trainning9,

    max(case sub.day
        when 10
          then sub.trainning
        else 0
        end)  trainning10,

    max(case sub.day
        when 11
          then sub.trainning
        else 0
        end)  trainning11,

    max(case sub.day
        when 12
          then sub.trainning
        else 0
        end)  trainning12,

    max(case sub.day
      when 13
        then sub.trainning
      else 0
      end)  trainning13,

    max(case sub.day
        when 14
          then sub.trainning
        else 0
        end)  trainning14,

    max(case sub.day
      when 15
        then sub.trainning
      else 0
      end)  trainning15,

    max(case sub.day
        when 16
          then sub.trainning
        else 0
        end)  trainning16,

    max(case sub.day
      when 17
        then sub.trainning
      else 0
      end)  trainning17,

    max(case sub.day
        when 18
          then sub.trainning
        else 0
        end)  trainning18,

    max(case sub.day
      when 19
        then sub.trainning
      else 0
      end)  trainning19,

    max(case sub.day
        when 20
          then sub.trainning
        else 0
        end)  trainning20,

    max(case sub.day
      when 21
        then sub.trainning
      else 0
      end)  trainning21,

    max(case sub.day
        when 22
          then sub.trainning
        else 0
        end)  trainning22,

    max(case sub.day
      when 23
        then sub.trainning
      else 0
      end)  trainning23,

    max(case sub.day
        when 24
          then sub.trainning
        else 0
        end)  trainning24,

    max(case sub.day
      when 25
        then sub.trainning
      else 0
      end)  trainning25,

    max(case sub.day
        when 26
          then sub.trainning
        else 0
        end)  trainning26,

    max(case sub.day
      when 27
        then sub.trainning
      else 0
      end)  trainning27,

    max(case sub.day
        when 28
          then sub.trainning
        else 0
        end)  trainning28







from (
  SELECT
    checkin.APPLY_ID,
    checkin.BREAKFAST breakfast,
    checkin.LUNCH lunch,
    checkin.DINNER dinner,
    checkin.TRAINNING trainning,
    (checkin.BREAKFAST + checkin.LUNCH + checkin.DINNER + checkin.TRAINNING) as checkinTimes,
      checkin.check_in_date check_date,
      term.CAMP_START_TIME start_date,
    DATEDIFF(checkin.CHECK_IN_DATE, term.CAMP_START_TIME)+1                       day

  FROM TB_CHECK_IN checkin
    LEFT JOIN TB_APPLY_RECORD apply ON apply.APPLY_ID = checkin.APPLY_ID
    LEFT JOIN TB_TERM term ON term.TERM_ID = apply.TERM_ID
    LEFT JOIN TB_ORDER tborder ON apply.PACKAGE_ORDER_ID = tborder.ORDER_ID
  WHERE tborder.OUTER_ORIGIN != 'exchange_white_list_test'
        AND term.TYPE = 1
        AND checkin.CHECK_IN_DATE >= term.CAMP_START_TIME
        AND checkin.CHECK_IN_DATE < date_add(term.CAMP_START_TIME, INTERVAL term.DAYS DAY)
        AND (checkin.BREAKFAST + checkin.LUNCH + checkin.DINNER + checkin.TRAINNING) > 0
        AND date_add(term.CAMP_START_TIME, INTERVAL term.DAYS DAY) > now()

  order by checkin.APPLY_ID, checkin.CHECK_IN_DATE
)sub
group by sub.APPLY_ID
    ''')


    for r in record:
        r_dic ={}
        r_dic['apply_Id'] = r.apply_Id
        r_dic['check1']= r.check1
        r_dic['check2']= r.check2
        r_dic['check3']= r.check3
        r_dic['check4']= r.check4
        r_dic['check5'] = r.check5
        r_dic['check6'] = r.check6

        r_dic['check7']= r.check7
        r_dic['check8']= r.check8
        r_dic['check9']= r.check9
        r_dic['check10']= r.check10
        r_dic['check11'] = r.check11
        r_dic['check12'] = r.check12

        r_dic['check13']= r.check13
        r_dic['check14']= r.check14
        r_dic['check15']= r.check15
        r_dic['check16']= r.check16
        r_dic['check17'] = r.check17
        r_dic['check18'] = r.check18

        r_dic['check19'] = r.check19
        r_dic['check20'] = r.check20
        r_dic['check21'] = r.check21
        r_dic['check22'] = r.check22
        r_dic['check23'] = r.check23
        r_dic['check24'] = r.check24

        r_dic['check25'] = r.check25
        r_dic['check26'] = r.check26
        r_dic['check27'] = r.check27
        r_dic['check28'] = r.check28




        r_dic['breakfast1'] = r.breakfast1
        r_dic['breakfast2'] = r.breakfast2
        r_dic['breakfast3'] = r.breakfast3
        r_dic['breakfast4'] = r.breakfast4
        r_dic['breakfast5'] = r.breakfast5
        r_dic['breakfast6'] = r.breakfast6

        r_dic['breakfast7'] = r.breakfast7
        r_dic['breakfast8'] = r.breakfast8
        r_dic['breakfast9'] = r.breakfast9
        r_dic['breakfast10'] = r.breakfast10
        r_dic['breakfast11'] = r.breakfast11
        r_dic['breakfast12'] = r.breakfast12

        r_dic['breakfast13'] = r.breakfast13
        r_dic['breakfast14'] = r.breakfast14
        r_dic['breakfast15'] = r.breakfast15
        r_dic['breakfast16'] = r.breakfast16
        r_dic['breakfast17'] = r.breakfast17
        r_dic['breakfast18'] = r.breakfast18

        r_dic['breakfast19'] = r.breakfast19
        r_dic['breakfast20'] = r.breakfast20
        r_dic['breakfast21'] = r.breakfast21
        r_dic['breakfast22'] = r.breakfast22
        r_dic['breakfast23'] = r.breakfast23
        r_dic['breakfast24'] = r.breakfast24

        r_dic['breakfast25'] = r.breakfast25
        r_dic['breakfast26'] = r.breakfast26
        r_dic['breakfast27'] = r.breakfast27
        r_dic['breakfast28'] = r.breakfast28





        r_dic['lunch1']= r.lunch1
        r_dic['lunch2']= r.lunch2
        r_dic['lunch3']= r.lunch3
        r_dic['lunch4']= r.lunch4
        r_dic['lunch5'] = r.lunch5
        r_dic['lunch6'] = r.lunch6

        r_dic['lunch7']= r.lunch7
        r_dic['lunch8']= r.lunch8
        r_dic['lunch9']= r.lunch9
        r_dic['lunch10']= r.lunch10
        r_dic['lunch11'] = r.lunch11
        r_dic['lunch12'] = r.lunch12

        r_dic['lunch13']= r.lunch13
        r_dic['lunch14']= r.lunch14
        r_dic['lunch15']= r.lunch15
        r_dic['lunch16']= r.lunch16
        r_dic['lunch17'] = r.lunch17
        r_dic['lunch18'] = r.lunch18

        r_dic['lunch19'] = r.lunch19
        r_dic['lunch20'] = r.lunch20
        r_dic['lunch21'] = r.lunch21
        r_dic['lunch22'] = r.lunch22
        r_dic['lunch23'] = r.lunch23
        r_dic['lunch24'] = r.lunch24

        r_dic['lunch25'] = r.lunch25
        r_dic['lunch26'] = r.lunch26
        r_dic['lunch27'] = r.lunch27
        r_dic['lunch28'] = r.lunch28


        r_dic['dinner1'] = r.dinner1
        r_dic['dinner2'] = r.dinner2
        r_dic['dinner3'] = r.dinner3
        r_dic['dinner4'] = r.dinner4
        r_dic['dinner5'] = r.dinner5
        r_dic['dinner6'] = r.dinner6

        r_dic['dinner7'] = r.dinner7
        r_dic['dinner8'] = r.dinner8
        r_dic['dinner9'] = r.dinner9
        r_dic['dinner10'] = r.dinner10
        r_dic['dinner11'] = r.dinner11
        r_dic['dinner12'] = r.dinner12

        r_dic['dinner13'] = r.dinner13
        r_dic['dinner14'] = r.dinner14
        r_dic['dinner15'] = r.dinner15
        r_dic['dinner16'] = r.dinner16
        r_dic['dinner17'] = r.dinner17
        r_dic['dinner18'] = r.dinner18

        r_dic['dinner19'] = r.dinner19
        r_dic['dinner20'] = r.dinner20
        r_dic['dinner21'] = r.dinner21
        r_dic['dinner22'] = r.dinner22
        r_dic['dinner23'] = r.dinner23
        r_dic['dinner24'] = r.dinner24

        r_dic['dinner25'] = r.dinner25
        r_dic['dinner26'] = r.dinner26
        r_dic['dinner27'] = r.dinner27
        r_dic['dinner28'] = r.dinner28





        r_dic['trainning1'] = r.trainning1
        r_dic['trainning2'] = r.trainning2
        r_dic['trainning3'] = r.trainning3
        r_dic['trainning4'] = r.trainning4
        r_dic['trainning5'] = r.trainning5
        r_dic['trainning6'] = r.trainning6

        r_dic['trainning7'] = r.trainning7
        r_dic['trainning8'] = r.trainning8
        r_dic['trainning9'] = r.trainning9
        r_dic['trainning10'] = r.trainning10
        r_dic['trainning11'] = r.trainning11
        r_dic['trainning12'] = r.trainning12

        r_dic['trainning13'] = r.trainning13
        r_dic['trainning14'] = r.trainning14
        r_dic['trainning15'] = r.trainning15
        r_dic['trainning16'] = r.trainning16
        r_dic['trainning17'] = r.trainning17
        r_dic['trainning18'] = r.trainning18

        r_dic['trainning19'] = r.trainning19
        r_dic['trainning20'] = r.trainning20
        r_dic['trainning21'] = r.trainning21
        r_dic['trainning22'] = r.trainning22
        r_dic['trainning23'] = r.trainning23
        r_dic['trainning24'] = r.trainning24

        r_dic['trainning25'] = r.trainning25
        r_dic['trainning26'] = r.trainning26
        r_dic['trainning27'] = r.trainning27
        r_dic['trainning28'] = r.trainning28

        # 因为breakfast lunch dinner trainning 都是string 类型 ，需要转成 float
        for k , v in r_dic.items():
            r_dic[k] = float(v)

        trainDatas.append(r_dic)



    if not camp_db.is_closed():
        camp_db.close()

    return trainDatas



# 提取所有未结营的说话信息
def get_day_speak():
    trainDatas = []
    if camp_db.is_closed():
        camp_db.connect()

    record = RawModel.raw('''
    select
  sub.id apply_Id,
  max(case sub.day
      when 1
        then sub.speak_one_day
      else 0
      end) speak1,

  max(case sub.day
      when 2
        then sub.speak_one_day
      else 0
      end)  speak2,

  max(case sub.day
          when 3
            then sub.speak_one_day
          else 0
          end)  speak3,

  max(case sub.day
        when 4
          then sub.speak_one_day
        else 0
        end)  speak4,

  max(case sub.day
        when 5
          then sub.speak_one_day
        else 0
        end)  speak5,

  max(case sub.day
        when 6
          then sub.speak_one_day
        else 0
        end)  speak6,

  max(case sub.day
        when 7
          then sub.speak_one_day
        else 0
        end)  speak7,

    max(case sub.day
        when 8
          then sub.speak_one_day
        else 0
        end)  speak8,

    max(case sub.day
      when 9
        then sub.speak_one_day
      else 0
      end)  speak9,

    max(case sub.day
        when 10
          then sub.speak_one_day
        else 0
        end)  speak10,

    max(case sub.day
        when 11
          then sub.speak_one_day
        else 0
        end)  speak11,

    max(case sub.day
        when 12
          then sub.speak_one_day
        else 0
        end)  speak12,

    max(case sub.day
      when 13
        then sub.speak_one_day
      else 0
      end)  speak13,

    max(case sub.day
        when 14
          then sub.speak_one_day
        else 0
        end)  speak14,

    max(case sub.day
      when 15
        then sub.speak_one_day
      else 0
      end)  speak15,

    max(case sub.day
        when 16
          then sub.speak_one_day
        else 0
        end)  speak16,

    max(case sub.day
      when 17
        then sub.speak_one_day
      else 0
      end)  speak17,

    max(case sub.day
        when 18
          then sub.speak_one_day
        else 0
        end)  speak18,

    max(case sub.day
      when 19
        then sub.speak_one_day
      else 0
      end)  speak19,

    max(case sub.day
        when 20
          then sub.speak_one_day
        else 0
        end)  speak20,

    max(case sub.day
      when 21
        then sub.speak_one_day
      else 0
      end)  speak21,

    max(case sub.day
        when 22
          then sub.speak_one_day
        else 0
        end)  speak22,

    max(case sub.day
      when 23
        then sub.speak_one_day
      else 0
      end)  speak23,

    max(case sub.day
        when 24
          then sub.speak_one_day
        else 0
        end)  speak24,

    max(case sub.day
      when 25
        then sub.speak_one_day
      else 0
      end)  speak25,

    max(case sub.day
        when 26
          then sub.speak_one_day
        else 0
        end)  speak26,

    max(case sub.day
      when 27
        then sub.speak_one_day
      else 0
      end)  speak27,

    max(case sub.day
        when 28
          then sub.speak_one_day
        else 0
        end)  speak28,






  max(case sub.day
      when 1
        then sub.GREED
      else 0
      end) greed1,

  max(case sub.day
      when 2
        then sub.GREED
      else 0
      end)  greed2,

  max(case sub.day
          when 3
            then sub.GREED
          else 0
          end)  greed3,

  max(case sub.day
        when 4
          then sub.GREED
        else 0
        end)  greed4,

  max(case sub.day
        when 5
          then sub.GREED
        else 0
        end)  greed5,

  max(case sub.day
        when 6
          then sub.GREED
        else 0
        end)  greed6,

  max(case sub.day
        when 7
          then sub.GREED
        else 0
        end)  greed7,

    max(case sub.day
        when 8
          then sub.GREED
        else 0
        end)  greed8,

    max(case sub.day
      when 9
        then sub.GREED
      else 0
      end)  greed9,

    max(case sub.day
        when 10
          then sub.GREED
        else 0
        end)  greed10,

    max(case sub.day
        when 11
          then sub.GREED
        else 0
        end)  greed11,

    max(case sub.day
        when 12
          then sub.GREED
        else 0
        end)  greed12,

    max(case sub.day
      when 13
        then sub.GREED
      else 0
      end)  greed13,

    max(case sub.day
        when 14
          then sub.GREED
        else 0
        end)  greed14,

    max(case sub.day
      when 15
        then sub.GREED
      else 0
      end)  greed15,

    max(case sub.day
        when 16
          then sub.GREED
        else 0
        end)  greed16,

    max(case sub.day
      when 17
        then sub.GREED
      else 0
      end)  greed17,

    max(case sub.day
        when 18
          then sub.GREED
        else 0
        end)  greed18,

    max(case sub.day
      when 19
        then sub.GREED
      else 0
      end)  greed19,

    max(case sub.day
        when 20
          then sub.GREED
        else 0
        end)  greed20,

    max(case sub.day
      when 21
        then sub.GREED
      else 0
      end)  greed21,

    max(case sub.day
        when 22
          then sub.GREED
        else 0
        end)  greed22,

    max(case sub.day
      when 23
        then sub.GREED
      else 0
      end)  greed23,

    max(case sub.day
        when 24
          then sub.GREED
        else 0
        end)  greed24,

    max(case sub.day
      when 25
        then sub.GREED
      else 0
      end)  greed25,

    max(case sub.day
        when 26
          then sub.GREED
        else 0
        end)  greed26,

    max(case sub.day
      when 27
        then sub.GREED
      else 0
      end)  greed27,

    max(case sub.day
        when 28
          then sub.GREED
        else 0
        end)  greed28,



  max(case sub.day
      when 1
        then sub.PRESSURE
      else 0
      end) pressure1,

  max(case sub.day
      when 2
        then sub.PRESSURE
      else 0
      end)  pressure2,

  max(case sub.day
          when 3
            then sub.PRESSURE
          else 0
          end)  pressure3,

  max(case sub.day
        when 4
          then sub.PRESSURE
        else 0
        end)  pressure4,

  max(case sub.day
        when 5
          then sub.PRESSURE
        else 0
        end)  pressure5,

  max(case sub.day
        when 6
          then sub.PRESSURE
        else 0
        end)  pressure6,

  max(case sub.day
        when 7
          then sub.PRESSURE
        else 0
        end)  pressure7,

    max(case sub.day
        when 8
          then sub.PRESSURE
        else 0
        end)  pressure8,

    max(case sub.day
      when 9
        then sub.PRESSURE
      else 0
      end)  pressure9,

    max(case sub.day
        when 10
          then sub.PRESSURE
        else 0
        end)  pressure10,

    max(case sub.day
        when 11
          then sub.PRESSURE
        else 0
        end)  pressure11,

    max(case sub.day
        when 12
          then sub.PRESSURE
        else 0
        end)  pressure12,

    max(case sub.day
      when 13
        then sub.PRESSURE
      else 0
      end)  pressure13,

    max(case sub.day
        when 14
          then sub.PRESSURE
        else 0
        end)  pressure14,

    max(case sub.day
      when 15
        then sub.PRESSURE
      else 0
      end)  pressure15,

    max(case sub.day
        when 16
          then sub.PRESSURE
        else 0
        end)  pressure16,

    max(case sub.day
      when 17
        then sub.PRESSURE
      else 0
      end)  pressure17,

    max(case sub.day
        when 18
          then sub.PRESSURE
        else 0
        end)  pressure18,

    max(case sub.day
      when 19
        then sub.PRESSURE
      else 0
      end)  pressure19,

    max(case sub.day
        when 20
          then sub.PRESSURE
        else 0
        end)  pressure20,

    max(case sub.day
      when 21
        then sub.PRESSURE
      else 0
      end)  pressure21,

    max(case sub.day
        when 22
          then sub.PRESSURE
        else 0
        end)  pressure22,

    max(case sub.day
      when 23
        then sub.PRESSURE
      else 0
      end)  pressure23,

    max(case sub.day
        when 24
          then sub.PRESSURE
        else 0
        end)  pressure24,

    max(case sub.day
      when 25
        then sub.PRESSURE
      else 0
      end)  pressure25,

    max(case sub.day
        when 26
          then sub.PRESSURE
        else 0
        end)  pressure26,

    max(case sub.day
      when 27
        then sub.PRESSURE
      else 0
      end)  pressure27,

    max(case sub.day
        when 28
          then sub.PRESSURE
        else 0
        end)  pressure28,




  max(case sub.day
      when 1
        then sub.MENSTRUAL
      else 0
      end) menstrual1,

  max(case sub.day
      when 2
        then sub.MENSTRUAL
      else 0
      end)  menstrual2,

  max(case sub.day
          when 3
            then sub.MENSTRUAL
          else 0
          end)  menstrual3,

  max(case sub.day
        when 4
          then sub.MENSTRUAL
        else 0
        end)  menstrual4,

  max(case sub.day
        when 5
          then sub.MENSTRUAL
        else 0
        end)  menstrual5,

  max(case sub.day
        when 6
          then sub.MENSTRUAL
        else 0
        end)  menstrual6,

  max(case sub.day
        when 7
          then sub.MENSTRUAL
        else 0
        end)  menstrual7,

    max(case sub.day
        when 8
          then sub.MENSTRUAL
        else 0
        end)  menstrual8,

    max(case sub.day
      when 9
        then sub.MENSTRUAL
      else 0
      end)  menstrual9,

    max(case sub.day
        when 10
          then sub.MENSTRUAL
        else 0
        end)  menstrual10,

    max(case sub.day
        when 11
          then sub.MENSTRUAL
        else 0
        end)  menstrual11,

    max(case sub.day
        when 12
          then sub.MENSTRUAL
        else 0
        end)  menstrual12,

    max(case sub.day
      when 13
        then sub.MENSTRUAL
      else 0
      end)  menstrual13,

    max(case sub.day
        when 14
          then sub.MENSTRUAL
        else 0
        end)  menstrual14,

    max(case sub.day
      when 15
        then sub.MENSTRUAL
      else 0
      end)  menstrual15,

    max(case sub.day
        when 16
          then sub.MENSTRUAL
        else 0
        end)  menstrual16,

    max(case sub.day
      when 17
        then sub.MENSTRUAL
      else 0
      end)  menstrual17,

    max(case sub.day
        when 18
          then sub.MENSTRUAL
        else 0
        end)  menstrual18,

    max(case sub.day
      when 19
        then sub.MENSTRUAL
      else 0
      end)  menstrual19,

    max(case sub.day
        when 20
          then sub.MENSTRUAL
        else 0
        end)  menstrual20,

    max(case sub.day
      when 21
        then sub.MENSTRUAL
      else 0
      end)  menstrual21,

    max(case sub.day
        when 22
          then sub.MENSTRUAL
        else 0
        end)  menstrual22,

    max(case sub.day
      when 23
        then sub.MENSTRUAL
      else 0
      end)  menstrual23,

    max(case sub.day
        when 24
          then sub.MENSTRUAL
        else 0
        end)  menstrual24,

    max(case sub.day
      when 25
        then sub.MENSTRUAL
      else 0
      end)  menstrual25,

    max(case sub.day
        when 26
          then sub.MENSTRUAL
        else 0
        end)  menstrual26,

    max(case sub.day
      when 27
        then sub.MENSTRUAL
      else 0
      end)  menstrual27,

    max(case sub.day
        when 28
          then sub.MENSTRUAL
        else 0
        end)  menstrual28


from (
select
  apply.APPLY_ID id,
  cr.content content,
  cr.createTime  time,
  cr.wxID        weixin,
  DATEDIFF(cr.createTime , term.CAMP_START_TIME)+1 day,
  count(1) speak_one_day,
  SUM(if(instr(cr.content, '馋'), 1, 0))                        as GREED,
  SUM(if(instr(cr.content, '压力'), 1, 0))                       as PRESSURE,
  SUM(if(instr(cr.content, '经期')
         or instr(cr.content, '月经')
         or instr(cr.content, '例假')
         or instr(cr.content, '姨妈'), 1, 0))                    as MENSTRUAL
from chatrecord.chat_record cr
  left join
  (
    select max(u.applyId) as Id, wxID
    from  chatrecord.user_group u
    group by Id
  ) ug on cr.wxID = ug.wxID
  left join eshop.TB_APPLY_RECORD apply on apply.apply_id = ug.Id
  left JOIN eshop.TB_TERM term ON term.TERM_ID = apply.TERM_ID
where apply.APPLY_ID is not null
      AND term.TYPE = 1
      AND cr.createTime >= term.CAMP_START_TIME
      AND cr.createTime < date_add(term.CAMP_START_TIME, INTERVAL term.DAYS DAY)
      AND date_add(term.CAMP_START_TIME, INTERVAL term.DAYS DAY) > now()

group by id,day
order by cr.wxID, cr.createTime
)sub
group by apply_Id

    ''')


    for r in record:
        r_dic ={}
        r_dic['apply_Id'] = r.apply_Id
        r_dic['speak1']= r.speak1
        r_dic['speak2']= r.speak2
        r_dic['speak3']= r.speak3
        r_dic['speak4']= r.speak4
        r_dic['speak5'] = r.speak5
        r_dic['speak6'] = r.speak6

        r_dic['speak7']= r.speak7
        r_dic['speak8']= r.speak8
        r_dic['speak9']= r.speak9
        r_dic['speak10']= r.speak10
        r_dic['speak11'] = r.speak11
        r_dic['speak12'] = r.speak12

        r_dic['speak13']= r.speak13
        r_dic['speak14']= r.speak14
        r_dic['speak15']= r.speak15
        r_dic['speak16']= r.speak16
        r_dic['speak17'] = r.speak17
        r_dic['speak18'] = r.speak18

        r_dic['speak19'] = r.speak19
        r_dic['speak20'] = r.speak20
        r_dic['speak21'] = r.speak21
        r_dic['speak22'] = r.speak22
        r_dic['speak23'] = r.speak23
        r_dic['speak24'] = r.speak24

        r_dic['speak25'] = r.speak25
        r_dic['speak26'] = r.speak26
        r_dic['speak27'] = r.speak27
        r_dic['speak28'] = r.speak28



        r_dic['greed1']= r.greed1
        r_dic['greed2']= r.greed2
        r_dic['greed3']= r.greed3
        r_dic['greed4']= r.greed4
        r_dic['greed5'] = r.greed5
        r_dic['greed6'] = r.greed6

        r_dic['greed7']= r.greed7
        r_dic['greed8']= r.greed8
        r_dic['greed9']= r.greed9
        r_dic['greed10']= r.greed10
        r_dic['greed11'] = r.greed11
        r_dic['greed12'] = r.greed12

        r_dic['greed13']= r.greed13
        r_dic['greed14']= r.greed14
        r_dic['greed15']= r.greed15
        r_dic['greed16']= r.greed16
        r_dic['greed17'] = r.greed17
        r_dic['greed18'] = r.greed18

        r_dic['greed19'] = r.greed19
        r_dic['greed20'] = r.greed20
        r_dic['greed21'] = r.greed21
        r_dic['greed22'] = r.greed22
        r_dic['greed23'] = r.greed23
        r_dic['greed24'] = r.greed24

        r_dic['greed25'] = r.greed25
        r_dic['greed26'] = r.greed26
        r_dic['greed27'] = r.greed27
        r_dic['greed28'] = r.greed28





        r_dic['pressure1']= r.pressure1
        r_dic['pressure2']= r.pressure2
        r_dic['pressure3']= r.pressure3
        r_dic['pressure4']= r.pressure4
        r_dic['pressure5'] = r.pressure5
        r_dic['pressure6'] = r.pressure6

        r_dic['pressure7']= r.pressure7
        r_dic['pressure8']= r.pressure8
        r_dic['pressure9']= r.pressure9
        r_dic['pressure10']= r.pressure10
        r_dic['pressure11'] = r.pressure11
        r_dic['pressure12'] = r.pressure12

        r_dic['pressure13']= r.pressure13
        r_dic['pressure14']= r.pressure14
        r_dic['pressure15']= r.pressure15
        r_dic['pressure16']= r.pressure16
        r_dic['pressure17'] = r.pressure17
        r_dic['pressure18'] = r.pressure18

        r_dic['pressure19'] = r.pressure19
        r_dic['pressure20'] = r.pressure20
        r_dic['pressure21'] = r.pressure21
        r_dic['pressure22'] = r.pressure22
        r_dic['pressure23'] = r.pressure23
        r_dic['pressure24'] = r.pressure24

        r_dic['pressure25'] = r.pressure25
        r_dic['pressure26'] = r.pressure26
        r_dic['pressure27'] = r.pressure27
        r_dic['pressure28'] = r.pressure28


        r_dic['menstrual1']= r.menstrual1
        r_dic['menstrual2']= r.menstrual2
        r_dic['menstrual3']= r.menstrual3
        r_dic['menstrual4']= r.menstrual4
        r_dic['menstrual5'] = r.menstrual5
        r_dic['menstrual6'] = r.menstrual6

        r_dic['menstrual7']= r.menstrual7
        r_dic['menstrual8']= r.menstrual8
        r_dic['menstrual9']= r.menstrual9
        r_dic['menstrual10']= r.menstrual10
        r_dic['menstrual11'] = r.menstrual11
        r_dic['menstrual12'] = r.menstrual12

        r_dic['menstrual13']= r.menstrual13
        r_dic['menstrual14']= r.menstrual14
        r_dic['menstrual15']= r.menstrual15
        r_dic['menstrual16']= r.menstrual16
        r_dic['menstrual17'] = r.menstrual17
        r_dic['menstrual18'] = r.menstrual18

        r_dic['menstrual19'] = r.menstrual19
        r_dic['menstrual20'] = r.menstrual20
        r_dic['menstrual21'] = r.menstrual21
        r_dic['menstrual22'] = r.menstrual22
        r_dic['menstrual23'] = r.menstrual23
        r_dic['menstrual24'] = r.menstrual24

        r_dic['menstrual25'] = r.menstrual25
        r_dic['menstrual26'] = r.menstrual26
        r_dic['menstrual27'] = r.menstrual27
        r_dic['menstrual28'] = r.menstrual28

        #menstrual 数据存在sql decimal('0') 类型 ，需要转换成float
        for k , v in r_dic.items():
            r_dic[k] = float(v)

        trainDatas.append(r_dic)

    return trainDatas



#用applyID 将打卡信息 ,说话信息 填充进 not_over_term_list(装体重的数据结构)
def get_all_data(not_over_term_list , cl ,sl ):
    for term_num_dic in not_over_term_list:
        for person in term_num_dic['predict_data']:
            for i in range(1, 29):
                person['check%d' % i] = 0
                person['breakfast%d' % i] = 0
                person['lunch%d' % i] = 0
                person['dinner%d' % i] = 0
                person['trainning%d' % i] = 0
                person['speak%d' % i] = 0
                person['greed%d' % i] = 0
                person['pressure%d' % i] = 0
                person['menstrual%d' % i] = 0

        for person in term_num_dic['predict_data']:
            apply_Id = person['apply_Id']

            for person2 in cl:
                if person2['apply_Id'] == apply_Id:
                    for i in range(1, 29):
                        person['check%d' % i] = person2['check%d' % i]
                        person['breakfast%d' % i] = person2['breakfast%d' % i]
                        person['lunch%d' % i] = person2['lunch%d' % i]
                        person['dinner%d' % i] = person2['dinner%d' % i]
                        person['trainning%d' % i] = person2['trainning%d' % i]
                    break

            for person3 in sl:
                if person3['apply_Id'] == apply_Id:
                    for i in range(1, 29):
                        person['speak%d' % i] = person3['speak%d' % i]
                        person['greed%d' % i] = person3['greed%d' % i]
                        person['pressure%d' % i] = person3['pressure%d' % i]
                        person['menstrual%d' % i] = person3['menstrual%d' % i]
                    break

    return not_over_term_list



# 从前向后填充体重
def add_null_weight(not_over_term_list):
    # not_over_term_list = [{'termID': 261, 'term_num': 114, 'predict_day': 22 , 'predict_data':[{'apply_Id':_ , 'term_num':_ ,}...]}, ,,]
    for term_num_dic in not_over_term_list:
        for person in term_num_dic['predict_data']:
            last_record_weight = person['week0Weight']

            for time in range(1,29):
                if person['day%dWeight'%time] == 0:
                    person['day%dWeight'%time] = last_record_weight
                else:
                    last_record_weight = person['day%dWeight'%time]

    return not_over_term_list



def show(not_over_term_list , predict0_list):
    predict_dic = {}
    term_set = []
    for person in predict0_list:
        term_set.append(person['term'])
    term_set = list(set(term_set))

    for term in term_set:
        predict_dic[term] = 0

    for person in predict0_list:
        predict_dic[person['term']] +=1

    all_list =[]
    for term_dic in not_over_term_list:
        show_list = {}
        show_list['term'] = term_dic['term_num']
        show_list['total'] = len(term_dic['predict_data'])
        show_list['run'] = predict_dic[term_dic['term_num']]
        all_list.append(show_list)
    print(all_list)

    return






#[{'term': 114, 'name': '马超', 'day': 22}, {'term': 114, 'name': '郭佳仪', 'day': 22}, {'term': 114, 'name': '祖朋', 'day': 22}, {'term': 114, 'name': '肖迪', 'day': 22}, {'term': 114, 'name': '大兵', 'day': 22}, {'term': 114, 'name': '黄凡', 'day': 22}, {'term': 114, 'name': '冯姣', 'day': 22}, {'term': 114, 'name': '杨义飞', 'day': 22}, {'term': 114, 'name': '杨玙', 'day': 22}, {'term': 114, 'name': '安大人', 'day': 22}, {'term': 114, 'name': '潘灯', 'day': 22}, {'term': 114, 'name': '高琳', 'day': 22}, {'term': 114, 'name': '贾祯祯', 'day': 22}, {'term': 114, 'name': '邢扬和', 'day': 22}, {'term': 114, 'name': '袁颖', 'day': 22}, {'term': 114, 'name': '徐凯', 'day': 22}, {'term': 114, 'name': '王姝妍', 'day': 22}, {'term': 114, 'name': '程惠娟', 'day': 22}, {'term': 114, 'name': '谢智文', 'day': 22}, {'term': 114, 'name': '耿聪', 'day': 22}, {'term': 114, 'name': '三米', 'day': 22}, {'term': 114, 'name': '杨远屏', 'day': 22}, {'term': 114, 'name': '李佳欣', 'day': 22}, {'term': 114, 'name': '谢丽', 'day': 22}, {'term': 114, 'name': '萧琳琳', 'day': 22}, {'term': 114, 'name': '张莹', 'day': 22}, {'term': 114, 'name': '彭捷才', 'day': 22}, {'term': 114, 'name': '张放', 'day': 22}, {'term': 114, 'name': '金一帆', 'day': 22}, {'term': 114, 'name': '迟小宝', 'day': 22}, {'term': 114, 'name': '张国正', 'day': 22}, {'term': 114, 'name': '邓洁星', 'day': 22}, {'term': 114, 'name': '高阳雪', 'day': 22}, {'term': 114, 'name': '郭思明', 'day': 22}, {'term': 114, 'name': '陆青峰', 'day': 22}, {'term': 114, 'name': '戴倩媛', 'day': 22}, {'term': 115, 'name': '高家林', 'day': 15}, {'term': 115, 'name': '蔡洵', 'day': 15}, {'term': 115, 'name': '朱子涵', 'day': 15}, {'term': 115, 'name': '米奇', 'day': 15}, {'term': 115, 'name': '单丹丹', 'day': 15}, {'term': 115, 'name': '林琪琪', 'day': 15}, {'term': 115, 'name': '樊宇芳', 'day': 15}, {'term': 115, 'name': '华丹', 'day': 15}, {'term': 115, 'name': '胡霜颖', 'day': 15}, {'term': 116, 'name': '刘瑞琦', 'day': 8}, {'term': 116, 'name': '陈欣欣', 'day': 8}, {'term': 116, 'name': '王萌', 'day': 8}, {'term': 116, 'name': '任雨', 'day': 8}, {'term': 116, 'name': '张河', 'day': 8}, {'term': 116, 'name': '黄婷', 'day': 8}, {'term': 116, 'name': '黄蕗颖', 'day': 8}, {'term': 116, 'name': 'Aaliyah', 'day': 8}, {'term': 116, 'name': '孙永妍', 'day': 8}, {'term': 116, 'name': '赵马一', 'day': 8}, {'term': 116, 'name': '陈瑞珊', 'day': 8}, {'term': 117, 'name': '赵七七', 'day': 1}, {'term': 117, 'name': '程阳', 'day': 1}, {'term': 117, 'name': '李楠', 'day': 1}]
def make_xls_file_with_all_message(predict0_list, file_type):
    date_now = time.strftime('%Y-%m-%d', time.localtime())

    file = Workbook(encoding='utf-8')
    table = file.add_sheet('data')

    data_list = [['学期','姓名','手机','开营时间','要跑的日期','用1-n天数据预测','待的时间']]

    for day in range(1, 27):
        data_list[0].append('第%d天体重' % day)
        data_list[0].append('第%d天早餐' % day)
        data_list[0].append('第%d天午餐' % day)
        data_list[0].append('第%d天晚餐' % day)
        data_list[0].append('第%d天运动' % day)
        data_list[0].append('第%d天说话' % day)
        data_list[0].append('第%d天说馋次数' % day)
        data_list[0].append('第%d天说压力次数' % day)
        data_list[0].append('第%d天说月经次数' % day)

    for person in predict0_list:
        data = []
        for k , v in person.items():
            if k == 'day':
                data.append(date_now)
            data.append(v)
        data_list.append(data)


    for i, p in enumerate(data_list):
        for j, q in enumerate(p):
            table.write(i, j, q)

    if file_type == 'predict':
        file.save('./every_day_result/预测要跑.xls')
    elif file_type == 'already_leave':
        file.save('./every_day_result/已经跑了.xls')

    return


def no_weight_make_xls_file_with_all_message(no_weight_predict0_list):
    date_now = time.strftime('%Y-%m-%d', time.localtime())

    file = Workbook(encoding='utf-8')
    table = file.add_sheet('data2')

    data_list = [['学期','姓名','手机','开营时间','要跑的日期','用1-n天数据预测','待的时间']]

    for day in range(1, 27):
        data_list[0].append('第%d天早餐' % day)
        data_list[0].append('第%d天午餐' % day)
        data_list[0].append('第%d天晚餐' % day)
        data_list[0].append('第%d天运动' % day)
        data_list[0].append('第%d天说话' % day)
        data_list[0].append('第%d天说馋次数' % day)
        data_list[0].append('第%d天说压力次数' % day)
        data_list[0].append('第%d天说月经次数' % day)

    for person in no_weight_predict0_list:
        data = []
        for k , v in person.items():
            if k == 'day':
                data.append(date_now)
            data.append(v)
        data_list.append(data)


    for i, p in enumerate(data_list):
        for j, q in enumerate(p):
            table.write(i, j, q)
    file.save('./every_day_result/无体重名单.xls')

    return


# 拿到这个人最后有活动的天数
def get_last_stay_time(person_dic, day_len):
    day_check_speak_list = []
    day_weight_list = [person_dic['week0Weight']]

    for time in range(1, day_len+1):
        day_check = person_dic['breakfast%d'%time] +person_dic['lunch%d'%time]+person_dic['dinner%d'%time]+person_dic['trainning%d'%time]+ person_dic['speak%d'%time]

        day_check_speak_list.append(day_check)
        day_weight_list.append(person_dic['day%dWeight'%time])


    sum_not_check_speak_time = 0
    for i in range(len(day_check_speak_list)-1, -1 , -1):
        if day_check_speak_list[i] == 0:
            sum_not_check_speak_time += 1
        else:
            break

    # check_speak_stay_time = 这人打卡持续的天数
    check_speak_stay_time = day_len - sum_not_check_speak_time



    last_day_weight = person_dic['day%dWeight'%day_len]
    sum_weight_not_change = 1
    for i in range(len(day_weight_list)-2 , -1, -1):
        if day_weight_list[i] == last_day_weight:
            sum_weight_not_change += 1
        else:
            break

    # weight_stay_time = 这人记录体重持续的天数
    if sum_weight_not_change > day_len:
        weight_stay_time = 0
    else:
        weight_stay_time = day_len - sum_weight_not_change + 1


    if weight_stay_time >= check_speak_stay_time:
        return weight_stay_time
    else:
        return check_speak_stay_time



# 拿到这个人最后有活动的天数
def no_weight_get_last_stay_time(person_dic, day_len):
    day_check_speak_list = []

    for time in range(1, day_len+1):
        day_check = person_dic['breakfast%d'%time] +person_dic['lunch%d'%time]+person_dic['dinner%d'%time]+person_dic['trainning%d'%time]+ person_dic['speak%d'%time]
        day_check_speak_list.append(day_check)


    sum_not_check_speak_time = 0
    for i in range(len(day_check_speak_list)-1, -1 , -1):
        if day_check_speak_list[i] == 0:
            sum_not_check_speak_time += 1
        else:
            break

    # check_speak_stay_time = 这人打卡持续的天数
    check_speak_stay_time = day_len - sum_not_check_speak_time

    return check_speak_stay_time



# 移除在预测之前已经离开的人 ，并将他们以字典形式 ，写入一个列表
def cut_already_leave_person_before_predict(not_over_term_list):
    already_leave_list = []

    for term_num_dic in not_over_term_list:
        # print(term_num_dic['term_num'],'期 =',len(term_num_dic['predict_data']),'人')
        day_len = term_num_dic['predict_day']
        term_already_leave_list = []

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

        remove_id_list = []
        for person in term_num_dic['predict_data']:

            day_len = term_num_dic['predict_day']
            person_real_stay_time = get_last_stay_time(person, day_len)
            if person_real_stay_time < day_len:
                person_dic = {}
                person_dic['term'] = person['term_num']
                person_dic['name'] = person['name']
                person_dic['phone'] = person['phone']
                person_dic['camp_start_time'] = term_num_dic['camp_start_time']
                person_dic['day'] = term_num_dic['predict_day']
                person_dic['stay_day'] = person_real_stay_time

                for feature in feature_map:
                    person_dic[feature] = person[feature]

                term_already_leave_list.append(person_dic)
                remove_id_list.append(person['apply_Id'])



        for id in remove_id_list:
            for person in term_num_dic['predict_data']:
                if id == person['apply_Id']:
                    term_num_dic['predict_data'].remove(person)
                    break





        # 对term_already_leave_list 'stay_day' 升序排序
        term_already_leave_list = sorted(term_already_leave_list, key=operator.itemgetter('stay_day'), reverse=1)
        already_leave_list.extend(term_already_leave_list)


    return already_leave_list , not_over_term_list


# (无体重版本) 移除在预测之前已经离开的人 ，并将他们以字典形式 ，写入一个列表
def no_weight_cut_already_leave_person_before_predict(no_weight_not_over_term_list):
    already_leave_list = []

    for term_num_dic in no_weight_not_over_term_list:

        day_len = term_num_dic['predict_day']
        term_already_leave_list = []

        feature_map = []
        for day in range(1, day_len + 1):
            feature_map.append('breakfast%d' % day)
            feature_map.append('lunch%d' % day)
            feature_map.append('dinner%d' % day)
            feature_map.append('trainning%d' % day)
            feature_map.append('speak%d' % day)
            feature_map.append('greed%d' % day)
            feature_map.append('pressure%d' % day)
            feature_map.append('menstrual%d' % day)

        remove_id_list = []
        for person in term_num_dic['predict_data']:

            day_len = term_num_dic['predict_day']
            person_real_stay_time = no_weight_get_last_stay_time(person, day_len)
            if person_real_stay_time < day_len:
                person_dic = {}
                person_dic['term'] = person['term_num']
                person_dic['name'] = person['name']
                person_dic['phone'] = person['phone']
                person_dic['camp_start_time'] = term_num_dic['camp_start_time']
                person_dic['day'] = term_num_dic['predict_day']
                person_dic['stay_day'] = person_real_stay_time

                for feature in feature_map:
                    person_dic[feature] = person[feature]

                term_already_leave_list.append(person_dic)
                remove_id_list.append(person['apply_Id'])



        for id in remove_id_list:
            for person in term_num_dic['predict_data']:
                if id == person['apply_Id']:
                    term_num_dic['predict_data'].remove(person)
                    break




        # 对term_already_leave_list 'stay_day' 升序排序
        term_already_leave_list = sorted(term_already_leave_list, key=operator.itemgetter('stay_day'), reverse=1)
        already_leave_list.extend(term_already_leave_list)


    return already_leave_list , no_weight_not_over_term_list


# 从 no_weight_not_over_term_list(所有applyID)  删除  not_over_term_list(有体重的applyID) 中有体重的人
def remove_weight_person(no_weight_not_over_term_list, not_over_term_list):
    #no_weight_not_over_term_list 此时是全applyID
    #not_over_term_list  有体重的applyID

    for no_weight_term in no_weight_not_over_term_list:
        term_num = no_weight_term['term_num']

        remove_id_list = []
        for weight_term in not_over_term_list:
            if weight_term['term_num'] == term_num:
                for person in weight_term['predict_data']:
                    remove_id_list.append(person['apply_Id'])

        for id in remove_id_list:
            for no_weight_person in no_weight_term['predict_data']:
                if id == no_weight_person['apply_Id']:
                    no_weight_term['predict_data'].remove(no_weight_person)
                    break

    return no_weight_not_over_term_list




# 每天运行这个函数去拉减脂营在营的数据进行预测和统计
def every_day_run_predict():
    # not_over_term_list = [{'termID': 261, 'term_num': 114, 'camp_start_time': '2018-07-23 00:00:00', 'leave_time': '2018-08-18 16:19:11', 'predict_day': 26, },{},,,]
    not_over_term_list = get_not_over_TermID()



    #存开局无体重的人
    no_weight_not_over_term_list = get_not_over_TermID()
    no_weight_not_over_term_list = get_day_all_applyID(no_weight_not_over_term_list)

    not_over_term_list = get_day_weight(not_over_term_list)

    #从 no_weight_not_over_term_list  删除  not_over_term_list 中有体重的人
    no_weight_not_over_term_list = remove_weight_person(no_weight_not_over_term_list, not_over_term_list)

    day_check_list = get_day_check()

    day_speak_list = get_day_speak()

    #[{'termID': 261, 'term_num': 114, 'predict_day': 22 , 'predict_data':[{'apply_Id':_ , 'term_num':_ ,}...]}, ,,]
    not_over_term_list = get_all_data(not_over_term_list,day_check_list , day_speak_list)
    no_weight_not_over_term_list = get_all_data(no_weight_not_over_term_list, day_check_list , day_speak_list)

    not_over_term_list = add_null_weight(not_over_term_list)
    # print(not_over_term_list[0]['predict_data'][0])



    # 把以前走的人从 not_over_term_list 移 到already_leave_list , 最后一天有行动的留在 not_over_term_list 进行预测
    already_leave_list, not_over_term_list = cut_already_leave_person_before_predict(not_over_term_list)
    no_weight_already_leave_list, no_weight_not_over_term_list = no_weight_cut_already_leave_person_before_predict(no_weight_not_over_term_list)


    # predict0_list =[{'term_num':_ , 'name':_}, ,,]
    print('开始预测有体重')
    # 1000个逻辑回归预测
    predict0_list = predict_leave(not_over_term_list)
    make_xls_file_with_all_message(predict0_list, file_type = 'predict')
    make_xls_file_with_all_message(already_leave_list, file_type = 'already_leave')
    print('有体重 预测完毕')


    print('开始预测无体重')
    no_weight_predict0_list = no_weight_predict_leave(no_weight_not_over_term_list)
    no_weight_predict0_list.extend(no_weight_already_leave_list)
    no_weight_make_xls_file_with_all_message(no_weight_predict0_list)
    print('无体重 预测完毕')




if __name__ == '__main__':
    every_day_run_predict()






