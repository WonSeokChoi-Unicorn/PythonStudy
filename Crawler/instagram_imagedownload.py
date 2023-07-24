
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
# 파일 존재 여부 확인 위한 os를 import 한다.
import os
from datetime import datetime
import urllib.request
import time
from user_agent import generate_user_agent
import re

# 오늘 날짜를 YYYYMMDD 형태로 변경
todaytime = datetime.today().strftime('%Y%m%d%H%M')

# 폴더 생성
def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

# 정규 표현식 패턴을 사용하여 "B-ouuLwDjy8"을 추출합니다.
pattern = r"/p/([A-Za-z0-9_-]+)/"

# 차단 당하지 않기 위한 대기 시간
waittime = 10
options = webdriver.ChromeOptions()
# 로그를 없애는 설정
options.add_experimental_option("excludeSwitches", ["enable-logging"])
# 크롬 브라우저 안 보이게
options.add_argument('headless')

# 이미지를 저장할 인스타그램 URL들
urls = [
        'https://www.instagram.com/p/B-ouuLwDjy8/?utm_source=ig_web_button_share_sheet'
       ]
# 웹드라이버 실행
browser = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)
# url 만들기
urlload = "https://sssinstagram.com/ko"
# url 로드
browser.get(urlload)
time.sleep(waittime)
for url in urls:
    # 정규 표현식 패턴을 사용하여 고유ID를 추출합니다.
    match = re.search(pattern, url)
    post_id = match.group(1)
    # image 저장할 경로
    savepath = "C:\\temp\\" + todaytime + "_" + post_id + "\\"
    # image 저장할 경로 체크 및 생성
    createDirectory(savepath)
    # 주소란에 입력
    browser.find_element(By.CSS_SELECTOR, "#main_page_text").send_keys(url)
    time.sleep(waittime)
    # 다운로드 클릭
    browser.find_element(By.CSS_SELECTOR, "#submit").click()
    time.sleep(waittime)
    # 로드 된 페이지 소스를 html이란 변수에 저장합니다.
    Html = browser.page_source
    # HTML을 'lxml(XML, HTML 처리)'를 사용하여 분석
    Soup = BeautifulSoup(Html, 'lxml')
    # 다운로드 수집
    downloads = Soup.find_all('div', 'download-wrapper')
    # 카운트 설정
    cnt = 1
    # 다운로드들 확인하여 이미지로 저장
    for download in downloads:
        # IMG 태그 찾기
        imgsrc = download.find('a')
        # 이미지 파일명
        imagesave = savepath + post_id + "_" + str(cnt) + ".jpg"
        # 403 forbidden 회피 객체
        opener = urllib.request.URLopener()
        # 403 forbidden 회피 객체 헤더 추가
        opener.addheader('User-Agent', generate_user_agent(device_type = 'desktop'))
        # 진행
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ", " + str(downloads.index(download) + 1) + "/" + str(len(downloads)) + ", " + imgsrc['href'])
        # 이미지 저장
        opener.retrieve(imgsrc['href'], imagesave)
        # 카운트 증가
        cnt += 1
# 웹드라이버 종료
browser.quit()