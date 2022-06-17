# pip install pycoingecko
from pycoingecko import CoinGeckoAPI
import time
cg = CoinGeckoAPI()

# 암호 화폐 종류 확인
tickers = cg.get_coins_list()
# 모든 암호 화폐 리스트 확인
for ticker in tickers:
    # 암호 화폐 이름 출력
    print(str(tickers.index(ticker) + 1) + " / " + str(len(tickers)) + " - " + ticker['id'] + " - " + ticker['symbol'] + " - " + ticker['name'])
    # 시간 지연 Free API has a rate limit of 50 calls/minute
    time.sleep(1.25)