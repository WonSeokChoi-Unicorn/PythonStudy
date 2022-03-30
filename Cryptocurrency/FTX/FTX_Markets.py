# pip install ftx
import ftx
# 클라이언트 선언
client = ftx.FtxClient()
# 암호 화폐 리스트 가져오기
markets = client.get_markets()
# 모든 암호 화폐 리스트 확인
for market in markets:
    # 암호 화폐 이름 출력
    print(str(markets.index(market) + 1) + " / " + str(len(markets)) + " - " + market['name'])