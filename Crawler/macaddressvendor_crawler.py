import json
import requests
import pandas as pd
from datetime import datetime
from wcwidth import wcswidth
import progressbar

# 검색할 Mac Address 리스트 파일
filename = 'C:\\Temp\\macaddresslist.txt'
# 없앨 기호
deletestr = str.maketrans({'.' : '', '-' : '', ':' : ''})
# 검색할 Mac Address URL
maurl = "https://www.wireshark.org/assets/js/manuf.json"
# 검색할 Mac Address URL 연결
maresult = json.loads(requests.get(maurl).content)
# Dataframe 컬럼에 이름 설정.
madataname = ['Mac Address', 'Vendor']
# Dataframe 선언
madf = pd.DataFrame(columns = madataname)
# 오늘 날짜를 YYYYMMDDHHMMSS 형태로 변경
todaytime = datetime.today().strftime('%Y%m%d%H%M%S')
# XLSX 정보
writer = pd.ExcelWriter("C:\\Temp\\"+ todaytime + "_MacAddressVendor.xlsx", engine='xlsxwriter')
# 검색할 Mac Address 리스트 파일 읽기
f1 = open(filename, 'r')
# 전체 가져오기
filelines = f1.readlines()
# 검색할 Mac Address 리스트 파일 닫기
f1.close
# 진행 상황 객체 생성
bar = progressbar.ProgressBar()
# 한 줄씩 읽기
for fileline in bar(filelines):
    # 기호 없애기
    macaddress = fileline.translate(deletestr).strip()
    # 왼쪽에서 6자리까지만 가져오기
    macaddress = macaddress[0:5 + 1].lower()
    # Mac Address List에서 찾기
    macaddressvendor = maresult['data'].get(macaddress)
    # Dataframe에 추가
    madf = madf.append({'Mac Address' : fileline.strip(), 'Vendor' : macaddressvendor}, ignore_index = True)
# 엑셀 파일로 저장
madf.to_excel(writer, index = False)
# 엑셀 컬럼 폭 자동 조절
for column in madf:
    collist = madf[column].astype(str).values
    maxcollen = 0
    for col in collist:
        collen = wcswidth(col)
        if maxcollen < collen:
            maxcollen = collen
    column_width = max(maxcollen, len(column.encode()))
    col_idx = madf.columns.get_loc(column)
    writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_width)
# 엑셀 작성 완료 후 파일 저장
writer.save()