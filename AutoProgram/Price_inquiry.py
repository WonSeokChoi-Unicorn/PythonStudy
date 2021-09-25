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
# 주식
def inquiry1():
    price1 = 0
    # 오늘 삼성전자
    price1 = fdr.DataReader('005930', today, today, exchange='KRX')
    # 개장 전 또는 휴장 여부 체크
    if price1.empty:
        print('Stock market closed!')
    else:
        # 종가(Close)만 가져오기
        closeprice1 = price1['Close'][0]
        # 현재 시간을 YYYY/MM/DD HH:MM:SS 형태로 변경
        now_time = '({})'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
        # 금액을 출력
        print(now_time + ' Stock : ' + str(closeprice1))
        # 목표가 설정
        setprice1 = 77000
        # 목표가를 넘어가면 slack으로 알림        
        if closeprice1 > setprice1:
            # 안내문구 설정
            text1 = now_time + " Stock(" + str(closeprice1) + ") exceeded the set price(" + str(setprice1) +")"
            # 안내문구 출력
            print(text1)
            # Send a message to Slack channel
            post_message(myToken, "#channel", text1)
    # 1분(60초)마다 반복 실행
    threading.Timer(60, inquiry1).start()
# 암호화폐
def inquiry2():
    price2 = 0
    # 오늘 비트코인
    price2 = fdr.DataReader('BTC/KRW', today, today)
    # 종가(Close)만 가져오기
    closeprice2 = price2['Close'][0]
    # 현재 시간을 YYYY/MM/DD HH:MM:SS 형태로 변경
    now_time = '({})'.format(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
    # 금액을 출력
    print(now_time + ' Cryptocurrency : ' + str(closeprice2))
    # 목표가 설정
    setprice2 = 53042000
    # 목표가를 넘어가면 slack으로 알림
    if closeprice2 > setprice2:
        # 안내문구 설정
        text2 = now_time + " Cryptocurrency(" + str(closeprice2) + ") exceeded the set price(" + str(setprice2) +")"
        # 안내문구 출력
        print(text2)
        # Send a message to Slack channel
        post_message(myToken, "#channel", text2)
    # 1분(60초)마다 반복 실행
    threading.Timer(60, inquiry2).start()
# 주식 알람 받으려면 inquiry1, 암호화폐 알람 받으려면 inquiry2 사용하고, 사용하지 않는 함수는 주석 처리
# inquiry1()
# inquiry2()
