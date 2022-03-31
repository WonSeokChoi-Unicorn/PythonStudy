# pip install pybithumb
import pybithumb

# 암호 화폐 종류 확인
tickers = pybithumb.get_tickers()
# 모든 암호 화폐 리스트 확인
for ticker in tickers:
    # 암호 화폐 이름, 시가/종가/고가/저가/거래량 정보를 DataFrame으로 출력
    # chart_intervals : 1m, 3m, 5m, 10m, 30m, 1h, 6h, 12h, 24h
    print(str(tickers.index(ticker) + 1) + " / " + str(len(tickers)) + " - " + ticker)
    df = pybithumb.get_candlestick(ticker, chart_intervals="1m")
    print(df.tail(5))