import requests
import json
from pandas.io.json import json_normalize

# 네이버 증권에서 ETF만 가져오기
etfurl = 'https://finance.naver.com/api/sise/etfItemList.nhn'
# json으로 가져오기
json_data = json.loads(requests.get(etfurl).text)
# dataframe으로 변환하기
etf_df = json_normalize(json_data['result']['etfItemList'])
# 불필요한 컬럼들 삭제
etf_df.drop('etfTabCode', axis=1, inplace=True)
etf_df.drop('nowVal', axis=1, inplace=True)
etf_df.drop('risefall', axis=1, inplace=True)
etf_df.drop('changeVal', axis=1, inplace=True)
etf_df.drop('changeRate', axis=1, inplace=True)
etf_df.drop('nav', axis=1, inplace=True)
etf_df.drop('threeMonthEarnRate', axis=1, inplace=True)
etf_df.drop('quant', axis=1, inplace=True)
etf_df.drop('amonut', axis=1, inplace=True)
etf_df.drop('marketSum', axis=1, inplace=True)
# 컬럼명 변경하기
etf_df = etf_df.rename(columns={'itemcode': 'code', 'itemname': 'company'})
# 엑셀로 저장하기
etf_df.to_excel('etflist.xlsx')