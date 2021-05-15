import requests, json
import sys
from bs4 import BeautifulSoup
from bs4 import NavigableString
from datetime import datetime, timedelta
# 이미지 해상도 확인 2021.01.23 병합
import io
import struct
import urllib.request as urllib2
# 에러 확인 위해 HTTPError을 import
from urllib.request import HTTPError
import re

# 전역 변수 설정
GGOORR_MAIN_URL = "https://ggoorr.net"                              # 꾸르 메인 주소
GGOORR_DETAIL_URL = 'https://ggoorr.net/index.php?mid=all&page='    # 꾸르 상세 주소
headers = {'User-Agent': 'Mozilla/5.0'}                             # 봇 방지 웹사이트 회피

# 파일 변수 글로벌로 이동
nowDate = datetime.now()
# 파일 작성 시간이 길어져서 년월일로 파일명 생성
f = open(nowDate.strftime('%Y-%m-%d') + '_ggoorr.txt', mode='wt', encoding='utf-8')
# 전체 컨텐츠가 저장되는 dictionary
contentDictionary = {}
# 전체 컨텐츠가 sort 되어 저장되는 dictionary
sortedKeyList = {}

# 이미지 해상도 확인 2021.01.23 병합
def getImageInfo(imgUrl):

        req = urllib2.Request(imgUrl, headers={"Range": "5000", "User-Agent": 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"})

        # try:
        #     r = urllib2.urlopen(req)
        #     data = r.read()
        # except HTTPError as e:
        #     print(e) # null을 반환하거나, break 문을 실행하거나, 기타 다른 방법을 사용

        r = urllib2.urlopen(req)

        data = r.read()

        size = len(data)
        # print(size)
        height = -1
        width = -1
        content_type = ''

        # handle GIFs
        if (size >= 10) and data[:6] in (b'GIF87a', b'GIF89a'):
            # Check to see if content_type is correct
            content_type = 'image/gif'
            w, h = struct.unpack(b"<HH", data[6:10])
            width = int(w)
            height = int(h)

        # See PNG 2. Edition spec (http://www.w3.org/TR/PNG/)
        # Bytes 0-7 are below, 4-byte chunk length, then 'IHDR'
        # and finally the 4-byte width, height
        elif ((size >= 24) and data.startswith(b'\211PNG\r\n\032\n')
                and (data[12:16] == b'IHDR')):
            content_type = 'image/png'
            w, h = struct.unpack(b">LL", data[16:24])
            width = int(w)
            height = int(h)

        # Maybe this is for an older PNG version.
        elif (size >= 16) and data.startswith(b'\211PNG\r\n\032\n'):
            # Check to see if we have the right content type
            content_type = 'image/png'
            w, h = struct.unpack(b">LL", data[8:16])
            width = int(w)
            height = int(h)

        # handle JPEGs
        elif (size >= 2) and data.startswith(b'\377\330'):
            content_type = 'image/jpeg'
            jpeg = io.BytesIO(data)
            jpeg.read(2)
            b = jpeg.read(1)
            try:
                while (b and ord(b) != 0xDA):
                    while (ord(b) != 0xFF): b = jpeg.read(1)
                    while (ord(b) == 0xFF): b = jpeg.read(1)
                    if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
                        jpeg.read(3)
                        h, w = struct.unpack(b">HH", jpeg.read(4))
                        break
                    else:
                        jpeg.read(int(struct.unpack(b">H", jpeg.read(2))[0])-2)
                    b = jpeg.read(1)
                width = int(w)
                height = int(h)
            except struct.error:
                pass
            except ValueError:
                pass

        return content_type, width, height

# 상세 게시글 HTML 수집 함수
def getDetail(writetimeString, title, detailUrl):

    # 상세 주소 요청 및 응답 수신
    detailRes = requests.get(detailUrl, headers=headers)

    # HTTP 응답 성공 200
    if detailRes.status_code == 200:
        
        # 게시글의 HTML을 받아 BeautifulSoup 로 파싱 저장 
        detailHtml = detailRes.text
        detailSoup = BeautifulSoup(detailHtml, 'html.parser')
        
        # article 태그만 데이터만 사용함
        articleBody = detailSoup.find('article')  # article 태그 찾기 

        # span class="fr-video" 있는 article은 PASS 2021.01.19 수정
        articleBodyText = str(articleBody)
        articleBodyGIFText1 = articleBodyText.find("fr-video")
        if articleBodyGIFText1 >=0:
            print("articleBody span class=fr-video >=0 is pass")
            return

        # video class="gifmp4_video" 있는 article은 PASS 2021.01.26 추가
        articleBodyGIFText2 = articleBodyText.find("gifmp4_video")
        if articleBodyGIFText2 >=0:
            print("articleBody video class=gifmp4_video >=0 is pass")
            return

        # articleBody 에서 div 영역을 찾아서, p 로 바꿈...
        # xeContentDiv = articleBody.div.div.contents
        # xeContentDivStr = str(xeContentDiv)
        # xeContentDivStr = xeContentDivStr.replace("<div","<p")
        # xeContentDivStr = xeContentDivStr.replace("div>","p>")
        # articleBody = BeautifulSoup(xeContentDivStr, 'html.parser')

        # div class xe_content 내의 child 를 순차적으로 호출하여 div 로 시작하는 첫번째 태그만 <p> 로 변경 
        # for child in articleBody.div.div.children:
        #     if child.name == 'div':
        #         child.name = 'p'

        # 게시글 머릿말/꼬리말 설정
        articleHeader = '<article><div id="article_1"><div>'
        articleTail = '</div></div></article>'
 
        # 01 게시글 앞에 머릿말 추가
        articleString = articleHeader

        # 02 article 태그 안에서 <p>태그들을 찾아서 저장함
        # for pLine in articleBody.select("p"):
        for pLine in articleBody.div.div.children:     # p 로 처리하는 방식에서 문제가 많아 child 방식으로 변경

            # 2021.02.24 구글 블로거에서 자동으로 width를 810으로 맞추어 주어서 주석 처리
            # # 이미지 태그가 있는경우, 이미지의 사이즈를 체크 및 수정
            # for img in pLine.select("img"):
            #     # src 속성 찾기
            #     imgSrcText = str(img['src'])
            #     # style 속성 삭제
            #     del img['style']
            #     # print(imgSrcText)
            #     if imgSrcText == "None":
            #         # 이미지가 없을 경우
            #         pass
            #     elif ".daumcdn.net" in imgSrcText:
            #         # .daumcdn.net가 있을 경우 폭을 800으로 변경
            #         img['src'] = imgSrcText.replace("R1024x0", "R800x0")
            #     elif "gamechosun.co.kr" in imgSrcText: 
            #         # 2021.01.26 gamechosun.co.kr 문제 있어서 예외 처리
            #         img['width'] = 800
            #     else:
            #         # 그 외 경우는 폭이 800을 초과할 경우 width 속성을 800으로 지정
            #         imgArr = getImageInfo( img['src'] )
            #         # print(str(imgArr))
            #         if imgArr != None and len(imgArr) == 3 and int(imgArr[1]) > 800:
            #             img['width'] = 800
            try:               
                # tag 없는 일반 문자열만 있을 경우 .select() 실행시 오류 발생하여 분기 처리
                if isinstance(pLine, NavigableString):
                    pLine = "<div><span>" + pLine + "</span></div>"
                else:
                    # 이미지 태그를 P태그로 감싸기 2021.03.13 기능 살림
                    for img in pLine.select("img"):
                        img.wrap(detailSoup.new_tag("p"))               
            except AttributeError as e:
                print("예외가 발생했습니다.", e)
                pass # 에러 발생해도 무시 - 아래 코드들이 문자열 처리하는 기능이라서 실행되도 상관 없음

            # 유튜브 주소를 찾아서 링크 url 변경 처리, 유튜브 주소 없을경우는 변경없이 저장
            pLineText = str(pLine)
            utubeShrotUrlIndex  = pLineText.find('https://youtu.be/')                  # 유튜브 짧은 주소 접두어
            utubeUrlIndex       = pLineText.find('https://youtube.com/watch?v=')       # 유튜브 긴 주소 접두어
            utubewwwUrlIndex    = pLineText.find('https://www.youtube.com/watch?v=')   # 유튜브 www 긴 주소 접두어

            utubeKey = ""       # 유튜브 키값 초기화 2021.01.03 추가
            utubeKeyIndex = 0   # 유튜브 키값 초기화 2021.01.03 추가
            # tempStr = ""        # 임시 변수 초기화 2021.01.25 추가

            # 유튜브 주소 길이 판단
            if utubeShrotUrlIndex >= 0:
                utubeKeyIndex = pLineText.find('https://youtu.be/')
                utubeKey = pLineText[utubeKeyIndex + 17 : utubeKeyIndex + 17 + 11] # 파싱 수정 2021.01.03 추가
                # 유튜브 키값을 iframe 태그로 변경
                tempStr = '<p><iframe style="width:560; height:315px" src="https://www.youtube.com/embed/' + utubeKey + '?rel=0&vq=hd1080" frameborder="0" allowfullscreen></iframe>'
            elif utubeUrlIndex >= 0:
                utubeKeyIndex = pLineText.find('https://youtube.com/watch?v=')
                utubeKey = pLineText[utubeKeyIndex + 28 : utubeKeyIndex + 28 + 11] # 파싱 수정 2021.01.03 추가
                # 유튜브 키값을 iframe 태그로 변경
                tempStr = '<p><iframe style="width:560; height:315px" src="https://www.youtube.com/embed/' + utubeKey + '?rel=0&vq=hd1080" frameborder="0" allowfullscreen></iframe>'
            elif utubewwwUrlIndex >= 0:
                utubeKeyIndex = pLineText.find('https://www.youtube.com/watch?v=')
                utubeKey = pLineText[utubeKeyIndex + 32 : utubeKeyIndex + 32 + 11]  # 파싱 추가 2021.01.18 추가
                # 유튜브 키값을 iframe 태그로 변경
                tempStr = '<p><iframe style="width:560; height:315px" src="https://www.youtube.com/embed/' + utubeKey + '?rel=0&vq=hd1080" frameborder="0" allowfullscreen></iframe>'
            else:
                # 유튜브 주소가 없을 경우 변경 없음
                tempStr = pLineText

            # 줄 끝에 줄 바꿈 처리
            articleString += tempStr + "\n"
        # end of [for pLine in articleBody.select("p"):]

        # 03 게시글 끝에 꼬릿말 추가
        articleString += articleTail   
        
        # 04 3가지 변경 작업
        # 04-01 cdn.ggoorr.net은 프록시 서버 경유
        articleString = articleString.replace("https://cdn.ggoorr.net", "https://t1.daumcdn.net/thumb/R0x0/?fname=https://cdn.ggoorr.net")
        # 04-02 img 태그 앞에 줄 바꿈
        # articleString = articleString.replace("<img", "<p><img")
        # 04-03 img 폭을 800 2020.12.29 추가 2021.01.23 삭제
        # articleString = articleString.replace("<img", "<img width=800")
        
        # 05.제목이 포함된 내용 삭제하기 2021.02.27
        # 변수 초기화, 지정
        titleIndex = 0
        tmpTitle = title

        # 05-01 제목 끝에 "(스압)" 을 제거 2021.03.07
        tmpTitle = tmpTitle.replace("(스압)", "").strip()

        # 05-02 제목과 100% 동일한 본문 내용 삭제하기 2021.03.07 
        articleString = articleString.replace(tmpTitle, "")

        # 05-03 제목에 "[xxx]" 가 있으나 본문에는 "[xxx]"가 없는 경우 처리 > 제목의 [xxx]를 제거
        if title.find("]") >= 0:
            titleIndex = title.index("]")
        # "[ ~ ]"가 있을 경우 처리 2021.02.27
        if tmpTitle.startswith("[") and titleIndex >= 0:
            tmpTitle = (title[titleIndex+1:]).strip()
        articleString = articleString.replace(tmpTitle, "")
        
        # 파일에 저장
        fileContent = "<p>" + title + "</p>" # 게시글 제목 앞에 <p> 추가, 제목 뒤에 </p> 추가. 2021.01.03 추가
        # fileContent += "\n"
        # fileContent += writetimeString
        fileContent += "\n"
        fileContent += articleString
        fileContent += "\n"

        # 작성시간을 key로해서 html코드를 value로 저장
        contentDictionary[writetimeString] = fileContent
        
        # if (f is not None) and f.write(fileContent):
        #     print("fileContent write OK ")
    else :
        print(" >>>> GET ERROR.....")
    
    # print("------------------------------------ end of getDetail -----------------------------------")

# 게시판 목록 처리 함수 : 게시글 목록에서 해당 게시물이 작성 대상인 경우 게시글 상세 처리(getDetail)를 호출
# 게시글 처리 대상 - 전일 오전 7시 ~ 당일 오전 6시 59분 59초
def searchList(page):

    print("=========================================== " + str(page) + " page start =====================================")
    res = requests.get(GGOORR_DETAIL_URL + str(page), headers=headers)

    if res.status_code == 200:
        # 응답 html코드를 text로 변환
        html = res.text

        # 응답받은 html코드를 BeautifulSoup에 사용하기 위하여 인스턴스 지정
        soup = BeautifulSoup(html, 'html.parser')

        # tbody 에 필요한 게시글 목록이 있어 해당 영역 가져오기 처리
        tbody = soup.select('.bd_tb_lst tbody')
        contentsBody = tbody[0]

        nCnt = 0 # 게시글 처리 순서 저장
        # tr - 개별 게시글 확인
        for trOne in contentsBody.select('tr'):
            print("--------------------------------------- [ " + str(page) + " page / " + str(nCnt) + " line ] ---------------------------------------")

            # 공지글은 생략
            if None != trOne.get('class'):
                if ("notice" == trOne['class'][0]):
                    print("공지는 PASS!!")
                    nCnt+=1
                    continue
            else:
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
                    classNm = tdTag["class"][0]
                    if classNm == "cate":
                        # 카테고리
                        cate = tdTag.get_text()
                    elif classNm == "title":
                        # 제목 및 URL
                        alist = tdTag.find_all('a', class_="hx")
                        title = alist[0].get_text().strip().replace("\n", "")
                        detailUrl = GGOORR_MAIN_URL + alist[0]['data-viewer']
                    elif classNm == "author":
                        # 작성자
                        author = tdTag.get_text()
                    elif classNm == "time":
                        time1 = tdTag.get_text()        # 1일 이내는 N분 전/N시간 전, 1일 이후는 날짜
                        time2 = tdTag.attrs['title']    # 1일 이내는 N분 전/N시간 전, 1일 이후는 시간

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
                print("category : " + cate)
                print("title : " + title)
                print("author : " + author)
                print("writetime : " + writetime.strftime('%Y-%m-%d %H:%M:%S'))
                print("detailUrl : " + detailUrl)

                # 전일 오전 7시
                yesterday = datetime.today() - timedelta(days=1)
                fromdate = datetime(yesterday.year, yesterday.month, yesterday.day, 7, 0, 0)

                # 당일 오전 6시 59분 59초
                todate = datetime(datetime.today().year, datetime.today().month, datetime.today().day, 6, 59, 59)

                if(writetime > todate):
                    print("작성 안 하고, 다음 게시물 조회")
                    pass
                # 2021.02.24 구글 블로거에서 자동으로 width를 810으로 맞추어 주어서 주석 처리
                # elif detailUrl == "https://ggoorr.net/index.php?mid=all&document_srl=11074939&listStyle=viewer":
                #     print("HTTP Error 400 있는 경우라서, 다음 게시물 조회")
                #     pass
                # elif detailUrl == "https://ggoorr.net/index.php?mid=all&document_srl=11090562&listStyle=viewer":
                #     print("HTTP Error 400 있는 경우라서, 다음 게시물 조회")
                #     pass                
                # elif detailUrl == "https://ggoorr.net/index.php?mid=all&document_srl=11220982&listStyle=viewer":
                #     print("<div>와 </div> 사이에 내용이 있어서, 다음 게시물 조회")
                #     pass                
                elif writetime <= fromdate:
                    print("작성 대상 아님 - 더 이상 게시물 조회하지 않음")

                    # 데이터 정렬하여 파일에 저장 처리 
                    SaveSortedContentDictionary()

                    return False
                else :
                    print("작성 대상 맞음")
                    # 작성 시간을 (20-nCnt)만큼 빼기
                    # writetimeref = writetime - timedelta(seconds=int(20-nCnt))
                    # string으로 변환
                    # stringwritetime = writetimeref.strftime('%Y-%m-%d %H:%M:%S')
                    stringwritetime = writetime.strftime('%Y-%m-%d %H:%M:%S')
                    # 함수로 넘김
                    getDetail(stringwritetime, title, detailUrl)

            nCnt+=1
            # end of [for trOne in contentsBody.select('tr'):]
        print("=========================================== end of List =====================================")
        return True        
    else:
        print(GGOORR_DETAIL_URL + str(page) + " >>>> GET ERROR.....")

# 데이터 정렬하여 파일에 저장 처리 
def SaveSortedContentDictionary():
    # 딕셔너리는 key로 정렬하면 튜플 형태의 리스트가 됨
    sortedKeyList = sorted(contentDictionary.items())
    # 정렬 후 value를 파일에 저장
    for (tuplekey, tuplevalue) in sortedKeyList:             
        f.write(str(tuplevalue))
        print("fileContent write OK ")
    
    if f is not None:
        f.close

# youtube test
# getDetail("title", "https://ggoorr.net/enter/10765153")
# sys.exit()

# gif test
# getDetail("title", "https://ggoorr.net/thisthat/10768975")
# sys.exit()

# 문제의 <p>태그없이 이미지만 있는 게시물 > 해결 안됨 > 처리 룰 필요..!!
# getDetail("title", "https://ggoorr.net/enter/10770855")
# sys.exit()

# 문제의 <p>태그없이 href 만 있는 게시물 > 해결 안됨 > 처리 룰 필요..!!
# getDetail("title", "https://ggoorr.net/all/10815964")
# sys.exit()

# 이미지 가로 사이즈 800 이상
# getDetail("title", "https://ggoorr.net/all/10857189")
# sys.exit()

# 이미지를 daum cdn 을 통해 서비스 하는 경우 - img1.daumcdn.net
# getDetail("title", "https://ggoorr.net/all/10898864")
# sys.exit()

# 이미지를 daum cdn 을 통해 서비스 하는 경우  - t1.daumcdn.net
# getDetail("title", "https://ggoorr.net/all/10894836")
# sys.exit()

# img styles 속성이 있는 경우
# getDetail("title", "https://ggoorr.net/all/10893852")
# sys.exit()

# 텍스트가 중복되는 경우
# getDetail("title", "https://ggoorr.net/all/10909429")
# sys.exit()

# 이미지 태그 p 로 감싸기 확인용 
# getDetail("title", "https://ggoorr.net/all/10917601")
# sys.exit()

# gamechosun.co.kr 이미지 있는 경우
# getDetail("title", "https://ggoorr.net/all/10918226")
# sys.exit()

# HTTP Error 400: Bad Request 이미지 있는 경우
# getDetail("title", "https://ggoorr.net/all/11074939")
# sys.exit()

# 제목 중복 지우기 (동일)
# getDetail("브이로그 유튜버 진훤", "https://ggoorr.net/thisthat/11095623")
# sys.exit()

# 제목 중복 지우기 (유사)
# getDetail("[놀면뭐하니] 동거동락 유경험자 탁재훈 클래스", "https://ggoorr.net/all/11100509")
# sys.exit()

# http://zeany.net/46 참고해서 제목 지우기 시도해보기

# 제목 중복 지우기 (괄호 있는 것까지 동일)
# getDetail("[쓰리박] 박지성 인맥이 부러운 이청용", "https://ggoorr.net/enter/11157332")
# sys.exit()

# 제목 중복 지우기 (제목 뒤에 괄호 있는 동일)
# getDetail("러블리즈 정예인 레깅스 (스압)", "https://ggoorr.net/enter/11157408")
# sys.exit()

# 제목 중복 지우기 (내용 끝에 동일한 제목)
# getDetail("2021-05-15 12:08:02", "요즘 이미지 망친 회사들의 공통점", "https://ggoorr.net/all/11173591")
# sys.exit()

# 2021.03.15 <div>와 </div> 사이에 내용이 있을 경우 오류 발생 - <div>를 <p>로 변경할 지?
# getDetail("2021-05-15 12:08:01", "악마도 울고 갈 CJ의 아이즈원 컴백및 발표 타이밍", "https://ggoorr.net/enter/11220982")
# sys.exit()

# contentDictionary - 데이터 정렬하여 저장하는 함수 
# SaveSortedContentDictionary()


# 메인 시작 : 1-20 페이지까지 for loop
def startCrawlering():
    for page in range(1, 20):
        if False == searchList(page):
            break

startCrawlering()