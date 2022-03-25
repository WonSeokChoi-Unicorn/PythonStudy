import requests
import urllib.request
from bs4 import BeautifulSoup
# 파일 존재 여부 확인 위한 os를 import 한다.
import os

# 폴더 생성
def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")
# image 저장할 경로
savepath = "C:\\temp\\image\\"
# image 저장할 경로 체크
createDirectory(savepath)
# image 파일명
savefile = "WebImages_"
# 주소
URL = "http://unicornworld.org"
# 봇 방지 웹사이트 회피
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
# 주소 요청 및 응답 수신
Res = requests.get(URL, headers=headers)
# HTTP 응답 성공 200
if Res.status_code == 200:        
    # HTML 받기 
    Html = Res.text
    # lxml으로 parsing
    Soup = BeautifulSoup(Html, 'lxml')
    # img tag 수집
    imglist = Soup.find_all('img')
    # 파일명용 카운트
    cnt = 1
    # 수집된 img tag 확인
    for img in imglist:
        # 마지막 . 위치 파악
        imgdot = [ i for i, dot in enumerate(img['src']) if dot == '.']
        # 확장자 가져오기
        imgext = img['src'][imgdot[-1] :]
        # 저장할 파일명(경로 포함)
        imagesave = savepath + savefile + str(cnt) + imgext
        # image를 파일로 저장
        urllib.request.urlretrieve(img['src'], imagesave)
        # 카운트 증가
        cnt += 1
        # 파일명 출력
        print(imagesave)

# 원치 않는 이미지가 나올 경우 범위를 좁히거나 예외 처리하는 절차가 필요