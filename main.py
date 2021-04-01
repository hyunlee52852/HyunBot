from PIL import Image, ImageDraw, ImageFont
import numpy as np
import pymysql
import datetime
from datetime import datetime, timedelta, date
import textwrap
import math

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
_select_sorted_data = "SELECT date, period, description, duration FROM %s ORDER BY date ASC, period ASC;"
_adddata = 'INSERT INTO %s'
#------------

#SQL에 쓰이는 변수 모음
__table_name = 'test'
__select = 'SELECT'

#------------

#학생 정보 딕셔너리 선언
stddic = {}

#시간표 변수들

#교과과목
_LIT = '문학'
_ENG = '영어'
_MAT = '수학'
_PE = '체육'
_MUS = '음악'
_SPE = '창체'

#전공과목
_MTA = '수A'
_MTB = '수B'
_JAP = '일어'
_IFA = '정A'
_IFB = '정B'
_SYS = '시프'
_DTA = '료A'
_DTB = '료B'
_SPC = '창특'
_IND = '공업'
_SCF = '창진' 

_TIMETABLE = [
    [_MTA, _PE, _JAP, _IFB, _IFB, _IND, None],
    [_LIT, _ENG, _MAT, _SYS, _SYS, _SPE, _SPE],
    [_DTA, _JAP, _MTB, _IFA, _ENG, _LIT, _MAT],
    [_SYS, _SYS, _MTA, _SPC, _JAP, _MUS, _DTB],
    [_MAT, _LIT, _IND, _SYS, _SYS, _JAP, _SCF]
]

#글로벌 위치 변수 선언.
globalx = 0
globaly = 0

#폰트 모음
___d2coding_font = "fonts\\D2coding\\D2CodingLigature\\D2coding.ttf"
___d2coding_font_bold = "fonts\\D2coding\\D2CodingLigature\\D2codingBold.ttf"
___noto_sans_bold = "fonts\\Noto_Sans_KR\\NotoSansKR-Bold.otf"
___noto_sans = "fonts\\Noto_Sans_KR\\NotoSansKR-Medium.otf"
#-----------

#텍스트 관련 함수 모음
def getfont(fontpath, fontsize):
    return ImageFont.truetype(fontpath, fontsize)

def printtext(tarstr, fnt, curx, cury, fontcolor): # 텍스트를 출력하는 함수
    dt.text(getmiddletext(tarstr, fnt, curx, cury), tarstr, font = fnt, fill = fontcolor)
    #dt.text(getmiddletext(lenstr, satft, nextx, 180), lenstr, font = satft, fill = (0, 0, 0))


def getmiddletext(str, fnt, fx, fy):
    sizex, sizey = dt.textsize(str, font = fnt)
    return (fx - (sizex / 2), fy - (sizey / 2))

def printmultiplelines(tarstr, len , curx, cury, fnt, fontcolor):
    lines = textwrap.wrap(tarstr, width=len)
    print(lines)
    for line in lines:
        w, h = fnt.getsize(line)
        dt.text((curx, cury), line, fill = fontcolor, font = fnt)
        cury += h
    return curx, cury
#------------

#도형 관련 함수 모음
def linedashed(x0, y0, x1, y1, dashlen, ratio, wdt): 
    dx=x1-x0 # delta x
    dy=y1-y0 # delta y
    # check whether we can avoid sqrt
    if dy==0: len=dx
    elif dx==0: len=dy
    else: len=math.sqrt(dx*dx+dy*dy) # length of line
    xa=dx/len # x add for 1px line length
    ya=dy/len # y add for 1px line length
    step=dashlen*ratio # step to the next dash
    a0=0
    while a0<len:
        a1=a0+dashlen
        if a1>len: a1=len
        dt.line((x0+xa*a0, y0+ya*a0, x0+xa*a1, y0+ya*a1), fill = (0,0,0), width= wdt)
        a0+=step 

def dataquery():
    cursor.execute(_select_sorted_data % (__table_name))
    result = cursor.fetchall()
    
    for dic in result:
        date = None
        period = None
        desc = None
        dur = None
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
            elif key == 'duration':
                dur = value

        #print(date + " " + period + " " + desc)
        stddic.setdefault(date,[]).append((period, desc, dur))

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
    sat_left = sat_day - tomorrow

    #날짜를 문자열로 변환
    monthstr = tomorrow.strftime('%b').upper()
    daystr = tomorrow.strftime('%d')
    weekdaystr = tomorrow.strftime('%a').upper()
    satleftstr = "D-" + str(sat_left.days)

    #글자 출력
    printtext(monthstr, monthft, 80, 110, (255, 255, 255))
    printtext(weekdaystr, monthft, 80, 230, (255, 255, 255))
    printtext(daystr, dayft, 320, 150, (255, 255, 255))
    printtext(satleftstr, satft, 420, 18, (0, 0, 0))

    # 일정 표 출력
    curx = 500
    cury = 270

    for i in range(-30, 30):
        nextday = tomorrow + timedelta(days = i)
        nextdaystr = nextday.strftime('%d')
        nextquerystr = str(nextday.strftime("%Y-%m-%d"))
        nextx = curx + (i * 50) + 2
        textcol = (0, 0, 0)
        if(i <= 0):
            nextx = curx
        if(i > 0):
            if(nextday.weekday() == 5 or nextday.weekday() == 6):
                textcol = (255, 255, 255)
                dt.rectangle(((nextx - 25, 250), (nextx + 25, 300)), fill=(0, 0, 0)) 
            printtext(nextdaystr, satft, nextx, cury, textcol)
        if nextquerystr in stddic:
            lenstr = str(len(stddic[nextquerystr]))
            for j in stddic[nextquerystr]:
                dur = int(j[2])
                desc = str(j[1])
                if (dur > 0):
                    dt.rectangle(((nextx - 2, 140), (nextx + (dur * 50) + 2, 150)), fill = 'black')
                    printtext(desc, satft, (nextx + ((dur * 50)) / 2), 110, (0, 0, 0))
            if(i > 0):
                printtext(lenstr, satft, nextx, 180, (0, 0, 0))


def settomorrowdata():
    globalx = 50
    globaly = 450
    tomorrow = date.today() + timedelta(days=1)
    tomorrowstr = str(tomorrow.strftime("%Y-%m-%d"))
    kyoshifont = getfont(___noto_sans, 40)
    textfont = getfont(___noto_sans, 30)
    periodfont = getfont(___noto_sans, 80)
    periodnamefont = getfont(___noto_sans, 60)
    kyoshi = '교시'
    printtext(kyoshi, kyoshifont, 100, 380, (0, 0, 0))
    linedashed(1000, 400, 1000, 1500, 20, 2, 5)
    for curperiod in range(1, 8):
        printtext(str(curperiod), periodfont, 100, globaly, (0, 0, 0))
        cursub = str(_TIMETABLE[tomorrow.weekday()][curperiod - 1])
        printtext(cursub, periodnamefont, 200, globaly, (0, 0, 0))
        globaly += 100

        
    

def imageinit(): #이미지의 크기를 미리 결정
    imagex = 2000
    imagey = 1300
    #for key, value in stddic.items():
        #print(key)
        #print(value)
    return imagex, imagey

    


# cursor position init

dataquery()
imagex, imagey = imageinit()
img = Image.new('RGB', (imagex, imagey), color = 'white') # create img
dt = ImageDraw.Draw(img) # make text draw cursor
setupperpart()
settomorrowdata()

img.show()
img.save('output.png')