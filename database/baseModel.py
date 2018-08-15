import os
from playhouse.migrate import *

camp_db = MySQLDatabase(host='172.31.100.148', port=3306, user='onlineuser', database='eshop',passwd='ndSMwY085_8',charset='utf8')


class EshopBaseModel(Model):
    class Meta:
        database = camp_db


