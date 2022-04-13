import requests
import json
import pandas as pd

# Dataframe 생성
crytodf = pd.DataFrame(columns=['코드', '한글명'])
# Dataframe 생성 (KRW)
crytokrwdf = pd.DataFrame(columns=['코드', '한글명'])
# Dataframe 생성 (BTC)
crytobtcdf = pd.DataFrame(columns=['코드', '한글명'])
# Dataframe 생성 (USDT)
crytousdtdf = pd.DataFrame(columns=['코드', '한글명'])
# 업비트 API 마켓 코드 조회 URL
url = "https://api.upbit.com/v1/market/all"
# 유의종목 필드과 같은 상세 정보 노출 X
querystring = {"isDetails" : "false"}
# 지정 헤더
headers = {"Accept": "application/json"}
# 업비트 API 마켓 코드 조회 URL을 GET 방식으로 request
response = requests.request("GET", url, headers = headers, params = querystring)
# json으로 읽기
result = json.loads(response.text)
# 결과 처리
for ticker in result:
    # 코드
    cryto = ticker['market']
    # 한글명
    crytoKorean = ticker['korean_name']
    # 코드, 한글명 Dataframe에 추가
    crytodf = crytodf.append({'코드' : cryto, '한글명' : crytoKorean}, ignore_index=True)
    if "KRW-" in cryto:
        # 코드, 한글명 Dataframe에 추가
        crytokrwdf = crytokrwdf.append({'코드' : cryto, '한글명' : crytoKorean}, ignore_index=True)
    elif "BTC-" in cryto:
        # 코드, 한글명 Dataframe에 추가
        crytobtcdf = crytobtcdf.append({'코드' : cryto, '한글명' : crytoKorean}, ignore_index=True)
    elif "USDT-" in cryto:
        # 코드, 한글명 Dataframe에 추가
        crytousdtdf = crytousdtdf.append({'코드' : cryto, '한글명' : crytoKorean}, ignore_index=True)
# 코드, 한글명 Dataframe을 엑셀 파일로 저장
crytodf.to_excel("C:\\temp\\upbitallname.xlsx")
crytokrwdf.to_excel("C:\\temp\\upbitkrwname.xlsx")
crytobtcdf.to_excel("C:\\temp\\upbitbtcname.xlsx")
crytousdtdf.to_excel("C:\\temp\\upbitusdtname.xlsx")