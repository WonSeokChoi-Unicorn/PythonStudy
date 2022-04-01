# pip install pyupbit
import pyupbit
import time

# 암호 화폐 종류 확인
tickers = pyupbit.get_tickers()
# 모든 암호 화폐 리스트 확인
for ticker in tickers:
    # 암호 화폐 이름 출력
    print(str(tickers.index(ticker) + 1) + " / " + str(len(tickers)) + " - " + ticker)
    # 암호 화폐 현재가 출력
    print(pyupbit.get_current_price(ticker))
    # 분당 600회, 초당 10회 사용 가능하므로 시간 지연
    time.sleep(0.25)