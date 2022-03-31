# pip install pybithumb
import pybithumb

# 암호 화폐 종류 확인
tickers = pybithumb.get_tickers()
# 모든 암호 화폐 리스트 확인
for ticker in tickers:
    # 암호 화폐 이름, 00시 기준으로 시가/고가/저가/종가/거래량 정보 출력
    print(str(tickers.index(ticker) + 1) + " / " + str(len(tickers)) + " - " + ticker + " - " + str(pybithumb.get_market_detail(ticker)))