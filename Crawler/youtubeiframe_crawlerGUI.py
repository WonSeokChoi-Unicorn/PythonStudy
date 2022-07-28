# selenium에서 webdriver를 사용할 수 있게 webdriver를 import 한다.
# https://sites.google.com/chromium.org/driver/
# 에서 크롬 버전에 맞는 크롬드라이버를 다운로드 후 Scripts 폴더로 복사하기
from selenium import webdriver
# find_element 사용 위해서 import
from selenium.webdriver.common.by import By
# BeautifulSoup4를 import 한다.
from bs4 import BeautifulSoup
# iframe TAG 작성을 위해 yt를 import 한다. (pip install yt-iframe)
from yt_iframe import yt
# 파일 존재 여부 확인 위한 os를 import 한다.
import os
# 날짜 시간 처리 위해 datetime를 import 한다.
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
import sys

def crawling():
    # 유튜브 URL 정리한 텍스트 파일을 한 줄씩 읽어 옵니다
    # 경로에 기본 확장 문자(escape sequence)를 피하기 위해서 역슬래시를 2개 사용
    fr = open("D:\\youtubeurl.txt", 'r')
    # 한 줄씩 읽기
    lines = fr.readlines()

    # 파일명을 날짜로 이용하기 위해 글로벌로 이동
    nowDate = datetime.now()

    # 파일에 저장 (시작)
    if os.path.isfile(nowDate.strftime('%Y-%m-%d') + '_youtubeonce.txt'):
        # 파일이 존재할 경우 추가, 파일 작성 시간이 길어져서 년월일로 파일명 생성
        fw = open(nowDate.strftime('%Y-%m-%d') + '_youtubeonce.txt', mode='at', encoding='utf-8')
    else:
        # 파일이 존재하지 않을 경우 생성, 파일 작성 시간이 길어져서 년월일로 파일명 생성
        fw = open(nowDate.strftime('%Y-%m-%d') + '_youtubeonce.txt', mode='wt', encoding='utf-8')

    options = webdriver.ChromeOptions()
    # 로그를 없애는 설정
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # 크롬 브라우저 안 보이게
    options.add_argument('headless')
    # driver란 변수에 객체를 만들어 준다. chromedriver는 파이썬이 있는 경로에 두거나, 다른 경로에 두면 전체 경로명을 다 적어 줍니다.
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)

    for line in lines:
        utubeKey = ""       # 유튜브 키값 초기화
        url = ""            # url 초기화
        iframe = ""         # iframe 초기화
        fileContent = ""    # fileContent 초기화
        tempstr = ""        # 임시 저장 초기화

        # iframe 태그 생성을 위해 폭과 높이를 설정
        width = '560' # (Optional)
        height = '315' # (Optional)

        # 빈 줄일 경우 통과
        if line.strip() == "":
            continue

        # line의 공백 제거
        line = line.strip()

        # 원하는 사이트의 url을 입력하여 사이트를 연다.
        driver.get(line)

        # body를 스크롤하기 위해 tagname이 body로 되어있는것을 추출합니다.
        body = driver.find_element(By.TAG_NAME, 'body')
        # body = driver.find_element_by_tag_name('body')

        # 로드 된 페이지 소스를 html이란 변수에 저장합니다.
        html = driver.page_source

        # html을 'lxml' parser를 사용하여 분석합니다.
        soup = BeautifulSoup(html, 'lxml')

        # 제목 조건에 맞는 모든 div 태그의 ytp-title-text class들을 가져옵니다.
        title = soup.find('title').get_text()

        # " - YouTube"를 삭제 처리
        title = title.replace(" - YouTube", "")
        window.textBrowser.append("####################################################################################################################################")
        window.textBrowser.append(title)
        window.textBrowser.append("####################################################################################################################################")

        # url 길이에 따라서 Video ID 추출하는 방법 구분
        if len(line) == 43:
            utubeKey = line[32 : 32 + 11]
        elif len(line) == 39:
            utubeKey = line[28 : 28 + 11]
        elif len(line) == 28:
            utubeKey = line[17 : 17 + 11]

        # 유튜브 URL 만들기
        url = 'https://www.youtube.com/watch?v=' + str(utubeKey)
        # iframe 태그 생성
        iframe = yt.video(url, width=width, height=height)

        tempstr = "<p>" + title + "</p>"
        tempstr += "\n"
        tempstr += '<p><a target=_blank href="' + url + '">' + url + '</a></p>'
        tempstr += "\n"
        tempstr += "<p>" + iframe + "</p>"
        tempstr += "\n"

        # 파일에 저장 (계속)
        fileContent = tempstr
        
        if (fw is not None) and fw.write(fileContent):
            window.textBrowser.append("fileContent write OK ")
        else:
            fw.close
    # webdriver를 종료한다.
    driver.quit()
    fr.close()
#파일 경로
#pyinstaller로 원파일로 압축할때 경로 필요함
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
# 앱 선언
app = QApplication(sys.argv)
# UI 파일 선언
ui_file = QFile(resource_path(".\\youtubeiframe_crawlerGUI.ui"))
# UI 파일 열기
ui_file.open(QFile.ReadOnly)
# UI 로더 선언
loader = QUiLoader()
# UI 로더로 UI 파일 로드
window = loader.load(ui_file)
# 앱 제목
window.setWindowTitle("Youtube URL to iframe Program")
# 앱 해상도
window.resize(1024,768)
# 버튼
window.pushButton.clicked.connect(crawling)
# UI 파일 닫기
ui_file.close()
# 앱 실행
window.show()
# 앱 종료
sys.exit(app.exec_())