# pip install pyupbit
import pyupbit

# 암호 화폐 종류 확인
tickers = pyupbit.get_tickers()
# 모든 암호 화폐 리스트 확인
for ticker in tickers:
    # 암호 화폐 이름 출력
    print(str(tickers.index(ticker) + 1) + " / " + str(len(tickers)) + " - " + ticker)