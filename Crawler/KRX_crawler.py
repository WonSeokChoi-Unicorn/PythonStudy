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
# 엑셀로 저장하기
krx_df.to_excel('KRXlist.xlsx')