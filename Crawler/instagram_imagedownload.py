
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# 파일 존재 여부 확인 위한 os를 import 한다.
import os
from datetime import datetime
import urllib.request
import time
# 오늘 날짜를 YYYYMMDD 형태로 변경
todaytime = datetime.today().strftime('%Y%m%d%H%M')

# 폴더 생성
def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")
# image 저장할 경로
savepath = "C:\\temp\\" + todaytime + "_instagram\\"
# image 저장할 경로 체크 및 생성
createDirectory(savepath)

options = webdriver.ChromeOptions()
# 로그를 없애는 설정
options.add_experimental_option("excludeSwitches", ["enable-logging"])
# 크롬 브라우저 안 보이게
options.add_argument('headless')

# 이미지를 저장할 인스타그램 URL들
urls = [
        'https://www.instagram.com/p/Cb1yIBlOpvH/',
        'https://www.instagram.com/p/Cc9uFA_DkQB/'
       ]
for url in urls:
    # 웹드라이버 실행
    browser = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)
    # url 만들기
    urlload = "https://instadownloader.co/ko/#url=" + url
    # url 로드
    browser.get(urlload)
    # 다운로드 클릭
    browser.find_element_by_css_selector("#send").click()
    time.sleep(5)
    # 로드 된 페이지 소스를 html이란 변수에 저장합니다.
    Html = browser.page_source
    # HTML을 'lxml(XML, HTML 처리)'를 사용하여 분석
    Soup = BeautifulSoup(Html, 'lxml')
    # 다운로드 수집
    downloads = Soup.find_all('a', 'btn btn-warning btn-download')
    # 카운트 설정
    cnt = 1
    # / 위치 파악
    poslist = [pos for pos, char in enumerate(url) if char == "/"]
    # 파일명 접두어 만들기
    fileprefix = url[poslist[-2] + 1 : -1] + "_"
    # 다운로드들 확인하여 이미지로 저장
    for download in downloads:        
        # 이미지 파일명
        imagesave = savepath + fileprefix + str(cnt) + ".jpg"
        # 이미지 저장
        urllib.request.urlretrieve(download['href'], imagesave)
        # 카운트 증가
        cnt += 1
    # 웹드라이버 종료
    browser.quit()