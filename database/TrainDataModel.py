#首先运行，提数据
import csv
from peewee import *
from database.baseModel import EshopBaseModel, camp_db


class RawModel(EshopBaseModel):
    rawID = IntegerField()


def getLastTermID():
    if camp_db.is_closed():
        camp_db.connect()

    record = RawModel.raw('''
SELECT
  term.TERM_ID as termID
FROM eshop.TB_TERM term
WHERE date_add(term.CAMP_START_TIME, INTERVAL term.DAYS DAY) < date_add(now(), INTERVAL -5 DAY)
AND term.TYPE = 1
ORDER BY term.TERM_ID DESC
LIMIT 1
            ''')

    termID = 0
    for r in record:
        termID = r.termID

    if not camp_db.is_closed():
        camp_db.close()

    return termID

#这段代码抽取所有减脂营 有开局体重的applyID
def get_week_weight(termID):
    trainDatas = []
    if camp_db.is_closed():
        camp_db.connect()

    record = RawModel.raw('''
    select
  body.APPLY_ID apply_Id,
  apply.AGE age,
  case apply.GENDER
       when 'f'
       then 1
       ELSE 0 end   gender,

   Max(CASE body.WEEK
        WHEN 0
          THEN body.HEIGHT
        ELSE 0 END) 'week0Height',
    # weight
    Max(CASE body.WEEK
        WHEN 0
          THEN body.WEIGHT
        ELSE 0 END) 'week0Weight',
    Max(CASE body.WEEK
        WHEN 1
          THEN body.WEIGHT
        ELSE 0 END) 'week1Weight',
    Max(CASE body.WEEK
        WHEN 2
          THEN body.WEIGHT
        ELSE 0 END) 'week2Weight',
    Max(CASE body.WEEK
        WHEN 3
          THEN body.WEIGHT
        ELSE 0 END) 'week3Weight',
    Max(CASE body.WEEK
        WHEN 4
          THEN body.WEIGHT
        ELSE 0 END) 'week4Weight'
from TB_BODY_DATA body
  left join  TB_APPLY_RECORD apply on apply.APPLY_ID = body.APPLY_ID
    LEFT JOIN TB_TERM term ON term.TERM_ID = apply.TERM_ID
    LEFT JOIN TB_ORDER tborder ON apply.PACKAGE_ORDER_ID = tborder.ORDER_ID
  WHERE tborder.OUTER_ORIGIN != 'exchange_white_list_test'
    AND term.TYPE = 1
    and term.TERM_ID < %s
    and apply.GENDER is not null
    and apply.age is not null
group by apply_Id
having
    week0Height > 10
    and week0Weight > 10
    and week0Weight < 120

    and week1Weight < 130

    and week2Weight < 130

    and week3Weight < 130

    and week4Weight < 130

''', termID)

    for r in record:
        r_dic ={}
        r_dic['apply_Id'] = r.apply_Id
        r_dic['age'] = r.age
        r_dic['gender'] = r.gender
        r_dic['week0Height']= r.week0Height
        r_dic['week0Weight']= r.week0Weight
        r_dic['week1Weight']= r.week1Weight
        r_dic['week2Weight']= r.week2Weight
        r_dic['week3Weight'] = r.week3Weight
        r_dic['week4Weight'] = r.week4Weight
        trainDatas.append(r_dic)

    if not camp_db.is_closed():
        camp_db.close()

    return trainDatas


#这段代码抽取所有减脂营 结营的applyID
def get_all_apply_id(termID):
    trainDatas = []
    if camp_db.is_closed():
        camp_db.connect()

    record = RawModel.raw('''
select
  apply.APPLY_ID apply_Id
    from TB_APPLY_RECORD apply
    LEFT JOIN TB_TERM term ON term.TERM_ID = apply.TERM_ID
    LEFT JOIN TB_ORDER tborder ON apply.PACKAGE_ORDER_ID = tborder.ORDER_ID
  WHERE tborder.OUTER_ORIGIN != 'exchange_white_list_test'
    AND term.TYPE = 1
    and term.TERM_ID < %s
''', termID)

    for r in record:
        r_dic ={}
        r_dic['apply_Id'] = r.apply_Id
        trainDatas.append(r_dic)

    if not camp_db.is_closed():
        camp_db.close()

    return trainDatas


def get_day_check():
    trainDatas = []

    if camp_db.is_closed():
        camp_db.connect()

    record = RawModel.raw('''select
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
  order by checkin.APPLY_ID, checkin.CHECK_IN_DATE
)sub
group by sub.APPLY_ID''')

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


        trainDatas.append(r_dic)

    if not camp_db.is_closed():
        camp_db.close()

    return trainDatas


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
      AND cr.createTime >= term.CAMP_START_TIME
      AND cr.createTime < date_add(term.CAMP_START_TIME, INTERVAL term.DAYS DAY)
      AND term.TYPE = 1
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

        trainDatas.append(r_dic)

    return trainDatas


def get_all_data(wl , cl ,sl ):

    for person in wl:
        for i in range(1,29):
            person['check%d'%i] = 0
            person['breakfast%d'%i] =0
            person['lunch%d'%i] = 0
            person['dinner%d'%i] = 0
            person['trainning%d'%i] = 0
            person['speak%d'%i] = 0
            person['greed%d'%i] = 0
            person['pressure%d'%i] = 0
            person['menstrual%d'%i] = 0

    for person in wl:
        apply_Id = person['apply_Id']

        for person2 in cl:
            if person2['apply_Id'] == apply_Id:
                for i in range(1,29):
                    person['check%d' %i] = person2['check%d' %i]
                    person['breakfast%d' %i] = person2['breakfast%d'%i]
                    person['lunch%d' % i] = person2['lunch%d'%i]
                    person['dinner%d' % i] = person2['dinner%d'%i]
                    person['trainning%d' % i] = person2['trainning%d'%i]
                break

        for person3 in sl:
            if person3['apply_Id'] == apply_Id:
                for i in range(1, 29):
                    person['speak%d'%i] =  person3['speak%d'%i]
                    person['greed%d'%i] =  person3['greed%d'%i]
                    person['pressure%d'%i] =  person3['pressure%d'%i]
                    person['menstrual%d'%i] =  person3['menstrual%d'%i]
                break



    #  /data/weight_dataset
    with open("./data/weight_dataset/trainData.csv", "w+", encoding='utf8') as csvfile:
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

        for i in wl:
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

    return wl

def get_all_no_weight_data(al , cl ,sl ):

    for person in al:
        for i in range(1,29):
            person['check%d'%i] = 0
            person['breakfast%d'%i] =0
            person['lunch%d'%i] = 0
            person['dinner%d'%i] = 0
            person['trainning%d'%i] = 0
            person['speak%d'%i] = 0
            person['greed%d'%i] = 0
            person['pressure%d'%i] = 0
            person['menstrual%d'%i] = 0

    for person in al:
        apply_Id = person['apply_Id']

        for person2 in cl:
            if person2['apply_Id'] == apply_Id:
                for i in range(1,29):
                    person['check%d' %i] = person2['check%d' %i]
                    person['breakfast%d' %i] = person2['breakfast%d'%i]
                    person['lunch%d' % i] = person2['lunch%d'%i]
                    person['dinner%d' % i] = person2['dinner%d'%i]
                    person['trainning%d' % i] = person2['trainning%d'%i]
                break

        for person3 in sl:
            if person3['apply_Id'] == apply_Id:
                for i in range(1, 29):
                    person['speak%d'%i] =  person3['speak%d'%i]
                    person['greed%d'%i] =  person3['greed%d'%i]
                    person['pressure%d'%i] =  person3['pressure%d'%i]
                    person['menstrual%d'%i] =  person3['menstrual%d'%i]
                break


    # /data/no_weight_dataset
    with open("./data/no_weight_dataset/trainData.csv", "w+", encoding='utf8') as csvfile:
        writer = csv.writer(csvfile)
        # 先写入columns_name

        writer.writerow([
            'apply_Id',

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

        for i in al:
            writer.writerow([
                i['apply_Id'],
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

    return al

# 提取有体重,无体重的数据集
def sql_get_data():
    lastID = getLastTermID()
    weight_list = get_week_weight(lastID)
    print(len(weight_list))

    check_list = get_day_check()
    print(len(check_list))

    speak_list = get_day_speak()
    print(len(speak_list))

    get_all_data(wl=weight_list, cl=check_list, sl=speak_list)
    print('开局有体重提取完毕')


    #提取开局无体重的 applyID
    apply_list = get_all_apply_id(lastID)
    get_all_no_weight_data(al=apply_list, cl=check_list, sl=speak_list)
    print('开局无体重提取完毕')



