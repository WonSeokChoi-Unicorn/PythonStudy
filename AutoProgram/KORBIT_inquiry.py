# 코빗 라이브러리 사용
import pykorbit
# 현재 시간을 보여주기 위해서 사용
import datetime
# slacker 사용 (최근 봇을 만들 경우 request 방법을 사용, https://developerdk.tistory.com/96 참고)
from slacker import Slacker
# 파이썬 내장 쓰레딩 함수 
import threading

def dbgout(message):
    """인자로 받은 문자열을 파이썬 셸과 슬랙으로 동시에 출력한다."""
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message)
    strbuf = datetime.now().strftime('[%m/%d %H:%M:%S] ') + message
    # Slack Bot User OAuth Access Token
    slack = Slacker('key')
    slack.chat.post_message('#채널', strbuf)

def inquiry():
    # 리플(XRP)의 현재가를 가져옵니다
    price = pykorbit.get_current_price("XRP")
    # 현재 시간을 표현합니다
    now_time = '({})'.format(datetime.datetime.now().strftime('%y/%m/%d %H:%M:%S'))
    print(now_time + ' ' + str(price))
    # 목표가(여기는 1500원)을 넘어가면 slack으로 알림
    if price > 1500:
        print("XRP is over 1,500KRW, It's time to sell")
        dbgout("XRP is over 1,500KRW, It's time to sell")
    # 10분(600초)마다 반복 실행
    threading.Timer(600, inquiry).start()

inquiry()