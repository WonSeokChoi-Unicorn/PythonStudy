# pip install pyupbit
import pyupbit
import time

# 암호 화폐 종류 확인
tickers = pyupbit.get_tickers()
# 모든 암호 화폐 리스트 확인
for ticker in tickers:
    # 암호 화폐 이름 출력
    print(str(tickers.index(ticker) + 1) + " / " + str(len(tickers)) + " - " + ticker)
    # 암호 화폐 고가/시가/저가/종가/거래량 출력
    # interval day/minute1/minute3/minute5/minute10/minute15/minute30/minute60/minute240/week/month
    # count 파라미터를 입력하지 않을 경우 default value는 200
    df = pyupbit.get_ohlcv(ticker, count = 600, interval = "minute1")
    print(df)