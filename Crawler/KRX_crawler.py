# Google Colaboratory 접속하기
# https://colab.research.google.com/

import sys
import pandas as pd
# pip install pykrx
from pykrx import stock
from datetime import datetime
# sleep 기능 이용하기 위해서 필요
import time

# to_excel 기능 이용 위해 openpyxl 필요
# pip install openpyxl

# excel 파일을 다운로드 하고 pandas에 load하기
# 흔히 사용하는 df라는 변수는 data frame을 의미합니다.
# 파일 형태는 xls이지만 내용은 html
df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]

# 종목코드에 값을 6자리 문자열로 설정 
# 종목코드의 숫자값을 6자리 문자열로 변환
# 채우는 자리는 0으로 채우기
df.종목코드 = df.종목코드.map('{:06d}'.format)

# 날짜형으로 변환
df['상장일'] = df['상장일'].astype('datetime64[ns]')
# 상장일에 1년 후 날짜 구해서 새로운 컬럼 만들기
df['상장일1년후'] = df['상장일'] + pd.DateOffset(years=1)
# 상장종가, 상장1년후종가 컬럼 추가
df['상장종가'] = 0
df['상장1년후종가'] = 0
# 최종 data frame 구조
df = df[[ '회사명' , '종목코드' , '업종' , '상장일' , '상장일1년후' , '상장종가' , '상장1년후종가' ]]
# 총 몇 건인지 보여주고 시작
print("Total number : " + str(len(df)))
# 변수 선언 및 값 초기화
price = 0
pricelist = []
afteryearprice = 0
afteryearpricelist = []
nowDate = datetime.now()

for i in range(len(df)):
    # 디버그 차원에서 진행 상황을 출력
    print("No : " + str(i) + ", Name : " + str(df['회사명'][i]) + ", Code : " + str(df['종목코드'][i])
    )
    # 종목 코드 변수를 선언
    code = ""
    code = df['종목코드'][i]
    # 상장일을 YYYYMMDD 형태로 변수에 저장하기
    birthdate = ""
    birthdate = df['상장일'][i]    
    formattedbirthDate = birthdate.strftime("%Y%m%d")
    # 상장후1년일을 YYYYMMDD 형태로 변수에 저장하기
    atferyeardate = ""
    afteryeardate = df['상장일1년후'][i]
    formattedafteryeardate = afteryeardate.strftime("%Y%m%d")

    # 함수 통해서 나온 상장종가를 리스트 형태로 저장하기
    price = stock.get_market_ohlcv_by_date(formattedbirthDate, formattedbirthDate, code)
    # 상장 폐지 등의 이유로 네이버 증권에 검색되지 않는 종목은 0으로 처리
    if len(price) == 0:
        pricelist.append(0)
    else:
        pricelist.append(price['종가'].values[0])
    # 함수 통해서 나온 상장1년후종가를 변수에 저장하기
    # 상장일1년후 날짜가 오늘보다 미래이면 0으로 저장하기
    if formattedafteryeardate >= nowDate.strftime('%Y-%m-%d'):
        afteryearpricelist.append(0)
    else:
        afteryearprice = stock.get_market_ohlcv_by_date(formattedafteryeardate, formattedafteryeardate, code)
        # 상장 폐지 등의 이유로 네이버 증권에 검색되지 않는 종목은 0으로 처리
        if len(afteryearprice) == 0:
            afteryearpricelist.append(0)
        else:
            afteryearpricelist.append(afteryearprice['종가'].values[0])
    # 실행 멈춤이 자주 생긴다면 아래 멈춤 기능 활성화
    # time.sleep(1)

# 상장종가, 상장1년후종가를 dataframe에 넣기
df['상장종가'] = pricelist
df['상장1년후종가'] = afteryearpricelist

# pandas data frame을 '상장일' 기준으로 정렬 (ascending=[True], [False]로 오름차순, 내림차순 정렬)
df = df.sort_values(['상장일'], ascending=[True])

df.to_excel('krxlist.xlsx')