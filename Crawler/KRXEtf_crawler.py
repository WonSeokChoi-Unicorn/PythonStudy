import requests
import json
from pandas.io.json import json_normalize
import pandas as pd

# KRX에서 상장사 가져오기
krxurl = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method='\
    'download&searchType=13'
# pandas로 html 읽어 오기
krx_df = pd.read_html(krxurl, header=0)[0]
# 종목코드와 회사명만 가져오기
krx_df = krx_df[['종목코드', '회사명']]
# 컬럼명 변경하기
krx_df = krx_df.rename(columns={'종목코드': 'code', '회사명': 'company'})
# 종목코드 형식 맞추기
krx_df.code = krx_df.code.map('{:06d}'.format)

# 네이버 증권에서 ETF만 가져오기
etfurl = 'https://finance.naver.com/api/sise/etfItemList.nhn'
# json으로 가져오기
json_data = json.loads(requests.get(etfurl).text)
# dataframe으로 변환하기
etf_df = json_normalize(json_data['result']['etfItemList'])
# 종목코드와 회사명만 가져오기
etf_df = etf_df[['itemcode', 'itemname']]
# 컬럼명 변경하기
etf_df = etf_df.rename(columns={'itemcode': 'code', 'itemname': 'company'})

# 상장자 리스트와 ETF 리스트를 합치기
stocklist = pd.concat([krx_df,etf_df])
# 엑셀로 저장하기
stocklist.to_excel('KRXEtflist.xlsx')