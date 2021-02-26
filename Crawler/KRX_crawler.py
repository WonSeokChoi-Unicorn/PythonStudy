# Google Colaboratory 접속하기
# https://colab.research.google.com/

import pandas as pd
from pykrx import stock
# excel 파일을 다운로드하는거와 동시에 pandas에 load하기
# 흔히 사용하는 df라는 변수는 data frame을 의미합니다.
df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]

# 종목코드에 값을 6자리 문자열로 설정 
# 종목코드의 숫자값을 6자리 문자열로 변환
# 채우는 자리는 0으로 채우기
df.종목코드 = df.종목코드.map('{:06d}'.format)

# 날짜형으로 변환
df['상장일'] = df['상장일'].astype('datetime64[ns]')
# 상장일에 1년 후 날짜 구해서 새로운 컬럼 만들기
df['상장일1년후'] = df['상장일'] + pd.DateOffset(years=1)
df['상장종가'] = 0
df['상장1년후종가'] = 0

df = df[['회사명' , '종목코드' , '상장일' , '상장일1년후' , '상장종가' , '상장1년후종가']]

# pandas data frame을 '상장일' 기준으로 정렬 (ascending=[True], [False]로 오름차순, 내림차순 정렬)
df = df.sort_values(['상장일'], ascending=[True])
# print(df.head(4000))
# print(len(df))
price = 0
pricelist = []
afteryearprice = 0
afteryearpricelist = []

for i in range(len(df)):
    # 종목 코드를 변수에 저장하기
    code = ""
    birthdate = ""
    atferyeardate = ""
    code = df['종목코드'][i]
    print('종목코드 : ' + code)
    birthdate = df['상장일'][i]
    formattedbirthDate = birthdate.strftime("%Y%m%d")
    afteryeardate = df['상장일1년후'][i]
    formattedafteryeardate = afteryeardate.strftime("%Y%m%d")
    # print(formattedbirthDate, type(formattedbirthDate))
    # print(formattedafteryeardate, type(formattedafteryeardate))
    
    # 상장 폐지 등의 이유로 네이버 증권에 검색되지 않는 종목들이 있어서 예외 처리 필요 (예. 교보메리츠 064900)

    # 함수 통해서 나온 상장종가를 변수에 저장하기
    price = stock.get_market_ohlcv_by_date(formattedbirthDate, formattedbirthDate, code)
    pricelist = [price['종가'].values[0]]
    print('상장종가 : ' + str(pricelist))
    # 함수 통해서 나온 상장1년후종가를 변수에 저장하기
    afteryearprice = stock.get_market_ohlcv_by_date(formattedafteryeardate, formattedafteryeardate, code)
    if len(afteryearprice) == 0:
        afteryearpricelist.append(0)
    else:
        afteryearpricelist = [afteryearprice['종가'].values[0]]        
    print('상장1년후종가 : ' + str(afteryearpricelist))

print(pricelist)
print(afteryearpricelist)
# dataframe에 넣기
