from PIL import Image, ImageDraw, ImageFont
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

#SQL 구문 모음
_readtest = "SELECT * FROM %s;"
_select_sorted_data = "SELECT date, period, description FROM %s ORDER BY date ASC, period ASC;"
_adddata = 'INSERT INTO %s'
#------------

#SQL에 쓰이는 변수 모음
__table_name = 'test'
__select = 'SELECT'

#------------

#폰트 모음
___d2coding_font = ImageFont.truetype("fonts\D2coding\D2CodingLigature\D2coding.ttf", 50)
___d2coding_font_bold = ImageFont.truetype("fonts\D2coding\D2CodingLigature\D2codingBold.ttf", 100)
#-----------

img = Image.new('RGB', (2000, 3000), color = 'white') # create img

dt = ImageDraw.Draw(img) # make text draw cursor

curx = 50
cury = 100
# cursor position init

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
        printtext("날짜 : " + date, ___d2coding_font_bold, (0, 0, 0), 50)
        printtext("교시 : " + period, ___d2coding_font_bold, (0, 0, 0), 20)
        printtext(desc, ___d2coding_font, (0, 0, 0), 20)
        print(dt.textsize(desc, font = ___d2coding_font))

def printtext(str, fnt, fontcolor, space): # 텍스트를 출력하는 함수 (출력할 문자열, 폰트, 폰트의 색 (R,G,B), 다음줄과의 간격)
    global curx
    global cury
    dt.text((curx, cury), str, font = fnt, fill = fontcolor)
    nextx, nexty = dt.textsize(str, font = fnt)
    print(nextx)
    print(nexty)
    cury += nexty + space
    

showdata()
#printtext( "날짜 : 03/30" , ___d2coding_font_bold, (0, 0, 0))
#printtext( "If I Write English, Will it change?" , ___d2coding_font_bold, (0, 0, 0))
img.show()