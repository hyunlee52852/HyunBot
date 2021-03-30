from PIL import Image
import numpy as np
import pymysql
import datetime

#password.txt 파일에서 id와 pw를 가져온다
with open('password.txt') as f:
    logindata = f.read().splitlines() 
id = logindata[0]
pw = logindata[1]

#내 서버에 있는 DB에 연결
_db = pymysql.connect(
    user=id, 
    passwd=pw, 
    host='34.82.97.92', 
    db='schedule', 
    charset='utf8'
)
#커서 지정

cursor = _db.cursor(pymysql.cursors.DictCursor)
insertcursor = _db.cursor(pymysql.cursors.Cursor)

#SQL에 쓰이는 변수 모음
__table_name = 'test'
__select = 'SELECT'

#------------

#SQL 구문 모음
_readtest = "SELECT * FROM %s;"
_select_sorted_data = "SELECT date, period, description FROM %s ORDER BY date ASC, period ASC;"
_adddata = 'INSERT INTO %s'
#------------


def showdata():
    cursor.execute(_select_sorted_data % (__table_name))
    result = cursor.fetchall()

    for dic in result:
        date = None
        period = None
        desc = None
        for key, value in dic.items():
            if isinstance(value, datetime.date):
                value = value.strftime("%m/%d")
            value = str(value)
            if key == 'date':
                date = value
            elif key == 'period':
                period = value
            elif key == 'description':
                desc = value
        print(date + " " + period + " " + desc)


showdata()