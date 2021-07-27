# 구글 번역 API import
# pip install googletrans==4.0.0-rc1
import googletrans
# 파일 존재 여부 확인 위한 os를 import 한다.
import os
# 번역기 개체
translator = googletrans.Translator()
# 번역할 텍스트 파일을 한 줄씩 읽어 옵니다
# 경로에 기본 확장 문자(escape sequence)를 피하기 위해서 역슬래시를 2개 사용
finput = open("input.txt", 'rt', encoding='UTF8')
# 총 라인수 구하기
totalcnt = len(finput.readlines())
finput.close()
# 위에서 총 라인수 구하다보니 마지막 줄을 읽은 상태라 다시 읽기
# 경로에 기본 확장 문자(escape sequence)를 피하기 위해서 역슬래시를 2개 사용
finput = open("input.txt", 'rt', encoding='UTF8')
# 한 줄씩 읽기
lines = finput.readlines()
# 번역한 문장을 텍스트 파일로 저장
if os.path.isfile("output.txt"):
    # 파일이 존재할 경우 추가
    foutput = open("output.txt", mode='at', encoding='utf-8')
else:
    # 파일이 존재하지 않을 경우 생성
    foutput = open("output.txt", mode='wt', encoding='utf-8')
# 진행 라인수 구하기
cnt = 0
for line in lines:
    cnt += 1
    # 빈 줄일 경우 통과
    if line.strip() == "":
        continue
    # 영어를 한국어로 번역
    result = translator.translate(line, dest='ko')
    # 번역한 한국어를 파일로 저장
    fileContent = result.text + "\n"
    if (foutput is not None) and foutput.write(fileContent):
        # 진행율을 보여주기
        print(str(cnt) + " row" + " / " + str(totalcnt) +" row(s) fileContent write OK ")
    else:
        foutput.close
finput.close()