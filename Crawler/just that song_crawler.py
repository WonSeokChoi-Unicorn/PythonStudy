
from bs4 import BeautifulSoup
# 파일 존재 여부 확인 위한 os를 import 한다.
import os
from datetime import datetime, timedelta
import requests
# 숫자만 추출하기 위한 re를 import 한다.
import re
import pandas as pd
import time
from wcwidth import wcswidth
# pip install progressbar
import progressbar
# 오늘 날짜를 YYYYMMDD 형태로 변경
todaytime = datetime.today().strftime('%Y%m%d%H%M')
# 폴더 생성
def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")
# Excel 저장할 경로
savepath = "C:\\temp\\JustThatSong\\"
# Excel 저장할 경로 체크 및 생성
createDirectory(savepath)
# Dataframe 컬럼에 이름 설정
dataname = ["날짜시간", "프로그램 명", "노래 명", "가수 명"]
# Dataframe 선언
justthatsongdf = pd.DataFrame(columns = dataname)
# TV/RADIO url
justthatsongurls = [
"https://search.daum.net/search?w=tot&q=TV+%EB%B0%B0%EA%B2%BD%EC%9D%8C%EC%95%85&DA=BGM&rtmaxcoll=BGM",
"https://search.daum.net/search?w=tot&q=%EB%9D%BC%EB%94%94%EC%98%A4%20%EC%84%A0%EA%B3%A1%ED%91%9C&DA=BGM&rtmaxcoll=BGM"
                   ]
# 봇 방지 웹사이트 회피
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
# Excel 파일명
writer = pd.ExcelWriter(savepath + todaytime + "_JustThatSonglists.xlsx", engine='xlsxwriter')
# 진행 상황 객체 생성
bar = progressbar.ProgressBar()
# URL 처리
for justthatsongurl in bar(justthatsongurls):    
    # 페이지 요청 및 응답 수신
    main = requests.get(justthatsongurl, headers=headers)
    # HTML로 받기
    html = main.text
    # HTML을 'lxml(XML, HTML 처리)'를 사용하여 분석
    Soup = BeautifulSoup(html, 'lxml')
    # TV 방금 그 곡 리스트
    song = Soup.find('ul', 'list_song')
    # TV 방금 그 곡 리스트 (상세)
    songlists = song.find_all('li')
    # 시간, 프로그램명, 노래명, 가수명 확인
    for songlist in songlists:
        # 시간
        publishtime = songlist.find('em','txt_time').text
        if '분 전' in publishtime:
            # 분일 경우 작성 시간 확인
            timenumber = re.findall("\d+", publishtime)
            writetime = datetime.today() - timedelta(minutes=int(timenumber[0]))
        elif '초 전' in publishtime:
            # 초일 경우 작성 시간 확인
            timenumber = re.findall("\d+", publishtime)
            writetime = datetime.today() - timedelta(seconds=int(timenumber[0]))
        # 프로그램명
        programname = songlist.find('span','txt_ellip')
        # 노래명
        songname = songlist.find('strong','tit_song')
        # 가수명
        singername = songlist.find('dd','cont')
        # "날짜시간", "프로그램 명", "노래 명", "가수 명"
        justthatsongdf = justthatsongdf.append({'날짜시간' : writetime.strftime('%Y-%m-%d %H:%M:%S'),\
                                                '프로그램 명' : programname.get_text(),\
                                                '노래 명' : songname.get_text(),\
                                                '가수 명' : singername.get_text()}, ignore_index=True)
    # 대기
    time.sleep(3)
# Dataframe을 Excel로
justthatsongdf.to_excel(writer, index = False)
# Excel 컬럼 폭 자동 조절
for column in justthatsongdf:
    collist = justthatsongdf[column].astype(str).values
    maxcollen = 0
    for col in collist:
        collen = wcswidth(col)
        if maxcollen < collen:
            maxcollen = collen
    column_width = max(maxcollen, len(column.encode()))
    col_idx = justthatsongdf.columns.get_loc(column)
    writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_width)
# Excel 저장
writer.save()