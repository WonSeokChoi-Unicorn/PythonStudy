import requests
import time
import sys
from bs4 import BeautifulSoup
from bs4 import NavigableString
from datetime import datetime, timedelta
# pip install user-agent
from user_agent import generate_user_agent
import html
import cv2
import re

# 오늘 날짜를 YYYYMMDDHHMMSS 형태로 변경
todaytime = datetime.today().strftime('%Y%m%d%H%M%S')
# 시간을 HH 형태로 변경
todaytimeHH = datetime.today().strftime('%H')

# 실행 과정을 기록할 파일
runlog = open('D:\\Python\LOG\\' + todaytime + '_ggoorr_output.txt', 'w', encoding = 'utf-8')
# 정상 실행
# sys.stdout = runlog
# 실행 오류
# sys.stderr = runlog
# 전역 변수 설정
# 꾸르 메인 주소
GGOORR_MAIN_URL = "https://ggoorr.net"
# 꾸르 상세 주소
GGOORR_DETAIL_URL = 'https://ggoorr.net/index?page='
# 에러 발생 URL 모음
errorurls = []
# 파일 변수 글로벌로 이동
nowDate = datetime.now()
# 파일 작성 시간이 길어져서 년월일로 파일명 생성
f = open(nowDate.strftime('%Y-%m-%d') + '_ggoorr.txt', mode = 'wt', encoding = 'utf-8')
# 전체 컨텐츠가 저장되는 dictionary
contentDictionary = {}
# 전체 컨텐츠가 sort 되어 저장되는 dictionary
sortedKeyList = {}
# 대기 시간
waittime = 0.5
# 게시글 url 리스트
detailUrllist = []

# 숫자를 추출하기 위한 정규 표현식
regex1  = r"\d+"
# "embed/" 다음에 있는 유튜브 키값 추출을 위한 정규 표현식
regex2 = r"embed/([a-zA-Z0-9_-]+)"

# 상세 게시글 HTML 수집 함수
def getDetail(detailUrl, option):
    # 2022.12.06 게시글 순번으로 sort
    # 2023.07.10 수정
    # realwritetime = detailUrl[23:detailUrl.index("?")]
    match1 = re.search(regex1, detailUrl)
    if match1:
        realwritetime = match1.group()
    try:
        # 봇 방지 웹사이트 회피
        headers = {'User-Agent': generate_user_agent(device_type = 'desktop') }
        # 상세 주소 요청 및 응답 수신
        detailRes = requests.get(detailUrl, headers = headers)
    except:
        print(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ", 오류가 발생했습니다." + detailUrl)
        # 오류가 발생하면 errorurl에 추가
        errorurls.append(detailUrl)
        return False

    # HTTP 응답 성공 200
    if detailRes.status_code == 200:        
        # 게시글의 HTML을 받아 BeautifulSoup 로 파싱 저장 
        detailHtml = detailRes.text
        # HTML을 'lxml(XML, HTML 처리)'를 사용하여 분석
        detailSoup = BeautifulSoup(detailHtml, 'lxml')
        # 제목
        title = detailSoup.find('h1', attrs = {"class" : "np_18px"}).get_text().strip()
        # 작성 날짜/시간
        writetimetemp = detailSoup.find('time', attrs = {"class" : "date m_no"}).get_text().strip()
        writetime = datetime(int(writetimetemp[:3 + 1]), int(writetimetemp[5:6 + 1]), int(writetimetemp[8:9 + 1]), int(writetimetemp[11:12 + 1]), int(writetimetemp[14:15 + 1]), 0)

        # 2023.07.21 실행 시간에 따라서 기준(시작~종료) 시간을 변경
        if todaytimeHH >= '15':
            # 당일 오전 7시
            fromdate = datetime(datetime.today().year, datetime.today().month, datetime.today().day, 7, 0, 0)

            # 내일 오전 6시 59분 59초
            tomorrow = datetime.today() + timedelta(days = 1)
            todate = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 6, 59, 59)
        else:
            # 전일 오전 7시
            yesterday = datetime.today() - timedelta(days = 1)
            fromdate = datetime(yesterday.year, yesterday.month, yesterday.day, 7, 0, 0)

            # 당일 오전 6시 59분 59초
            todate = datetime(datetime.today().year, datetime.today().month, datetime.today().day, 6, 59, 59)

        # 진행
        print(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + " - " + title + " - " + detailUrl)

        # 옵션이 Y인경우 기준대로 작성 대상 확인
        if option == 'Y':
            # 처리
            if (writetime > todate):
                print(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ", 작성 대상 아님 (" + todate.strftime('%Y-%m-%d %H:%M:%S') + " 이후)")
                return
            elif (writetime < fromdate):
                print(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ", 작성 대상 아님 - (" + fromdate.strftime('%Y-%m-%d %H:%M:%S') + " 이전)")
                return
            else:
                print(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ", 작성 대상 맞음 (" + fromdate.strftime('%Y-%m-%d %H:%M:%S') + " ~ " + todate.strftime('%Y-%m-%d %H:%M:%S') + ")")

        # 본문을 찾기 위해 article 태그의 데이터만 사용함
        articleBody = detailSoup.find('article')

        # 문자열로 변환
        articleBodyText = str(articleBody)

        # 2021.06.29 제외되는 게시글들을 URL로 저장
        # gifmp4_video class가 있을 경우
        articleBodyGIFText2 = articleBodyText.find("gifmp4_video")

        # 링크로 보여줘야 되는 것들에 대한 처리
        if articleBodyGIFText2 > 0:
            print(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ", replace with link")
            # 파일에 저장
            fileContent = "<br><br></br></br><p>" + title + "</p>" # 게시글 제목 앞에 <p> 추가, 제목 뒤에 </p> 추가. 2021.01.03 추가
            fileContent += "\n"
            fileContent += "\n" + '<a target=_blank href="' + detailUrl + '">' + detailUrl + "</a>" + "\n"
            fileContent += "\n" + "<br><br></br></br>" + "\n"
            # realwritetime을 key로해서 html코드를 value로 저장
            contentDictionary[realwritetime] = fileContent
            return

        # 게시글 머릿말/꼬리말 설정
        articleHeader = '<article><div id="article_1"><div>'
        articleTail = '</div></div></article>'
 
        # 01 게시글 앞에 머릿말 추가
        articleString = articleHeader

        # 20233.07.10 유튜브 키 리스트 초기화
        youtubekeylist = []

        # 02 article 태그 안에서 <p>태그들을 찾아서 저장함
        # p 로 처리하는 방식에서 문제가 많아 child 방식으로 변경
        for pLine in articleBody.div.div.children:

            # 2023.03.21 video height 속성 삭제
            try:
                if pLine.name == "video":
                    del pLine['height']
            except:
                pass
            # 2023.03.21 video width 속성 삭제 후 100%로 설정
            try:
                if pLine.name == "video":
                    del pLine['width']
                    # width를 100%로 설정
                    pLine['width'] = '100%'
            except:
                pass
            # 2023.08.21 video width 속성 삭제 후 100%로 설정
            try:
                pLinevideo = pLine.find('video')
                if not pLinevideo.has_attr('width'):
                    pLinevideo['width'] = '100%'
                else:
                    pLinevideo['width'] = '100%'
            except:
                pass
            # 2023.04.25 video style 속성 삭제
            try:
                if pLine.name == "video":
                    del pLine['style']
            except:
                pass

            try:
                # tag 없는 일반 문자열만 있을 경우 .select() 실행시 오류 발생하여 분기 처리
                if isinstance(pLine, NavigableString):
                    pLine = "<div><span>" + pLine + "</span></div>"
                else:
                    # 이미지 태그를 P태그로 감싸기
                    # 2021.03.13 기능 살림
                    for img in pLine.select("img"):
                        img.wrap(detailSoup.new_tag("p"))
            except AttributeError as e:
                print(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ", 예외가 발생했습니다." + str(e) + ", 오류가 발생한 곳은 : " + str(e.__traceback__.tb_lineno))
                # 에러 발생해도 무시 - 아래 코드들이 문자열 처리하는 기능이라서 실행되도 상관 없음
                pass
            
            
            # 유튜브 주소를 찾아서 링크 url 변경 처리, 유튜브 주소 없을경우는 변경없이 저장
            pLineText = str(pLine)
            # 유튜브 짧은 주소 접두어
            utubeShrotUrlIndex = pLineText.find('https://youtu.be/')
            # 유튜브 긴 주소 접두어
            utubeUrlIndex = pLineText.find('https://youtube.com/watch?v=')
            # 유튜브 www 긴 주소 접두어
            utubewwwUrlIndex = pLineText.find('https://www.youtube.com/watch?v=')
            # 유튜브 모바일 긴 주소 접두어
            utubemobileUrlIndex = pLineText.find('https://m.youtube.com/watch?v=')
            # 유튜브 shorts 주소 접두어
            utubeshortsUrlIndex = pLineText.find('https://youtube.com/shorts/')
            # 유튜브 shorts 긴 주소 접두어
            utubewwwshortsUrlIndex = pLineText.find('https://www.youtube.com/shorts/')

            # 2021.01.03 유튜브 키값 초기화 추가
            utubeKey = ""
            # 2021.01.03 유튜브 키값 초기화 추가
            utubeKeyIndex = 0

            # 유튜브 주소 길이 판단
            if utubeShrotUrlIndex > 0:
                utubeKeyIndex = pLineText.find('https://youtu.be/')
                # 2021.01.03 파싱 수정 추가
                utubeKey = pLineText[utubeKeyIndex + 17 : utubeKeyIndex + 17 + 11]
                # 유튜브 키값을 iframe 태그로 변경
                # 2022.02.27 p 태그 안에 img와 youtube 같이 있는 경우 감안하여 pLine에 iframe tag 추가
                tempStr = pLineText + '<p><iframe style="width:560; height:315px" src="https://www.youtube.com/embed/' + utubeKey + '?rel=0&vq=hd1080" frameborder="0" allowfullscreen></iframe>'
            elif utubeUrlIndex > 0:
                utubeKeyIndex = pLineText.find('https://youtube.com/watch?v=')
                # 2021.01.03 파싱 수정 추가
                utubeKey = pLineText[utubeKeyIndex + 28 : utubeKeyIndex + 28 + 11]
                # 유튜브 키값을 iframe 태그로 변경
                # 2022.02.27 p 태그 안에 img와 youtube 같이 있는 경우 감안하여 pLine에 iframe tag 추가
                tempStr = pLineText + '<p><iframe style="width:560; height:315px" src="https://www.youtube.com/embed/' + utubeKey + '?rel=0&vq=hd1080" frameborder="0" allowfullscreen></iframe>'
            elif utubewwwUrlIndex > 0:
                utubeKeyIndex = pLineText.find('https://www.youtube.com/watch?v=')
                # 2021.01.18 파싱 추가
                utubeKey = pLineText[utubeKeyIndex + 32 : utubeKeyIndex + 32 + 11]
                # 유튜브 키값을 iframe 태그로 변경
                # 2022.02.27 p 태그 안에 img와 youtube 같이 있는 경우 감안하여 pLine에 iframe tag 추가
                tempStr = pLineText + '<p><iframe style="width:560; height:315px" src="https://www.youtube.com/embed/' + utubeKey + '?rel=0&vq=hd1080" frameborder="0" allowfullscreen></iframe>'
            elif utubemobileUrlIndex > 0:
                utubeKeyIndex = pLineText.find('https://m.youtube.com/watch?v=')
                # 2023.02.16 파싱 추가
                utubeKey = pLineText[utubeKeyIndex + 30 : utubeKeyIndex + 30 + 11]
                # 유튜브 키값을 iframe 태그로 변경
                tempStr = pLineText + '<p><iframe style="width:560; height:315px" src="https://www.youtube.com/embed/' + utubeKey + '?rel=0&vq=hd1080" frameborder="0" allowfullscreen></iframe>'
            elif utubeshortsUrlIndex > 0:
                utubeKeyIndex = pLineText.find('https://youtube.com/shorts/')
                # 2022.10.07 파싱 추가
                utubeKey = pLineText[utubeKeyIndex + 27 : utubeKeyIndex + 27 + 11]
                # 유튜브 키값을 iframe 태그로 변경
                tempStr = pLineText + '<p><iframe style="width:315; height:560px" src="https://www.youtube.com/embed/' + utubeKey + '?rel=0&vq=hd1080" frameborder="0" allowfullscreen></iframe>'
            elif utubewwwshortsUrlIndex > 0:
                utubeKeyIndex = pLineText.find('https://www.youtube.com/shorts/')
                # 2022.10.07 파싱 추가
                utubeKey = pLineText[utubeKeyIndex + 31 : utubeKeyIndex + 31 + 11]
                # 유튜브 키값을 iframe 태그로 변경
                tempStr = pLineText + '<p><iframe style="width:315; height:560px" src="https://www.youtube.com/embed/' + utubeKey + '?rel=0&vq=hd1080" frameborder="0" allowfullscreen></iframe>'
            else:
                # 유튜브 주소가 없을 경우 변경 없음
                tempStr = pLineText

            # 유튜브 키 리스트에 유튜브 키값 추가
            youtubekeylist.append(utubeKey)

            # src="https://www.youtube.com/embed/ 가 존재하는 지 확인
            match2 = re.search(regex2, pLineText)
            if match2:
                embedutubeKey = match2.group(1)
                if embedutubeKey in youtubekeylist:
                    # 2023.07.10 이전에 저장된 유튜브 키값이 있으면 중복으로 iframe 처리 되니 다음으로 진행
                    continue

            try:
                # 트위터 주소 찾기
                # 2023.03.14 추가
                if 'https://twitter.com/' in pLine.find('a')['href']:
                    tempStr = pLineText + '<p><blockquote class="twitter-tweet" lang="en"><a href="' + pLine.find('a')['href'] + '"></a></blockquote><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'
            except:
                pass

            try:
                # 트위터 iframe 찾기
                # 2023.08.17 추가
                if 'ed-twitter-div' in pLineText:
                    # 제외 처리
                    continue
            except:
                pass

            # ggoorr video 접두어
            ggoorrvideoIndex = pLineText.find('src="/files/')

            # ggoorr video 존재 확인
            if ggoorrvideoIndex > 0:
                # 전체 URL로 변경
                pLineText = pLineText.replace('src="/files/', 'src="https://ggoorr.net/files/')
                tempStr = pLineText
                # # src 확인
                # ggoorrvideourl = BeautifulSoup(pLineText, 'lxml').find('video')['src']
                # # cv2 객체 생성
                # ggoorrvideo = cv2.VideoCapture(ggoorrvideourl)
                # # cv3 객체 폭
                # ggoorrvideowidth = int(ggoorrvideo.get(cv2.CAP_PROP_FRAME_WIDTH))
                # # cv2 객체 해제
                # ggoorrvideo.release()
                # # 모바일 환경 고려하여 333을 넘길 경우 수정
                # if ggoorrvideowidth > 333:
                #     tempStr = pLineText.replace("<video", '<video width="333"')
                # else:
                #     tempStr = pLineText

            # 줄 끝에 줄 바꿈 처리
            articleString += tempStr + "\n"

        # 03 게시글 끝에 꼬릿말 추가
        articleString += articleTail   

        # 04 cdn.ggoorr.net은 프록시 서버 경유
        articleString = articleString.replace("https://cdn.ggoorr.net", "https://t1.daumcdn.net/thumb/R1024x0/?fname=https://cdn.ggoorr.net")

        # 2021.02.27 05.제목이 포함된 내용 삭제하기
        # 2021.03.07 05-02 제목과 100% 동일한 본문 내용 삭제하기
        articleString = articleString.replace(title, "")
        # 2023.03.15 escape 문자 처리 위해 html.escape 추가
        articleString = articleString.replace(html.escape(title), "")

        # 파일에 저장
        # 2021.01.03 게시글 제목 앞에 <p> 추가, 제목 뒤에 </p> 추가.
        fileContent = "<p>" + title + "</p>"
        fileContent += "\n"
        fileContent += articleString
        fileContent += "\n"

        # realwritetime을 key로해서 html코드를 value로 저장
        contentDictionary[realwritetime] = fileContent

    else :
        print(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ", >>>> GET ERROR.....")
    # 대기
    time.sleep(waittime)

# 게시판 목록 처리 함수 : 게시글 목록에서 해당 게시물이 작성 대상인 경우 게시글 상세 처리(getDetail)를 호출
# 게시글 처리 대상 - 전일 오전 7시 ~ 당일 오전 6시 59분 59초
def searchList(page):

    print(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + " ========== " + str(page) + " page start ==========")
    # 봇 방지 웹사이트 회피
    headers = {'User-Agent': generate_user_agent(device_type = 'desktop') }
    res = requests.get(GGOORR_DETAIL_URL + str(page), headers = headers)

    if res.status_code == 200:
        # 응답 html코드를 text로 변환
        html = res.text

        # 응답받은 html코드를 BeautifulSoup에 사용하기 위하여 인스턴스 지정
        # 2022.07.24 가져오는 방식 변경
        # HTML을 'lxml(XML, HTML 처리)'를 사용하여 분석
        soup = BeautifulSoup(html, 'lxml')

        # tbody 에 필요한 게시글 목록이 있어 해당 영역 가져오기 처리
        # 2022.07.24 가져오는 방식 변경
        # tbody = soup.select('.bd_tb_lst tbody')
        tbody = soup.find('table', 'bd_lst bd_tb_lst bd_tb')        
        # 2022.07.24 가져오는 방식 변경
        # contentsBody = tbody[0]
        contentsBody = tbody.find('tbody')

        # 게시글 처리 순서 저장
        nCnt = 1
        # tr - 개별 게시글 확인
        for trOne in contentsBody.select('tr'):

            print(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "---------- [ " + str(page) + " page / " + str(nCnt) + " line ] ----------")

            # 공지글은 생략
            if None != trOne.get('class'):
                if ("notice" == trOne['class'][0]):
                    print(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ", 공지는 PASS!!")
                    nCnt += 1
                    continue
            else:
                # 변수 초기화
                cate = ""
                title = ""
                author = ""
                time1 = ""
                time2 = ""
                detailUrl = ""
                timenumber = ""
                writetime = ""

                # td 확인
                for tdTag in trOne.select('td'):
                    # td 태그의 class 가져오기
                    classNm = tdTag["class"][0]
                    if classNm == "cate":
                        # 카테고리
                        cate = tdTag.get_text()
                    elif classNm == "title":
                        # 제목 및 URL
                        alist = tdTag.find_all('a', class_ = "hx")
                        title = alist[0].get_text().strip().replace("\n", "")
                        detailUrl = GGOORR_MAIN_URL + alist[0]['data-viewer']
                        # 2023.03.09 정확한 시간 파악 위해서 url 먼저 수집
                        detailUrllist.append(detailUrl)
                    elif classNm == "author":
                        # 작성자
                        author = tdTag.get_text()
                    elif classNm == "time":
                        # 1일 이내는 N분 전/N시간 전, 1일 이후는 날짜
                        time1 = tdTag.get_text()
                        # 1일 이내는 N분 전/N시간 전, 1일 이후는 시간
                        time2 = tdTag.attrs['title']

                        if '분' in time1:
                            # 분일 경우 작성 시간 확인
                            timenumber = time1[0:time1.find('분')]
                            writetime = datetime.today() - timedelta(minutes=int(timenumber))
                        elif '시간' in time1:
                            # 시간일 경우 작성 시간 확인
                            timenumber = time1[0:time1.find('시간')]
                            writetime = datetime.today() - timedelta(hours=int(timenumber))
                        else:
                            # 분과 시간이 아니면 날짜와 시간을 조합
                            writetime = datetime.strptime((time1 + " " + time2), '%Y.%m.%d %H:%M')
                    else:
                        pass
                # end of [for tdTag in trOne.select('td'):]

                # 게시물 1개에 대한 처리여부 확인 로직 시작......
                print(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ", category : " + cate)
                print(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ", title : " + title)
                print(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ", author : " + author)
                print(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ", writetime : " + writetime.strftime('%Y-%m-%d %H:%M:%S'))
                print(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ", detailUrl : " + detailUrl)

                # # 전일 오전 7시
                # yesterday = datetime.today() - timedelta(days=1)
                # fromdate = datetime(yesterday.year, yesterday.month, yesterday.day, 7, 0, 0)

                # # 당일 오전 6시 59분 59초
                # todate = datetime(datetime.today().year, datetime.today().month, datetime.today().day, 6, 59, 59)

                # # 정상 처리
                # if(writetime > todate):
                #     print("작성 안 하고, 다음 게시물 조회 (당일 6시 59분 59초 초과)")
                #     pass
                # elif writetime < fromdate:
                #     print("작성 대상 아님 - (전일 7시 미만)")
                #     pass
                #     # return False
                # else :
                #     print("작성 대상 맞음 (전일 7시 ~ 당일 6시 59분 59초)")

            nCnt += 1
            # end of [for trOne in contentsBody.select('tr'):]
        print(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + "========== " +  str(page) + " page end ==========")
        return True        
    else:
        print(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ", " + GGOORR_DETAIL_URL + str(page) + " >>>> GET ERROR.....")
    # 대기
    time.sleep(waittime)

# 데이터 정렬하여 파일에 저장 처리 
def SaveSortedContentDictionary():
    # 딕셔너리는 key로 정렬하면 튜플 형태의 리스트가 됨
    sortedKeyList = sorted(contentDictionary.items())
    # 정렬 후 value를 파일에 저장
    for (tuplekey, tuplevalue) in sortedKeyList:             
        f.write(str(tuplevalue))

    if f is not None:
        f.close
        print(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + ", fileContent write OK ")

# 메인 시작 : 1-15 페이지까지 for loop
def startCrawlering():
    # 시간1
    datetime1 = datetime.now()
    print(datetime1.strftime('%Y-%m-%d %H:%M:%S') + " - Starting")
    # 15페이지까지 검색
    for page in range(1, 15 + 1):
        searchList(page)
    print(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + " Starting Crawling")
    # 크롤링 시작
    for detailUrl in detailUrllist:
        print(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + " " + str(detailUrllist.index(detailUrl) + 1) + "/" + str(len(detailUrllist)))
        getDetail(detailUrl, 'Y')
    print(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + " Ending Crawling")
    # 에러 url들이 있을 경우 크롤링 시작
    if len(errorurls) != 0:
        print(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + " Starting Error Crawling")
        # 에러 url들이 사라질 때까지 반복
        while True:
            # 에러 url 가져오기
            for errorurl in errorurls[:]:
                print(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + " " + str(errorurls.index(errorurl)) + "/" + str(len(errorurls)))
                # 크롤링 시작
                if False != getDetail(errorurl, 'Y'):
                    # 정상 처리 되면 errorurls에서 에러 url 삭제
                    errorurls.remove(errorurl)
            # 에러 url들이 없는 것을 확인
            if len(errorurls) == 0:
                # 에러 url들에 대한 크롤링 종료
                break
        print(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + " Ending Error Crawling")
    # 데이터 정렬하여 파일에 저장 처리 
    SaveSortedContentDictionary()
    # 시간1과 시간2의 차이를 구한다
    datetime2 = datetime.now()
    print(datetime1.strftime('%Y-%m-%d %H:%M:%S') + " ~ " + datetime2.strftime('%Y-%m-%d %H:%M:%S') + " - Ending")
    print(datetime2 - datetime1)

tempurllist = [
"https://ggoorr.net/all/15814039",
"https://ggoorr.net/all/15811184",
]
# 임시 작업일 경우 아래 4개줄 주석 해제
# for tempurl in tempurllist:
#     getDetail(tempurl, 'N')
# SaveSortedContentDictionary()
# sys.exit()

# 크롤링 시작
startCrawlering()