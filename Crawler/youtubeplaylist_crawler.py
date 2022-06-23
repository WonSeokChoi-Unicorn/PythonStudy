# 에서 크롬 버전에 맞는 크롬드라이버를 다운로드 후 Scripts 폴더로 복사하기
from selenium import webdriver
# BeautifulSoup4를 import 한다.
from bs4 import BeautifulSoup
# iframe TAG 작성을 위해 yt를 import 한다. (pip install yt-iframe)
from yt_iframe import yt
# 파일 존재 여부 확인 위한 os를 import 한다.
import os
import pandas as pd
import time
# 날짜 시간 처리 위해 datetime를 import 한다.
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Dataframe 선언
pldf = pd.DataFrame(columns=['Date', 'URL'])

youtubeplaylists = [
"https://www.youtube.com/playlist?list=PL3Eb1N33oAXijqFKrO83hDEN0HPwaecV3"
                   ]
# 파일명을 날짜로 이용하기 위해 글로벌로 이동
nowDate = datetime.now()

# 파일에 저장 (시작)
if os.path.isfile(nowDate.strftime('%Y-%m-%d') + '_youtubeplaylist.txt'):
    # 파일이 존재할 경우 추가, 파일 작성 시간이 길어져서 년월일로 파일명 생성
    fw = open(nowDate.strftime('%Y-%m-%d') + '_youtubeplaylist.txt', mode='at', encoding='utf-8')
else:
    # 파일이 존재하지 않을 경우 생성, 파일 작성 시간이 길어져서 년월일로 파일명 생성
    fw = open(nowDate.strftime('%Y-%m-%d') + '_youtubeplaylist.txt', mode='wt', encoding='utf-8')

options = webdriver.ChromeOptions()
# 로그를 없애는 설정
options.add_experimental_option("excludeSwitches", ["enable-logging"])
# 크롬 브라우저 안 보이게
# options.add_argument('headless')
# driver란 변수에 객체를 만들어 준다. chromedriver는 파이썬이 있는 경로에 두거나, 다른 경로에 두면 전체 경로명을 다 적어 줍니다.
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)
# 검색할 패턴을 . 으로 선언
searchpattern1 = "."

def infinite_loop():
    # 최초 페이지 스크롤 설정
    # 스크롤 시키지 않았을 때의 전체 높이
    last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        # 윈도우 창을 0에서 위에서 설정한 전체 높이로 이동
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(1)
        # 스크롤 다운한 만큼의 높이를 신규 높이로 설정 
        new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        # 직전 페이지 높이와 신규 페이지 높이 비교
        if new_page_height == last_page_height:
            time.sleep(1)
            # 신규 페이지 높이가 이전과 동일하면, while문 break
            if new_page_height == driver.execute_script("return document.documentElement.scrollHeight"):
                break
        else:
            last_page_height = new_page_height

# 유튜브 URLS
youtubeurls = []
def crawlingurlcollect():
    # 로드 된 페이지 소스를 html이란 변수에 저장합니다.
    plHtml = driver.page_source
    time.sleep(3)
    # html을 'lxml' parser를 사용하여 분석합니다.
    plSoup = BeautifulSoup(plHtml, 'lxml')
    # 유튜브 a tag 가져오기
    youtubealists = plSoup.find_all('a', 'yt-simple-endpoint style-scope ytd-playlist-video-renderer')
    # 유튜브 a tag에서 url 완성하기
    for youtubealist in youtubealists:
        # href 가져오기
        youtubehref = youtubealist['href']
        # video key 추출
        startpos = youtubehref.index("v=")
        endpos = youtubehref.index("&")
        youtubekey = youtubehref[startpos + 2 : endpos]
        # 유튜브 URL 만들기
        youtubeurl = 'https://www.youtube.com/watch?v=' + youtubekey
        # 유튜브 URLS에 추가
        youtubeurls.append(youtubeurl)

def crawlingiframemake():
    global pldf
    for listurl in youtubeurls:
        # 원하는 사이트의 url을 입력하여 사이트를 연다.
        driver.get(listurl)
        time.sleep(3)
        # 로드 된 페이지 소스를 html이란 변수에 저장합니다.
        iframeHtml = driver.page_source
        # html을 'lxml' parser를 사용하여 분석합니다.
        iframeSoup = BeautifulSoup(iframeHtml, 'lxml')
        # 날짜 가져오기
        dateinfo = iframeSoup.find_all('yt-formatted-string', 'style-scope ytd-video-primary-info-renderer')
        # 텍스트로 변환
        dateinfotext = dateinfo[1].get_text().strip()
        # . 위치 저장할 리스트 선언(초기화)
        searchpattern1list = []
        # . 위치 파악
        searchpattern1list = [pos for pos, char in enumerate(dateinfotext) if char == searchpattern1]
        # 연도
        dateYYYY = dateinfotext[:searchpattern1list[0]]
        # 월
        dateMM = "{:0>2}".format(dateinfotext[searchpattern1list[0] + 1 : searchpattern1list[1]].strip())
        # 일
        dateDD = "{:0>2}".format(dateinfotext[searchpattern1list[1] + 1 : searchpattern1list[2]].strip())
        # 전체 날짜
        dateYYYYMMDD = dateYYYY + dateMM + dateDD
        # Dataframe에 추가
        pldf = pldf.append({'Date' : dateYYYYMMDD, 'URL' : listurl}, ignore_index=True)
    # 날짜 오름차순으로 정렬
    pldf = pldf.sort_values(by=['Date'])
    # 5개마다 글 게시 위한 카운트
    cnt = 1
    # iframe 태그 생성을 위해 폭과 높이를 설정
    width = '560'
    height = '315'
    for tempdf in pldf.itertuples():
        # 초기화
        utubeKey = ""
        iframe = ""
        fileContent = ""
        tempstr = ""
        # URL 가져오기
        realurl = tempdf.URL
        # 원하는 사이트의 url을 입력하여 사이트를 연다.
        driver.get(realurl)
        time.sleep(3)
        # 로드 된 페이지 소스를 html이란 변수에 저장합니다.
        realHtml = driver.page_source
        # html을 'lxml' parser를 사용하여 분석합니다.
        realSoup = BeautifulSoup(realHtml, 'lxml')
        # 제목 조건에 맞는 모든 div 태그의 ytp-title-text class들을 가져옵니다.
        title = realSoup.find('title').get_text()
        # " - YouTube"를 삭제 처리
        title = title.replace(" - YouTube", "") + " - " + tempdf.Date[0:3 + 1] + "/" + tempdf.Date[4:5 + 1] + "/" + tempdf.Date[6:7 + 1]
        # url 길이에 따라서 Video ID 추출하는 방법 구분
        if len(realurl) == 43:
            utubeKey = realurl[32 : 32 + 11]
        elif len(realurl) == 39:
            utubeKey = realurl[28 : 28 + 11]
        elif len(realurl) == 28:
            utubeKey = realurl[17 : 17 + 11]
        # 유튜브 URL 만들기
        url = 'https://www.youtube.com/watch?v=' + str(utubeKey)
        # iframe 태그 생성
        iframe = yt.video(url, width = width, height = height)

        tempstr = "<p>" + title + "</p>"
        tempstr += "\n"
        tempstr += '<p><a target=_blank href="' + url + '">' + url + '</a></p>'
        tempstr += "\n"
        tempstr += "<p>" + iframe + "</p>"
        tempstr += "\n"

        # 파일에 저장 (계속)
        fileContent = tempstr
        
        if (fw is not None) and fw.write(fileContent):
            print("fileContent write OK ")
        else:
            fw.close

def run(url):
    # 원하는 사이트의 url을 입력하여 사이트를 연다.
    driver.get(url)
    time.sleep(3)
    # 무한 스크롤 다운
    infinite_loop()
    # 크롤링 - url 수집
    crawlingurlcollect()

# 플레이리스트들에 대해서 처리
for youtubeplaylist in youtubeplaylists:
    run(youtubeplaylist)

# 크롤링 - iframe 생성
crawlingiframemake()

# webdriver를 종료한다.
driver.quit()