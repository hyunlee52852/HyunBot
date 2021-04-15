from PIL import Image, ImageDraw, ImageFont
import numpy as np
import pymysql
import datetime
from datetime import datetime, timedelta, date
import textwrap
import math
import requests
from bs4 import BeautifulSoup
import re
from flask import Flask, render_template, jsonify, request
import sys

#SQL 구문 모음
_readtest = "SELECT * FROM %s;"
_select_sorted_data = "SELECT date, period, description, duration, changeperiod FROM %s ORDER BY date ASC, period ASC;"
_adddata = 'INSERT INTO %s'
#------------

#SQL에 쓰이는 변수 모음
__table_name = 'schedule'
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
_NON = 'N/A'
_TIMETABLE = [
    [_MTA, _PE, _JAP, _IFB, _IFB, _IND, _NON],
    [_LIT, _ENG, _MAT, _SYS, _SYS, _SPE, _SPE],
    [_DTA, _JAP, _MTB, _IFA, _ENG, _LIT, _MAT],
    [_SYS, _SYS, _MTA, _SPC, _JAP, _MUS, _DTB],
    [_MAT, _LIT, _IND, _SYS, _SYS, _ENG, _SCF],
    [_NON, _NON, _NON, _NON, _NON, _NON, _NON],
    [_NON, _NON, _NON, _NON, _NON, _NON, _NON]
]
#시간 변수 모음


#폰트 모음
___d2coding_font = "fonts/D2coding/D2CodingLigature/D2coding.ttf"
___d2coding_font_bold = "fonts/D2coding/D2CodingLigature/D2codingBold.ttf"
___noto_sans_bold = "fonts/Noto_Sans_KR/NotoSansKR-Bold.otf"
___noto_sans = "fonts/Noto_Sans_KR/NotoSansKR-Medium.otf"
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
    #print(lines)
    for line in lines:
        w, h = fnt.getsize(line)
        dt.text((curx, cury), line, fill = fontcolor, font = fnt)
        cury += h
    return cury
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

#급식 데이터 받아오는 함수 credit : https://mandu-mandu.tistory.com/21
def get_html(url):
   _html = ""
   resp = requests.get(url)
   if resp.status_code == 200:
      _html = resp.text
   return _html
 
 
def get_diet(code, ymd, weekday):
    schMmealScCode = code #int
    schYmd = ymd #str
    
    num = weekday + 1 #int 0월1화2수3목4금5토6일
    URL = (
            "http://stu.sen.go.kr/sts_sci_md01_001.do?"
            "schulCode=B100000405&schulCrseScCode=4&schulKndScCode=04"
            "&schMmealScCode=%d&schYmd=%s" % (schMmealScCode, schYmd)
        )
    html = get_html(URL)
    soup = BeautifulSoup(html, 'html.parser')
    element = soup.find_all("tr")
    element = element[2].find_all('td')
    try:
        element = element[num] #num
        element = str(element)
        element = element.replace('[', '')
        element = element.replace(']', '')
        element = element.replace('&amp;', '&')
        element = element.replace('<br/>', '\n')
        element = element.replace('<td class="textC last">', '')
        element = element.replace('<td class="textC">', '')
        element = element.replace('</td>', '')
        element = element.replace('(h)', '')
        element = element.replace('.', '')
        element = re.sub(r"\d", "", element)
    except:
        element = " "
    
    return element

def dataquery():
    stddic.clear()
    cursor.execute(_select_sorted_data % (__table_name))
    result = cursor.fetchall()
    
    for dic in result:
        date = None
        period = None
        desc = None
        dur = None
        changeperiod = None
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
            elif key == 'changeperiod':
                changeperiod = value

        #print(date + " " + period + " " + desc)
        stddic.setdefault(date,[]).append((period, desc, dur, changeperiod))
def setupperpart():
    upper_part = Image.open('Image_Files/Upper bar.png' , 'r')

    #상단 이미지 png로 불러오기
    upper_part = Image.composite(upper_part, Image.new('RGB', upper_part.size, 'white'), upper_part)

    img.paste(upper_part, (0, 0))
    # 월, 일, 요일 출력
    monthft = getfont(___d2coding_font, 100)
    dayft = getfont(___d2coding_font, 300)
    satft = getfont(___noto_sans, 32)

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
                    if(i <= 0):
                        dur = ((nextday + timedelta(days=dur)) - tomorrow).days
                    dt.rectangle(((nextx - 2, 140), (nextx + (dur * 50) + 2, 150)), fill = 'black')
                    #printtext(desc, satft, (nextx + ((dur * 50)) / 2), 110, (0, 0, 0))
                    printmultiplelines(desc, 40, (nextx ), 90,satft, (0, 0, 0))
            if(i > 0):
                printtext(lenstr, satft, nextx, 180, (0, 0, 0))


def settomorrowdata():
    curx = 50
    cury = 300
    tomorrowstr = str(tomorrow.strftime("%Y-%m-%d"))
    kyoshifont = getfont(___noto_sans_bold, 40)
    textfont = getfont(___noto_sans, 40)
    periodfont = getfont(___noto_sans, 80)
    periodnamefont = getfont(___noto_sans, 60)
    kyoshi = '교시'
    temptomorrow = tomorrow
    if(tomorrow.weekday() > 4):
        cury = 300
        printmultiplelines("주말입니다! 다음 주 월요일 일정을 확인하세요.", 30, 50, cury, periodfont, (0, 0, 0))
        temptomorrow += timedelta(days = 7 - tomorrow.weekday())
        cury += 130
        linedashed(0, cury, 2000, cury, 40, 1.5, 10)
        cury += 50
        tomorrowstr = str(temptomorrow.strftime("%Y-%m-%d"))
    tempy = cury
    gupsiky = printfooddata(cury)
    cury = printmultiplelines(kyoshi, 40, 50, cury + 10, kyoshifont, (0, 0, 0))
    
    perioddata = [[] for i in range(10)]
    changeperioddata = [[] for i in range(10)]

    if(tomorrowstr in stddic):
        for dat in stddic[tomorrowstr]:
            perioddata[int(dat[0])].append(dat[1])
            changeperioddata[int(dat[0])] = dat[3]
            print(dat[3])


    #print(perioddata)
    for curperiod in range(0, 8):
        printmultiplelines(str(curperiod), 40, 50, cury, periodfont, (0, 0, 0))
        cursub = str(_TIMETABLE[temptomorrow.weekday()][curperiod - 1])

        if(curperiod == 0):
            cursub = 'HR'
        if changeperioddata[curperiod]:
            cursub = str(changeperioddata[curperiod])
        
        printmultiplelines(cursub, 40, 100, cury + 15, periodnamefont, (0, 0, 0))
        beforey = cury
        for dat in perioddata[curperiod]:
            cury = printmultiplelines(dat, 20, 230, cury + 30, textfont, (0, 0, 0))
            #print(cury)
        if(cury - beforey <= 70):
            cury = beforey + 100
    cury += 20

    cury = max(cury, gupsiky)
    linedashed(1000, tempy + 10, 1000, cury, 20, 2, 5)
    linedashed(0, cury, 2000, cury, 40, 1, 5)
    return cury

def splitfooddata(originlist):
    outputlist = []
    for i in range(0, int(len(originlist) / 2)):
        outputlist.append(str(originlist[i * 2] + ", " + originlist[i * 2 + 1]))
    
    return outputlist


def printfooddata(cury):
    gupsikfont = getfont(___noto_sans, 50)
    biggupsikfont = getfont(___noto_sans, 80)
    textfont = getfont(___noto_sans, 30)
    temptomorrow = tomorrow
    print(tomorrow.weekday())
    #주말인 경우 다음 주 월요일 체크
    if temptomorrow.weekday() > 4 :
        temptomorrow += timedelta(days = 7 - tomorrow.weekday())
    jungsik = get_diet(2, temptomorrow.strftime("%Y.%m.%d"), temptomorrow.weekday())
    jungsik = jungsik.split("\n")

    sucksik = get_diet(3, temptomorrow.strftime("%Y.%m.%d"), temptomorrow.weekday())
    sucksik = sucksik.split("\n")

    cury = printmultiplelines('중식', 40, 1030, cury, biggupsikfont, (0, 0, 0))
    jungsiklist = splitfooddata(jungsik)
    print(jungsiklist)
    for line in jungsiklist:
        w, h = gupsikfont.getsize(line)
        cury = printmultiplelines(line, 20, 1030, cury, gupsikfont, (0, 0, 0))
    cury += 20
    linedashed(1010, cury, 19900, cury, 10, 2, 2)
    cury = printmultiplelines('석식', 40, 1030, cury, biggupsikfont, (0, 0, 0))
    sucksiklist = splitfooddata(sucksik)
    print(sucksiklist)
    for line in sucksiklist:
        w, h = gupsikfont.getsize(line)
        cury = printmultiplelines(line, 20, 1030, cury, gupsikfont, (0, 0, 0))
    cury += 20
    return cury
        
    
def setbottompart(cury):
    lower_part = Image.open('Image_Files/Down_bar.png', 'r')
    lower_part = Image.composite(lower_part, Image.new('RGB', lower_part.size, 'white'), lower_part)
    lower_part_flipped = Image.open('Image_Files/Down_bar_Flipped.png', 'r')
    lower_part_flipped = Image.composite(lower_part_flipped, Image.new('RGB', lower_part_flipped.size, 'white'), lower_part_flipped)
    
    datefont = getfont(___d2coding_font, 150)
    datefontsmall = getfont(___d2coding_font, 50)
    textfont = getfont(___noto_sans, 40)
    periodfont = getfont(___noto_sans, 80)
    periodnamefont = getfont(___noto_sans, 60)

    for key, value in stddic.items():

        curdate = datetime.date(datetime.strptime(key, '%Y-%m-%d'))

        monthstr = curdate.strftime('%b').upper()
        daystr = curdate.strftime('%d')
        weekday = curdate.weekday()
        weekdaystr = curdate.strftime('%a').upper()

        perioddata = [[] for i in range(10)]
        dur = -1
        durdesc = None
        for data in value:
            tempdur = int(data[2])
            if int(tempdur) > 0:
                dur = ((curdate + timedelta(days=tempdur)) - tomorrow).days
                durdesc = str(data[1])

        if(curdate <= tomorrow and dur < 0):
            continue
        
        print(dur)
        durdate = tomorrow + timedelta(days=dur)

        cury += 20
        img.paste(lower_part, (0, cury))
        if(dur >= 0):
            img.paste(lower_part_flipped, (200, cury))
            durmonthstr = durdate.strftime('%b').upper()
            durweekdaystr = durdate.strftime('%a').upper()
            durdaystr = durdate.strftime('%d')
            printmultiplelines("~", 20, 165, cury + 50, periodfont, (0, 0, 0))
            printmultiplelines(durmonthstr + " " + durweekdaystr, 20, 220, cury, datefontsmall, (255, 255, 255))
            cury = printmultiplelines(monthstr + " " + weekdaystr, 20, 5, cury, datefontsmall, (255, 255, 255))
            printmultiplelines(durdesc, 30, 400, cury + 20, periodnamefont, (0, 0, 0))
            printmultiplelines(daystr, 20, 0, cury, datefont, (0, 0, 0))
            cury = printmultiplelines(durdaystr, 20, 220, cury, datefont, (0, 0, 0))

        if(curdate <= tomorrow):
            continue

        tempy = cury

        if(dur == -1):
            cury = printmultiplelines(monthstr + " " + weekdaystr, 20, 5, cury, datefontsmall, (255, 255, 255))
            tempy = printmultiplelines(daystr, 20, 0, cury, datefont, (0, 0, 0))

        changeperioddata = [[] for i in range(10)]

        for dat in stddic[key]:
            changeperioddata[int(dat[0])] = dat[3]

        for data in value:
            curperiod = int(data[0])
            if int(data[2]) > 0:
                continue
            if curperiod > 7:
                curperiod = 0
            perioddata[curperiod].append(data[1])

        for period in range(0, 8):
            if not perioddata[period]:
                continue
            cursub = str(_TIMETABLE[weekday][period - 1])
            if period == 0:
                cursub = "HR"
            
            if changeperioddata[period]:
                cursub = changeperioddata[period]
            
            printmultiplelines(str(period), 30, 200, cury, periodfont, (0, 0, 0))
            printmultiplelines(cursub, 30, 250, cury + 15, periodnamefont, (0, 0, 0))
            for data in perioddata[period]:
                cury = printmultiplelines(data, 45, 400, cury + 25, textfont, (0, 0, 0))
        cury = max(tempy, cury)
        cury += 20
    return cury


def imageinit(): #이미지의 크기를 미리 결정
    imagex = 2000
    imagey = 10000
    #for key, value in stddic.items():
        #print(key)
        #print(value)
    return imagex, imagey

def createimage():
    global imagex
    global imagey
    global img
    global dt
    global globaly
    global globalx
    global cursor
    global insertcursor
    global today
    global tomorrow
    global sat_day

    today = date.today()
    tomorrow = today + timedelta(days = 1)
    sat_day = date(2022, 11, 17)
    imagex, imagey = imageinit()
    img = Image.new('RGB', (imagex, imagey), color = 'white') # create img
    dataquery()
    dt = ImageDraw.Draw(img) # make text draw cursor
    setupperpart()
    globaly = settomorrowdata()
    globaly = setbottompart(globaly)

    finalimg =  img.crop((0, 0, imagex, globaly))
    finalimg.show()
    finalimg.save('static/output.png')

    cursor.close()
    insertcursor.close()
    return

if __name__ == "__main__":
    #password.txt 파일에서 id와 pw를 가져온다
    with open('password.txt') as f:
        logindata = f.read().splitlines() 
    id = logindata[0]
    pw = logindata[1]

    #내 서버에 있는 DB에 연결
    _db = pymysql.connect(
        user=id, 
        passwd=pw, 
        host='34.83.145.171', 
        db='schedule', 
        charset='utf8'
    )
    cursor = _db.cursor(pymysql.cursors.DictCursor)
    
    today = date.today()
    tomorrow = today + timedelta(days = 1)
    sat_day = date(2022, 11, 17)

    #글로벌 위치 변수 선언.
    globalx = 0
    globaly = 0


    createimage()
