import requests
import xmltodict
from wcwidth import wcswidth 
import tkinter as tk

# https://www.opinet.co.kr/user/custapi/custApiInfo.do 에서 API key 신청 방법 확인
# 전국 주유소 평균가격
url = "http://www.opinet.co.kr/api/avgAllPrice.do?out=xml&code={API Key}"

urlresult = xmltodict.parse(requests.get(url).content)

def fmt(x, w, align='r'):
    """ 동아시아문자 폭을 고려하여, 문자열 포매팅을 해 주는 함수. 
    w 는 해당 문자열과 스페이스문자가 차지하는 너비. 
    align 은 문자열의 수평방향 정렬 좌(l)/우(r)/중간(c). """
    x = str(x)
    l = wcswidth(x)
    s = w - l
    if s <= 0:
        return x
    if align == 'l':
        return x + ' '*s
    if align == 'c':
        sl = s // 2
        sr = s - sl
        return ' '*sl + x + ' '*sr
    return ' '*s + x

for i in urlresult['RESULT']['OIL']:
    print('날짜 : ' + i['TRADE_DT'] + ', 유종 : ' + fmt(i['PRODNM'], 12, 'l') + ', 평균 금액 : ' + f"{i['PRICE']:>7}" + '원, 전일 대비 : ' + i['DIFF'] + '원')