import requests
import datetime
# import time
from bs4 import BeautifulSoup
# 일시 정지 기능 사용 위해서 os 모듈을 import 한다.
import os

def print_whichday(year, month, day) :
    r = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
    aday = datetime.date(year, month, day)
    bday = aday.weekday()
    return r[bday]

def get_request_query(url, operation, params, serviceKey):
    import urllib.parse as urlparse
    params = urlparse.urlencode(params)
    request_query = url + '/' + operation + '?' + params + '&' + 'serviceKey' + '=' + serviceKey
    return request_query

# 검색 위한 년도를 입력 받음
year = str(input("공휴일을 검색하고 싶은 년도는? (YYYY)> "))

# year = 2021
# data.go.kr에 가서 신청 https://www.data.go.kr/data/15012690/openapi.do 후 일반 인증키 (UTF-8) 받기
# 2년 후 다시 신청해야 됨
mykey = "일반 인증키"
holidaydatelist = []

for month in range(1,13):

    if month < 10:
        month = '0' + str(month)
    else:
        month = str(month)
    
    url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService'
    # getHoliDeInfo 에는 제헌절이 나오나 isHoliday이 N, getRestDeInfo 에는 제헌절이 안 나옴
    operation = 'getRestDeInfo'
    params = {'solYear':year, 'solMonth':month}

    request_query = get_request_query(url, operation, params, mykey)
    get_data = requests.get(request_query)    

    if True == get_data.ok:
        soup = BeautifulSoup(get_data.content, 'html.parser')        
        
        item = soup.findAll('item')
        #print(item);
        for i in item:
            
            day = int(i.locdate.string[-2:])
            weekname = print_whichday(int(year), int(month), day)
            print(i.datename.string, i.locdate.string, weekname) 
            # 공휴일을 list에 담기
            holidaydatelist.append(i.locdate.string) 

nowdate = datetime.datetime.now()
str_today = nowdate.strftime('%Y%m%d')
for t in range(len(holidaydatelist)):
    # 오늘이 휴일에 해당하는 지 체크
    if str_today == holidaydatelist[t]:
        # print(t)
        print("###################################################")
        print("Today(" + str_today + ") is Holiday!")
        print("###################################################")

print("아무 키나 누르면 종료합니다")
os.system('Pause')