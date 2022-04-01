# pip install ftx
import ftx
# 클라이언트 선언
client = ftx.FtxClient()
# 암호 화폐 리스트 가져오기
markets = client.get_markets()
# 모든 암호 화폐 리스트 확인
for market in markets:
    # 암호 화폐 순서 출력
    print(str(markets.index(market) + 1) + " / " + str(len(markets)) + " - " + market['name'])
    # 암호 화폐의 시장 정보 출력
    market = client.get_market(market['name'])
    for key, value in market.items():
        print(key, ":", value)