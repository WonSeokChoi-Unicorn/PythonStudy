# 파이썬 내장 datetime 함수 
from datetime import datetime
# 파이썬 내장 쓰레딩 함수 
import threading
# Slack 알림을 사용하기 위한 requests (설치 필요)
import requests
# FinanceDataReader 라이브러리 사용 (설치 필요)
import FinanceDataReader as fdr
# 근무일에만 발송하기 위해서 휴일 정보 확인
import holidays
# pip install pyupbit
import pyupbit
# 오늘 날짜 가져오기
nowDate = datetime.now()
# 날짜를 YYYYMMDD 형태로 변경
today = nowDate.strftime('%Y%m%d')

def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )
    print(response)
# Bot User OAuth Token을 적어 줍니다
myToken = ""

# 한국 증권 거래소
stockex = 'KRX'
# 한국 증권 거래소의 리스트 가져오기
stocks = fdr.StockListing(stockex)

stockcode = [
             '034730' # sk 034730 코스피
            ]
setprice = [
            100000 # sk 034730 코스피
           ]
# 한국 주식명 리스트
finalstockname = []

# 한국 주식 확인
def krstockinquiry():
    for stock3 in stockcode:
        # 주식명, 목표가를 가져오기 위한 index
        cnt3 = stockcode.index(stock3)
        # 종가 초기화
        closeprice3 = 0
        # 현재가
        price3 = fdr.DataReader(stock3, today, today, exchange=stockex)
        # 현재 시간을 YYYY/MM/DD HH:MM:SS 형태로 변경
        now_time = '({})'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
        # 개장 전 또는 휴장 여부 체크
        if price3.empty:
            print(now_time + ' ' + finalstockname[cnt3] + ' Stock market closed!')
        else:
            # 종가(Close)만 가져오기
            closeprice3 = price3['Close'][0]
            # 금액을 출력
            print(now_time + ' ' + finalstockname[cnt3] + ' Stock : KRW ' + str(format(closeprice3,",")))
            # 목표가를 넘어가면 slack으로 알림        
            if closeprice3 > setprice[cnt3]:
                # 안내문구 설정
                text1 = now_time + ' ' + finalstockname[cnt3] + "( KRW " + str(format(closeprice3,",")) + " ) exceeded the set price( KRW " + str(format(setprice[cnt3],",")) +" )"
                # 안내문구 출력
                print(text1)
                # Send a message to Slack channel
                post_message(myToken, "#channel", text1)
        del[[price3]]
    # 10분(600초)마다 반복 실행
    threading.Timer(600, krstockinquiry).start()

# 홍콩 증권 거래소
hkstockex = 'HKEX'
# 홍콩 증권 거래소의 리스트 가져오기
hkstocks = fdr.StockListing(hkstockex)

hkstockcode = [
               '1810' # Xiaomi Corp
              ]
hksetprice = [
              14 # Xiaomi Corp
             ]
# 홍콩 주식명 리스트
finalhkstockname = []

# 홍콩 주식 확인
def hkstockinquiry():
    for stock2 in hkstockcode:
        # 주식명, 목표가를 가져오기 위한 index
        cnt1 = hkstockcode.index(stock2)
        # 종가 초기화
        closeprice1 = 0
        # 현재가
        price1 = fdr.DataReader(stock2, today, today, exchange=hkstockex)
        # 현재 시간을 YYYY/MM/DD HH:MM:SS 형태로 변경
        now_time = '({})'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
        # 개장 전 또는 휴장 여부 체크
        if price1.empty:
            print(now_time + ' ' + finalhkstockname[cnt1] + ' Stock market closed!')
        else:
            # 종가(Close)만 가져오기
            closeprice1 = price1['Close'][0]
            # 금액을 출력
            print(now_time + ' ' + finalhkstockname[cnt1] + ' Stock : HKD ' + str(format(closeprice1,",.3f")))
            # 목표가를 넘어가면 slack으로 알림        
            if closeprice1 > hksetprice[cnt1]:
                # 안내문구 설정
                text1 = now_time + ' ' + finalhkstockname[cnt1] + "( HKD " + str(format(closeprice1,",.3f")) + " ) exceeded the set price( HKD " + str(format(hksetprice[cnt1],",.3f")) +" )"
                # 안내문구 출력
                print(text1)
                # Send a message to Slack channel
                post_message(myToken, "#channel", text1)
        del[[price1]]
    # 10분(600초)마다 반복 실행
    threading.Timer(600, hkstockinquiry).start()

cryptocode = [
              'KRW-XRP' # KRW-XRP
             ]
setcryptoprice = [
                  500 # KRW-XRP
                 ]

# 암호 화폐 확인
def cryptoinquiry():
    for crypto in cryptocode:
        # 주식명, 목표가를 가져오기 위한 index
        cnt2 = cryptocode.index(crypto)
        # 현재가 초기화
        currentprice = 0
        # 현재 시간을 YYYY/MM/DD HH:MM:SS 형태로 변경
        now_time = '({})'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
        # 업비트 암화화폐 현재가
        currentprice = pyupbit.get_current_price(crypto)
        # 금액을 출력
        print(now_time + ' ' + crypto + ' Cryptocurrency : ' + str(format(currentprice,",.3f")))
        # 목표가를 넘어가면 slack으로 알림
        if currentprice > setcryptoprice[cnt2]:
            # 안내문구 설정
            text2 = now_time + ' ' + crypto + " Cryptocurrency( KRW " + str(format(currentprice,",.3f")) + " ) exceeded the set price( KRW " + str(format(setcryptoprice[cnt2],",.3f")) +" )"
            # 안내문구 출력
            print(text2)
            # Send a message to Slack channel
            post_message(myToken, "#channel", text2)
        # 10분(600초)마다 반복 실행
    threading.Timer(600, cryptoinquiry).start()
    
# 토요일, 일요일 판단 위해 요일 확인
weekend = datetime.today().weekday()
# 홍콩 휴일 ISO code
hk_holidays = holidays.HK()
# 한국 휴일 ISO code
kr_holidays = holidays.KR()

# 암호 화폐는 1년 365일 24시간 운영되므로 시작 조건 없음
cryptoinquiry()

# 오늘이 휴일이 아니면 주가 확인 시작
if hk_holidays.get(today) == None:
    # 오늘이 주말이 아니면 주가 확인 시작
    if weekend < 5:
        # 주식 코드로 주식명 찾기
        for stock1 in hkstockcode:
            # 홍콩 주식명을 가져오기 위해서 00000 형식으로 처리
            stockcode1 = "{:0>5}".format(stock1)
            # Dataframe 형태로 가져옴
            hkstockname = hkstocks[hkstocks['Symbol'] == stockcode1]
            # 이름을 리스트에 추가
            finalhkstockname.append(hkstockname['Name'].values[0])
            # 오류로 인해 이전 자료 가져올까바 Dataframe 삭제
            del[[hkstockname]]
        # 홍콩 주식 알람
        hkstockinquiry()

# 오늘이 휴일이 아니면 주가 확인 시작
if kr_holidays.get(today) == None:
    # 오늘이 주말이 아니면 주가 확인 시작
    if weekend < 5:
        # 주식 코드로 주식명 찾기
        for stock3 in stockcode:
            # Dataframe 형태로 가져옴
            stockname = stocks[stocks['Symbol'] == stock3]
            # 이름을 리스트에 추가
            finalstockname.append(stockname['Name'].values[0])
            # 오류로 인해 이전 자료 가져올까바 Dataframe 삭제
            del[[stockname]]
        # 한국 주식 알람
        krstockinquiry()