# https://pypi.org/project/holidays/
import datetime
import holidays

# 검색 위한 시작일과 종료일을 입력 받음
fromdate = str(input("공휴일을 검색 위한 시작일은? (YYYYMMDD)> "))
todate   = str(input("공휴일을 검색 위한 종료일은? (YYYYMMDD)> "))

kr_holidayslistsum =[]

# ISO code KR or KOR
kr_holidays = holidays.KR()

# 해당 기간 동안 있는 공휴일 표시
kr_holidayslist = kr_holidays[ fromdate : todate ]

# YYYYMMDD로 변경
for i in range(len(kr_holidayslist)):
    # print(type(kr_holidayslist[i]))
    kr_holidayslistsum.append(kr_holidayslist[i].strftime('%Y%m%d'))


nowdate = datetime.datetime.now()
str_today = nowdate.strftime('%Y%m%d')

def print_whichday(year, month, day) :
    r = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
    aday = datetime.date(year, month, day)
    bday = aday.weekday()
    return r[bday]

for s in range(len(kr_holidayslistsum)):
    weekname = print_whichday(int(kr_holidayslist[s].strftime('%Y')), int(kr_holidayslist[s].strftime('%m')), int(kr_holidayslist[s].strftime('%d')))
    print(kr_holidays.get(kr_holidayslist[s].strftime('%Y-%m-%d')) + " : " + kr_holidayslistsum[s], weekname)

for t in range(len(kr_holidayslistsum)):
    # 오늘이 휴일에 해당하는 지 체크
    if str_today == kr_holidayslistsum[t]:
        # print(t)
        print("###################################################")
        print("Today(" + str_today + ") is Holiday!")
        print("###################################################")
