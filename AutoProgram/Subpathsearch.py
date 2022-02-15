import os
import pandas as pd

# 엑셀로 저장하기 위해서 Dataframe 선언
df = pd.DataFrame(columns=['Path&File'])

# 하위 경로 검색하게 해주는 os.walk
# "Q:\\"에 검색 원하는 경로 적어 주기
for (path, dir, files) in os.walk("Q:\\"):
    for filename in files:
        df = df.append({'Path&File' : path + '\\' + filename}, ignore_index=True)
df.to_excel("filelist.xlsx")