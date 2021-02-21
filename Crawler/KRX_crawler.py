# Google Colaboratory 접속하기
# https://colab.research.google.com/

import pandas as pd
# excel 파일을 다운로드하는거와 동시에 pandas에 load하기
# 흔히 사용하는 df라는 변수는 data frame을 의미합니다.
df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]

df = df[['회사명', '종목코드', '상장일']]
# pandas data frame을 '상장일' 기준으로 정렬 (ascending=[True], [False]로 오름차순, 내림차순 정렬)
df = df.sort_values(['상장일'], ascending=[True])
print(df.head(4000))

# 상장일 1년 뒤 종가 가져오는 부분 추가 필요