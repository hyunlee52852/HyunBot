from PIL import Image
import numpy as np
import pymysql

with open('password.txt') as f:
    logindata = f.read().splitlines() 
id = logindata[0]
pw = logindata[1]


_db = pymysql.connect(
    user=id, 
    passwd=pw, 
    host='34.82.97.92', 
    db='schedule', 
    charset='utf8'
)

cursor = _db.cursor(pymysql.cursors.DictCursor)

_readtest = 'SELECT * FROM test'
cursor.execute(_readtest)
result = cursor.fetchall()
print(result)

