import pandas as pd
# Excel 읽기
exceldata = pd.read_excel('C:\\testdoc.xlsx')
# NaN 값이 있는 행은 제거
exceldata = exceldata.dropna()
# Excel의 인덱스 수만큼 반복
for i in exceldata.index:
    # 현재 인덱스의 내용을 가져온다 text1, text2 컬럼이 있다고 가정
    text1 = exceldata.loc[i, 'text1']
    text2 = exceldata.loc[i, 'text2']
    # 아래는 {} {}로 변경 가능
    print('{} - {}'.format(text1, text2))