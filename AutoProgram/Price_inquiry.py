# 파이썬 내장 datetime 함수 
from datetime import datetime
# 파이썬 내장 쓰레딩 함수 
import threading
# Slack 알림을 사용하기 위한 requests (설치 필요)
import requests
# FinanceDataReader 라이브러리 사용 (설치 필요)
import FinanceDataReader as fdr
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
# 한국 주식
def inquiry1():
    price1 = 0
    # 한국 주식 코드
    stockcode1 = '005930'
    # 한국 증권 거래소
    stockex1 = 'KRX'
    # 한국 증권 거래소의 리스트 가져오기
    stocks1 = fdr.StockListing(stockex1)
    # 한국 증권 거래소의 주식명 가져오기
    stockname1 = stocks1[stocks1['Symbol'] == stockcode1]
    # Name 컬럼만 가져오기
    finalstockname1 = stockname1['Name'].values[0]
    # 오늘 삼성전자
    price1 = fdr.DataReader(stockcode1, today, today, exchange=stockex1)
    # 현재 시간을 YYYY/MM/DD HH:MM:SS 형태로 변경
    now_time = '({})'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
    # 개장 전 또는 휴장 여부 체크
    if price1.empty:
        print(now_time + ' ' + finalstockname1 + ' Stock market closed!')
    else:
        # 종가(Close)만 가져오기
        closeprice1 = price1['Close'][0]
        # 금액을 출력
        print(now_time + ' ' + finalstockname1 + ' Stock : ' + str(closeprice1))
        # 목표가 설정
        setprice1 = 77000
        # 목표가를 넘어가면 slack으로 알림        
        if closeprice1 > setprice1:
            # 안내문구 설정
            text1 = now_time + ' ' + finalstockname1 + " (" + str(closeprice1) + ") exceeded the set price(" + str(setprice1) +")"
            # 안내문구 출력
            print(text1)
            # Send a message to Slack channel
            post_message(myToken, "#channel", text1)
    # 10분(60초)마다 반복 실행
    threading.Timer(60, inquiry1).start()            
# 암호화폐
def inquiry2():
    price2 = 0
    # 암호 화폐 종류
    Crypto = 'BTC/KRW'
    # 오늘 비트코인
    price2 = fdr.DataReader(Crypto, today, today)
    # 현재 시간을 YYYY/MM/DD HH:MM:SS 형태로 변경
    now_time = '({})'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
    if price2.empty:
        print(now_time + ' There is no ' + Crypto + '-price!')
    else:
        # 종가(Close)만 가져오기
        closeprice2 = price2['Close'][0]
        # 금액을 출력
        print(now_time + ' ' + Crypto + ' Cryptocurrency : ' + str(closeprice2))
        # 목표가 설정
        setprice2 = 53042000
        # 목표가를 넘어가면 slack으로 알림
        if closeprice2 > setprice2:
            # 안내문구 설정
            text2 = now_time + ' ' + Crypto + " Cryptocurrency(" + str(closeprice2) + ") exceeded the set price(" + str(setprice2) +")"
            # 안내문구 출력
            print(text2)
            # Send a message to Slack channel
            post_message(myToken, "#channel", text2)
    # 1분(60초)마다 반복 실행
    threading.Timer(60, inquiry2).start()
# 주식
def inquiry3():
    # 반복 실행으로 종가 초기화
    price3 = 0
    # 홍콩 주식 코드 : KUAISHOU-W
    stockcode3 = '1024'
    # 홍콩 주식명을 가져오기 위해서 00000 형식으로 처리
    stocklistcode1 = "{:0>5}".format(stockcode3)
    # 홍콩 증권 거래소
    stockex3 = 'HKEX'
    # 홍콩 증권 거래소의 리스트 가져오기
    stocks3 = fdr.StockListing(stockex3)
    # 홍콩 증권 거래소의 주식명 가져오기
    stockname3 = stocks3[stocks3['Symbol'] == stocklistcode1]
    # Name 컬럼만 가져오기
    finalstockname3 = stockname3['Name'].values[0]
    # 오늘 홍콩거래소 - WINDMILL Group Ltd
    price3 = fdr.DataReader(stockcode3, today, today, exchange=stockex3)
    # 현재 시간을 YYYY/MM/DD HH:MM:SS 형태로 변경
    now_time = '({})'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))    
    # 개장 전 또는 휴장 여부 체크
    if price3.empty:
        print(now_time + ' ' + finalstockname3 + ' Stock market closed!')
    else:
        # 종가(Close)만 가져오기
        closeprice3 = price3['Close'][0]
        # 금액을 출력
        print(now_time + ' ' + finalstockname3 + ' Stock : ' + str(closeprice3))
        # 목표가 설정
        setprice3 = 2.7        
        # 목표가를 넘어가면 slack으로 알림        
        if closeprice3 > setprice3:
            # 안내문구 설정
            text3 = now_time + ' ' + finalstockname3 + " (" + str(closeprice3) + ") exceeded the set price(" + str(setprice3) +")"
            # 안내문구 출력
            print(text3)
            # Send a message to Slack channel
            post_message(myToken, "#stocktrading", text3)
    # 1분(60초)마다 반복 실행
    threading.Timer(60, inquiry3).start()
# 한국 주식 알람 받으려면 inquiry1, 암호화폐 알람 받으려면 inquiry2, 홍콩 주식 알람 받으려면 inquiry3, 사용하지 않는 함수는 주석 처리
# inquiry1()
# inquiry2()
# inquiry3()
