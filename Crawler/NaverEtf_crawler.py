import requests
import json
from pandas.io.json import json_normalize

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
# 엑셀로 저장하기
etf_df.to_excel('etflist.xlsx')