# pip install pykorbit
import pykorbit

# 암호 화폐 종류 확인
tickers = pykorbit.get_tickers()
# 모든 암호 화폐 리스트 확인
for ticker in tickers:
    # 암호 화폐 이름, 24시간 동안의 저가/고가/거래금액/거래량 출력
    print(str(tickers.index(ticker) + 1) + " / " + str(len(tickers)) + " - " + ticker + " - " + str(pykorbit.get_market_detail(ticker)))
