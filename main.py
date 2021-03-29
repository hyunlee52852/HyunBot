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

#SQL 구문 모음
_readtest = 'SELECT * FROM test'
_select_sorted_data = 'SELECT date, period, description FROM test ORDER BY date ASC, period ASC;'

#------------
cursor.execute(_select_sorted_data)
result = cursor.fetchall()

for dic in result:
    for key, value in dic.items():

        if isinstance(value, datetime.date):
            value = value.strftime("%m/%d")
        print(key + " : " + str(value))

