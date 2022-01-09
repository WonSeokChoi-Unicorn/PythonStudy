""" 내용에서 숫자만 추출하는 방법
import re
temp = '<span class="style-scope ytd-grid-video-renderer">스트리밍 시간: 3주 전</span>'
number = re.findall("\d+", temp)
print(number[0])
"""
# 텐서플로우 정상 동작 테스트
# Successfully opened dynamic library cudart64_110.dll 나오면 정상
# import tensorflow as tf

"""
from collections import Counter


def sort_by_frequency(n):
    # n을 카운터
    most_n = Counter(n)
    
    most_n_list = sorted((count, -num) for num, count in most_n.items())
    result = []

    for count, num in most_n_list:
        for i in range(count):
            result.append(-num)

    return result


print(sort_by_frequency([3, 8, 8, 3, 2, 8, 1, 2, 4, 56]))
"""
"""
import urllib.request
 
url = "https://1.bp.blogspot.com/-vF3httpOv6I/YC2TYrnrBfI/AAAAAAAAjG8/zRNq4MXLHEAtwQNkNKb7WZY1MqX9yPZgQCLcBGAsYHQ/s0/07.jpg"
res = urllib.request.urlopen(url)
# print(res.status)  ## 200
"""

# from bs4 import BeautifulSoup

# htmltext='''<article><div id="article_1"><div class="document_11095623_8764177 xe_content"><p>브이로그 유튜버 진훤</p><p><br/></p><p><img alt="브이로그 유튜버 진훤 - 꾸르" class="fr-fic fr-dii" src="https://img1.daumcdn.net/thumb/R1024x0/?fname=https://t1.daumcdn.net/cafeattach/mEr9/b16ad950b981193c534e0d1c4c6a2d8acfb01dd4"/></p><p><br/></p><p><img alt="브이로그 유튜버 진훤 - 꾸르" class="fr-fic fr-dii" src="https://img1.daumcdn.net/thumb/R1024x0/?fname=https://t1.daumcdn.net/cafeattach/mEr9/99ae4a43d456f27aa1376abe79d08e047167a4b6"/></p><p><br/></p><p><img alt="브이로그 유튜버 진훤 - 꾸르" class="fr-fic fr-dii" src="https://img1.daumcdn.net/thumb/R1024x0/?fname=https://t1.daumcdn.net/cafeattach/mEr9/39dea46de597f5b72fe7a31ed931bb56045cb1e3"/></p><p><br/></p><p><img alt="브이로그 유튜버 진훤 - 꾸르" class="fr-fic fr-dii" src="https://img1.daumcdn.net/thumb/R1024x0/?fname=https://t1.daumcdn.net/cafeattach/mEr9/9f30e653ca20fba6db10e51359cbf0ac22a80bb6"/></p><p><br/></p><p><img alt="브이로그 유튜버 진훤 - 꾸르" class="fr-fic fr-dii" src="https://img1.daumcdn.net/thumb/R1024x0/?fname=https://t1.daumcdn.net/cafeattach/mEr9/57a0efbcdd20de4d6f8295dee9931ea432cb9c23"/></p><p><br/></p><p><img alt="브이로그 유튜버 진훤 - 꾸르" class="fr-fic fr-dii" src="https://img1.daumcdn.net/thumb/R1024x0/?fname=https://t1.daumcdn.net/cafeattach/mEr9/144999b90a37a30b81adbc4d236a00dbde012555"/></p><p><br/></p><p><img alt="브이로그 유튜버 진훤 - 꾸르" class="fr-fic fr-dii" src="https://img1.daumcdn.net/thumb/R1024x0/?fname=https://t1.daumcdn.net/cafeattach/mEr9/6c8b71be6a2dffdc77b756f06f26213a412cb123"/></p><p><br/></p><p><img alt="브이로그 유튜버 진훤 - 꾸르" class="fr-fic fr-dii" src="https://img1.daumcdn.net/thumb/R1024x0/?fname=https://t1.daumcdn.net/cafeattach/mEr9/b31b9773e7643d3ea8203762e60c331e4d47ba80"/></p><p><br/></p><p><img alt="브이로그 유튜버 진훤 - 꾸르" class="fr-fic fr-dii" src="https://img1.daumcdn.net/thumb/R1024x0/?fname=https://t1.daumcdn.net/cafeattach/mEr9/ea1ae1457151b6af6708366bfaa37c30fd79fd45"/></p><p><br/></p><p><img alt="브이로그 유튜버 진훤 - 꾸르" class="fr-fic fr-dii" src="https://img1.daumcdn.net/thumb/R1024x0/?fname=https://t1.daumcdn.net/cafeattach/mEr9/90c403a338c35324ae729ba07feb48fcdfbb07d4"/></p><p><br/></p><p><img alt="브이로그 유튜버 진훤 - 꾸르" class="fr-fic fr-dii" src="https://img1.daumcdn.net/thumb/R1024x0/?fname=https://t1.daumcdn.net/cafeattach/mEr9/ca5a63edfcefcc8a765a3b9efccb2d127eddf69c"/></p><p><br/></p><p><img alt="브이로그 유튜버 진훤 - 꾸르" class="fr-fic fr-dii" src="https://img1.daumcdn.net/thumb/R1024x0/?fname=https://t1.daumcdn.net/cafeattach/mEr9/a3551fa9b9b6b71e92362305810509e4e589ace8"/></p><p><br/></p></div></div></article>'''

# html = BeautifulSoup(htmltext)

# for pLine in html.div.div.children:
#     for p_tag in pLine.select("p"):
#         print("문자열 " + p_tag.text)

# if "브이로그 유튜버 진훤" in html:
#     print("존재합니다",html)

# from pykrx import stock
# df1 = stock.get_market_ohlcv_by_date("20201230", "20201230", "005930")
# print(df1)

"""
import urllib.parse
import pandas as pd

MARKET_CODES = {
    'kospi': 'stockMkt',
    'kosdaq': 'kosdaqMkt',
    'konex': 'konexMkt'
}

CORP_LIST_PATH = 'kind.krx.co.kr/corpgeneral/corpList.do'

def get_stock_code_list(market=None, delisted=False):
    param = {'method': 'download'}

    if market.lower() in MARKET_CODES:
        param['marketType'] = MARKET_CODES[market]

    if not delisted:
        param['searchType'] = 13

    params = urllib.parse.urlencode(param)
    url = urllib.parse.urlunsplit(['http', CORP_LIST_PATH, '', params, ''])
    print(url)

    df = pd.read_html(url, header=0)[0]
    return df
stocks = get_stock_code_list('kospi', 'delisted')
print(stocks.head())
"""
# 공휴일 공공 정보
# Python 샘플 코드 #


# from urllib.request import Request, urlopen
# from urllib.parse import urlencode, quote_plus

# url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getAnniversaryInfo'
# queryParams = '?' + urlencode({ quote_plus('ServiceKey') : '서비스키', quote_plus('pageNo') : '1', quote_plus('numOfRows') : '100', quote_plus('solYear') : '2021', quote_plus('solMonth') : '03' })

# request = Request(url + queryParams)
# request.get_method = lambda: 'GET'
# response_body = urlopen(request).read()
# print(response_body)

# str = '[쓰리박] 박지성 인맥이 부러운 이청용'

# print(str.endswith('이청용'))

# print(str.startswith('[쓰리박]'))

# print('박지성' in str)

# application 실행하기 위한 라이브러리 import
# from pywinauto import application
# import pywinauto
# 64bit Python 사용하면서 32bit 어플리케이션 자동화시 나오는 UserWarning를 없애기 위해 import
# import warnings
# warnings.simplefilter('ignore', category=UserWarning)
# # application 실행하기 위한 명령어 단축
# app = application.Application()
# app.start("notepad.exe")
# dlg = app['제목 없음 - Windows 메모장']
# dlg.print_control_identifiers()

# from datetime import datetime, timedelta
# from dateutil.relativedelta import relativedelta

# fromdate = datetime(2006, 1, 1, 0, 0, 0)
# presentmonth = datetime(datetime.today().year, datetime.today().month, 1, 0, 0, 0)

# i = -1
# while True:
#     i += 1
#     delta = relativedelta(months=int(i))
#     searchdate = fromdate + delta
#     print(searchdate.strftime('%Y-%m'))
#     if searchdate == presentmonth:
#         break


# import pandas as pd

# df = pd.DataFrame([
#     [16, 7, 10],
#     [15, 8, 11],
#     [14, 9, 12]],
#     columns = ['a', 'b', 'c'],
#     index = [1, 2, 3]
# )

# print(df)

# df = df.sort_values('a')

# print(df)

# import googletrans

# # 번역기 개체
# translator = googletrans.Translator()
# # 영어를 한국어로 번역
# result = translator.translate('How one of the most profitable companies in history rose to power - Adam Clulow', dest='ko')
# print(result.text)

# import requests

# url = "https://translate.kakao.com/translator/translate.json"

# headers = {
#     "Referer": "https://translate.kakao.com/",
#     "User-Agent": "Mozilla/5.0"
# }

# data = {
#     "queryLanguage": "en",
#     "resultLanguage": "kr",
#     "q": "How one of the most profitable companies in history rose to power - Adam Clulow"
# }

# resp = requests.post(url, headers=headers, data=data)
# data = resp.json()
# output = data['result']['output'][0][0]
# print(output)

# from urllib.request import Request, urlopen
# # 봇 방지 웹사이트 회피
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
# urlheaders = Request('https://ggoorr.net/', headers = headers)
# urldata = urlopen(urlheaders)
# page = urldata.read()

# print(page)
# res = requests.get(GGOORR_DETAIL_URL + str(page), headers=headers)

# url = "https://www.opinet.co.kr/api/lowTop10.do?out=json&code=F211220272&cnt=20&prodcd=D047&area=04"
# url = "http://www.opinet.co.kr/api/lowTop10.do?out=json&code=F210906183&cnt=20&prodcd=B034&area=0108"
# print(url.find("&area="))
# print(str(url.find("&area=")+5))
# print(url[89:])
# print(url[79:82+1])

from pyproj import Proj, transform

print(Proj('epsg:5178')(318031.7049, 513942.4367))

# transg = Transformer.from_crs(crs_proj.geodetic_crs, crs_proj)
# transg.transform(52.067567, 5.068913)