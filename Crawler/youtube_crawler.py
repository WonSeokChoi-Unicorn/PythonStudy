# 시스템 함수 sys를 import 한다.
import sys
# selenium에서 webdriver를 사용할 수 있게 webdriver를 import 한다.
# https://sites.google.com/a/chromium.org/chromedriver/home 
# 에서 크롬 버전에 맞는 크롬드라이버를 다운로드 후 Scripts 폴더로 복사하기
from selenium import webdriver
# BeautifulSoup4를 import 한다.
from bs4 import BeautifulSoup
# 날짜 시간 처리 위해 datetime, timedelta를 import 한다.
from datetime import datetime, timedelta
# iframe TAG 작성을 위해 yt를 import 한다. (pip install yt-iframe)
from yt_iframe import yt 
# 월, 년 단위 계산 위해서 relativedelta를 import 한다.
from dateutil.relativedelta import relativedelta
# 숫자만 추출하기 위한 re를 import 한다.
import re
# 파일 존재 여부 확인 위한 os를 import 한다.
import os
# lxml 설치 필요합니다 (pip install lxml)

# <p>채널명 [1번만 표시]</p><p>제목</p><p><a>URL</a></p><p><iframe></p> 로 작성

# 14F 일사에프 https://www.youtube.com/c/14FMBC/videos
# Kurzgesagt – In a Nutshell https://www.youtube.com/c/inanutshell/videos
# TED-Ed https://www.youtube.com/teded/videos
# Vox https://www.youtube.com/c/Vox/videos
# LG전자 https://www.youtube.com/c/LGElectronicsKorea/videos
# LG https://www.youtube.com/user/LGSTORY/videos
# 디즈니 https://www.youtube.com/c/DisneyMovieKr/videos
# MarvelKorea https://www.youtube.com/c/MarvelKorea/videos
# 리뷰엉이: Owl's Review https://www.youtube.com/c/Owlsreview/videos
# movie trip 무비트립 https://www.youtube.com/c/movietrip%EB%AC%B4%EB%B9%84%ED%8A%B8%EB%A6%BD/videos
# 고몽 https://www.youtube.com/user/rladndgussla/videos
# 천재이승국 GeniusSKLee https://www.youtube.com/c/GeniusSKLee/videos
# 은빛유니콘 https://www.youtube.com/channel/UCPq0i_bZeqVoVYm_u8qimDA/videos
# 엔스Ens https://www.youtube.com/channel/UC_Aly3X5CdojHdRDGmKi1ow/videos
# 가전주부 GJJB https://www.youtube.com/channel/UC5aNQ65ADb02zEJxzb_zmYQ/videos
# 멋진기영TV https://www.youtube.com/user/dlrldud1111/videos
# B Man 삐맨 https://www.youtube.com/c/BMan%EC%82%90%EB%A7%A8/videos
# 빨강도깨비 https://www.youtube.com/c/%EB%B9%A8%EA%B0%95%EB%8F%84%EA%B9%A8%EB%B9%84dokkebi/videos
# 발없는새 https://www.youtube.com/user/nofeetbird/videos
# sanggung상궁 https://www.youtube.com/c/sanggungtv/videos
# 엉삼 https://www.youtube.com/c/%EB%A6%AC%EB%B7%B0%EC%97%89%EC%9D%B4%EB%B6%81%EC%8A%A4/videos
# 오토뷰(Autoview) https://www.youtube.com/channel/UCfcgDLazgMa1L92Kl3r9ZAA/videos
# 한상기 오토프레스 Han Sang Ki https://www.youtube.com/c/%ED%95%9C%EC%83%81%EA%B8%B0HanSangKi/videos
# LikeRing https://www.youtube.com/channel/UC7A1QdDXcu3zu_KS8DddL1A/videos
# 사람사는세상노무현재단 https://www.youtube.com/c/%EC%82%AC%EB%9E%8C%EC%82%AC%EB%8A%94%EC%84%B8%EC%83%81%EB%85%B8%EB%AC%B4%ED%98%84%EC%9E%AC%EB%8B%A8/videos

# 추출할 유튜브 채널의 동영상 탭
urllist = [
           'https://www.youtube.com/c/14FMBC/videos',
           'https://www.youtube.com/c/inanutshell/videos',
           'https://www.youtube.com/teded/videos',
           'https://www.youtube.com/c/Vox/videos',
           'https://www.youtube.com/c/LGElectronicsKorea/videos',
           'https://www.youtube.com/user/LGSTORY/videos',
           'https://www.youtube.com/c/DisneyMovieKr/videos',
           'https://www.youtube.com/c/MarvelKorea/videos',
           'https://www.youtube.com/c/Owlsreview/videos',
           'https://www.youtube.com/c/movietrip%EB%AC%B4%EB%B9%84%ED%8A%B8%EB%A6%BD/videos',
           'https://www.youtube.com/user/rladndgussla/videos',
           'https://www.youtube.com/c/GeniusSKLee/videos',
           'https://www.youtube.com/channel/UCPq0i_bZeqVoVYm_u8qimDA/videos',
           'https://www.youtube.com/channel/UC_Aly3X5CdojHdRDGmKi1ow/videos',
           'https://www.youtube.com/channel/UC5aNQ65ADb02zEJxzb_zmYQ/videos',
           'https://www.youtube.com/user/dlrldud1111/videos',
           'https://www.youtube.com/c/BMan%EC%82%90%EB%A7%A8/videos',
           'https://www.youtube.com/c/%EB%B9%A8%EA%B0%95%EB%8F%84%EA%B9%A8%EB%B9%84dokkebi/videos',
           'https://www.youtube.com/user/nofeetbird/videos',
           'https://www.youtube.com/c/sanggungtv/videos',
           'https://www.youtube.com/c/%EB%A6%AC%EB%B7%B0%EC%97%89%EC%9D%B4%EB%B6%81%EC%8A%A4/videos',
           'https://www.youtube.com/channel/UCfcgDLazgMa1L92Kl3r9ZAA/videos',
           'https://www.youtube.com/c/%ED%95%9C%EC%83%81%EA%B8%B0HanSangKi/videos',
           'https://www.youtube.com/channel/UC7A1QdDXcu3zu_KS8DddL1A/videos',
           'https://www.youtube.com/c/%EC%82%AC%EB%9E%8C%EC%82%AC%EB%8A%94%EC%84%B8%EC%83%81%EB%85%B8%EB%AC%B4%ED%98%84%EC%9E%AC%EB%8B%A8/videos',
           'https://www.youtube.com/channel/UCjHn_Os5NoCXZyoXzuKth9w/videos'
          ]

# 전일 오전 7시
yesterday = datetime.today() - timedelta(days=1)
fromdate = datetime(yesterday.year, yesterday.month, yesterday.day, 7, 0, 0)

# 당일 오전 6시 59분 59초
todate = datetime(datetime.today().year, datetime.today().month, datetime.today().day, 6, 59, 59)

# 채널 리스트를 차례대로 불러옵니다.
for u in range(0, len(urllist)):
    # 로그를 없애는 설정
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # driver란 변수에 객체를 만들어 준다. chromedriver는 파이썬이 있는 경로에 두거나, 다른 경로에 두면 전체 경로명을 다 적어 줍니다.
    driver = webdriver.Chrome(executable_path='chromedriver', options=options)

    # 원하는 사이트의 url을 입력하여 사이트를 연다.
    driver.get(urllist[u])

    # body를 스크롤하기 위해 tagname이 body로 되어있는것을 추출합니다.
    body = driver.find_element_by_tag_name('body')

    # 로드 된 페이지 소스를 html이란 변수에 저장합니다.
    html = driver.page_source

    # html을 'lxml' parser를 사용하여 분석합니다.
    soup = BeautifulSoup(html, 'lxml')

    # channelname 조건에 맞는 모든 div 태그의 hidden style-scope paper-tooltip class들을 가져옵니다. 2021.02.23 웹사이트 변경
    allchannelname = soup.find_all('div', 'hidden style-scope tp-yt-paper-tooltip')

    # channelname 변수에 저장합니다.
    # 2021.03.25 [6] -> [7] 로 변경
    # 2021.08.03 [7] -> [6] 로 변경
    channelname = [soup.find_all('div','hidden style-scope tp-yt-paper-tooltip')[6].string for n in range(0,len(allchannelname))]

    # 채널명에 줄 바꿈이 있어서 제거합니다.
    for i in range(len(channelname)):
        channelname[i] = channelname[i].replace("\n", "")

    # title 조건에 맞는 모든 a 태그의 class들을 가져옵니다.
    all_title = soup.find_all('a','yt-simple-endpoint style-scope ytd-grid-video-renderer')

    # title이란 변수에 저장합니다.
    title = [soup.find_all('a','yt-simple-endpoint style-scope ytd-grid-video-renderer')[n].string for n in range(0,len(all_title))]

    # href 조건에 맞는 모든 a 태그의 id들을 가져옵니다.
    all_url = soup.find_all('a', {'id':'video-title'})

    # firsturl이란 변수에 저장합니다.
    firsturl = [soup.find_all('a', {'id':'video-title'})[n].get('href') for n in range(0,len(all_url))]

    # time 조건에 맞는 모든 span 태그의 class들을 가져옵니다. title, url의 2배수.
    all_time = soup.find_all('span','style-scope ytd-grid-video-renderer')

    # time이란 변수에 시간 정보(짝수)를 저장합니다.
    # 분 전, 시간 전, 일 전, 주 전, 개월 전, 년 전
    time = [all_time[n].text for n in range(1,len(all_time),2)]

    # iframe 태그 생성을 위해 폭과 높이를 설정
    width = '560' # (Optional)
    height = '315' # (Optional)

    # 파일명을 날짜로 이용하기 위해 글로벌로 이동
    nowDate = datetime.now()

    if os.path.isfile(nowDate.strftime('%Y-%m-%d') + '_youtube.txt'):
        # 파일이 존재할 경우 추가, 파일 작성 시간이 길어져서 년월일로 파일명 생성
        f = open(nowDate.strftime('%Y-%m-%d') + '_youtube.txt', mode='at', encoding='utf-8')
    else:
        # 파일이 존재하지 않을 경우 생성, 파일 작성 시간이 길어져서 년월일로 파일명 생성
        f = open(nowDate.strftime('%Y-%m-%d') + '_youtube.txt', mode='wt', encoding='utf-8')

    # 채널명은 반복문 전 파일에 1번만 저장하도록 
    channelheader = "<p>" + channelname[0] + "</p>"
    channelheader += "\n"

    print("##################################################################")
    print(channelname[0])
    print("##################################################################")

    fileContent = channelheader

    if (f is not None) and f.write(fileContent):
        print("fileContent write OK ")

    # 화면에 로드된 동영상 갯수만큼
    for x in range(0, len(time)-1):

        delta = ''          # 개월, 년 차이 초기화
        fileContent = ""    # fileContent 초기화
        utubeKey = ""       # 유튜브 키값 초기화
        url = ""            # url 초기화
        iframe = ""         # iframe 초기화
        tempstr = ""        # 임시 저장 초기화

        if '분 전' in time[x]:
            # 분일 경우 작성 시간 확인
            timenumber = re.findall("\d+", time[x])
            writetime = datetime.today() - timedelta(minutes=int(timenumber[0]))
        elif '시간 전' in time[x]:
            # 시간일 경우 작성 시간 확인
            timenumber = re.findall("\d+", time[x])
            writetime = datetime.today() - timedelta(hours=int(timenumber[0]))
        elif '일 전' in time[x]:
            # 일일 경우 작성 시간 확인
            timenumber = re.findall("\d+", time[x])
            writetime = datetime.today() - timedelta(days=int(timenumber[0]))
        elif '주 전' in time[x]:
            # 주일 경우 작성 시간 확인
            timenumber = re.findall("\d+", time[x])
            writetime = datetime.today() - timedelta(weeks=int(timenumber[0]))
        elif '개월 전' in time[x]:
            # 개월일 경우 작성 시간 확인
            timenumber = re.findall("\d+", time[x])
            delta = relativedelta(months=int(timenumber[0]))
            writetime = datetime.today() - delta
        elif '년 전' in time:
            # 년일 경우 작성 시간 확인
            timenumber = re.findall("\d+", time[x])
            delta = relativedelta(years=int(timenumber[0]))
            writetime = datetime.today() - delta

        # 2021.10.28 shorts 영상에 대한 처리 추가
        if "/shorts/" in firsturl[x]:
            # 유튜브 Video ID 추출
            utubeKey = firsturl[x][8 : 8 + 11]
            # 유튜브 URL 만들기
            url = 'https://www.youtube.com/shorts/' + str(utubeKey)
            # iframe 태그 생성 - 아직 라이브러리가 없어서 수동 처리
            iframe = '<iframe width="315" height="560" src="https://www.youtube.com/embed/' + str(utubeKey) + '" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
        else:
            # 유튜브 Video ID 추출
            utubeKey = firsturl[x][9 : 9 + 11]
            # 유튜브 URL 만들기
            url = 'https://www.youtube.com/watch?v=' + str(utubeKey)
            # iframe 태그 생성
            iframe = yt.video(url, width=width, height=height)

        if(writetime > todate):
            print("작성 대상 아님 (당일 7시 이후)")
            print(title[x])
            print(url)
            print(writetime)
            pass
        elif writetime <= fromdate:
            print("작성 대상 아님 (전일 7시 이전)")
            print(title[x])
            print(url)
            print(writetime)            
        else:
            print("작성 대상 맞음 (전일 7시 ~ 당일 6시 59분 59초)")
            print(title[x])
            print(url)
            print(writetime)

            # 태그들은 임시 변수에 저장
            tempstr = "<p>" + title[x] + "</p>" # 게시글 제목 앞에 <p> 추가, 제목 뒤에 </p> 추가. 2021.01.03 추가
            tempstr += "\n"
            tempstr += '<p><a target=_blank href="' + url + '">' + url + '</a></p>'
            tempstr += "\n"
            tempstr += "<p>" + iframe + "</p>"
            tempstr += "\n"

            # 파일에 저장 (계속)
            fileContent += tempstr
            
            if (f is not None) and f.write(fileContent):
                print("fileContent write OK ")
            else:
                f.close

    # webdriver를 종료한다.
    driver.close()