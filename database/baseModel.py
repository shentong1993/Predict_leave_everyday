import os
from playhouse.migrate import *

camp_db = MySQLDatabase(host='x.x.x.x', port=x, user='x', database='x',passwd='x',charset='utf8')


class EshopBaseModel(Model):
    class Meta:
        database = camp_db


