from pandas import DataFrame
import pandas as pd
from wcwidth import wcswidth

# 컬럼명이 데이터보다 길이가 더 긴 경우
# Sample 데이터
raw_data = {'col0': [1, 2, 3, 4],
            'col1': [10, 20, 30, 40]}
# Dataframe 생성
df = DataFrame(raw_data)
# 엑셀로 저장
writer = pd.ExcelWriter("C:\\temp\\columnslong.xlsx", engine='xlsxwriter')
# 엑셀 파일로 저장
df.to_excel(writer, index = False)
# 엑셀 컬럼 폭 자동 조절 - 컬럼명과 컬럼 데이터 중 가장 길이가 긴 값으로 설정
for column in df:
    collist = df[column].astype(str).values
    maxcollen = 0
    for col in collist:
        collen = wcswidth(col)
        if maxcollen < collen:
            maxcollen = collen
    column_width = max(maxcollen, wcswidth(column))
    col_idx = df.columns.get_loc(column)
    writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_width)
# 엑셀 작성 완료 후 파일 저장
writer.save()
# 데이터가 컬럼명보다 길이가 더 긴 경우
# Sample 데이터
raw_data = {'0': [10, 20, 30, 40],
            '1': [100, 200, 300, 400]}
# Dataframe 생성
df = DataFrame(raw_data)
# 엑셀로 저장
writer = pd.ExcelWriter("C:\\temp\\columnsshort.xlsx", engine='xlsxwriter')
# 엑셀 파일로 저장
df.to_excel(writer, index = False)
# 엑셀 컬럼 폭 자동 조절 - 컬럼명과 컬럼 데이터 중 가장 길이가 긴 값으로 설정
for column in df:
    collist = df[column].astype(str).values
    maxcollen = 0
    for col in collist:
        collen = wcswidth(col)
        if maxcollen < collen:
            maxcollen = collen
    column_width = max(maxcollen, wcswidth(column))
    col_idx = df.columns.get_loc(column)
    writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_width)
# 엑셀 작성 완료 후 파일 저장
writer.save()