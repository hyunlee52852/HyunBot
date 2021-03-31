from PIL import Image, ImageDraw, ImageFont
import numpy as np
import pymysql
import datetime
from datetime import datetime, timedelta, date
import textwrap

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

#학생들 정보 딕셔너리 선언
stddic = {}


#폰트 모음
___d2coding_font = "fonts\\D2coding\\D2CodingLigature\\D2coding.ttf"
___d2coding_font_bold = "fonts\\D2coding\\D2CodingLigature\\D2codingBold.ttf"
___noto_sans_bold = "fonts\\Noto_Sans_KR\\NotoSansKR-Bold.otf"
___noto_sans = "fonts\\Noto_Sans_KR\\NotoSansKR-Medium.otf"
#-----------

#텍스트 관련 함수 모음
def getfont(fontpath, fontsize):
    return ImageFont.truetype(fontpath, fontsize)

def printtext(str, fnt, fontcolor): # 텍스트를 출력하는 함수 (자동 줄바꿈) (출력할 문자열, 폰트, 폰트의 색 (R,G,B), 다음줄과의 간격)
    global curx
    global cury
    dt.text((curx, cury), str, font = fnt, fill = fontcolor)
    nextx, nexty = dt.textsize(str, font = fnt)
    print(nextx)
    print(nexty)

def getmiddletext(str, fnt, fx, fy):
    sizex, sizey = dt.textsize(str, font = fnt)
    return (fx - (sizex / 2), fy - (sizey / 2))
#------------


def dataquery():
    cursor.execute(_select_sorted_data % (__table_name))
    result = cursor.fetchall()
    
    for dic in result:
        date = None
        period = None
        desc = None
        for key, value in dic.items():
            if isinstance(value, type(datetime.date)):
                value = value.strftime("%m/%d")
            value = str(value)
            if key == 'date':
                date = value
            elif key == 'period':
                period = value
            elif key == 'description':
                desc = value
        print(date + " " + period + " " + desc)
        stddic.setdefault(date,[]).append((period, desc))
        

def setupperpart():
    upper_part = Image.open('Image Files\\Upper bar.png' , 'r')

    #상단 이미지 png로 불러오기
    upper_part = Image.composite(upper_part, Image.new('RGB', upper_part.size, 'white'), upper_part)
    img.paste(upper_part, (0, 0))
    # 월, 일, 요일 출력
    monthft = getfont(___d2coding_font, 100)
    dayft = getfont(___d2coding_font, 300)
    satft = getfont(___noto_sans, 32)

    #날짜 정하기
    today = date.today()
    tomorrow = today + timedelta(days = 1)
    sat_day = date(2022, 11, 17)
    sat_left = sat_day - today

    #날짜를 문자열로 변환
    monthstr = tomorrow.strftime('%b').upper()
    daystr = tomorrow.strftime('%d')
    weekdaystr = tomorrow.strftime('%a').upper()
    satleftstr = "D-" + str(sat_left.days)

    #글자 출력
    dt.text(getmiddletext(monthstr, monthft, 80, 110), monthstr, font = monthft, fill = (255, 255, 255))
    dt.text(getmiddletext(weekdaystr, monthft, 80, 230), weekdaystr, font = monthft, fill = (255, 255, 255))
    dt.text(getmiddletext(daystr, dayft, 320, 150), daystr, font = dayft, fill = (255, 255, 255))
    dt.text(getmiddletext(satleftstr, satft, 420, 18), satleftstr, font = satft, fill = (0, 0, 0))

def imageinit(): #이미지의 크기를 미리 결정
    imagex = 2000
    imagey = 300
    for key, value in stddic.items():
        print(value)
    return imagex, imagey

    

curx = 50
cury = 300
# cursor position init

dataquery()
imagex, imagey = imageinit()
img = Image.new('RGB', (imagex, imagey), color = 'white') # create img
dt = ImageDraw.Draw(img) # make text draw cursor
setupperpart()

img.show()
#img.save('output.png')