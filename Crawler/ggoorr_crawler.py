import sys
import requests
import time
from bs4 import BeautifulSoup
from bs4 import NavigableString
from datetime import datetime, timedelta

# pip install user-agent
from user_agent import generate_user_agent
import html
import re
import pytz
from pathlib import Path
import logging

# 로거 생성
logger = logging.getLogger("GgoorrLogger")
logger.setLevel(logging.INFO)

# 출력 형식 설정
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# 콘솔 출력 설정
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
stream_handler.setLevel(logging.INFO)

# 날짜별 로그 파일 생성
log_file = (
    f"D:\\Python\\LOG\\{datetime.now().strftime('%Y%m%d%H%M%S')}_ggoorr.log"
)
file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
file_handler.setLevel(logging.DEBUG)

# 크롤링 기준 날짜 설정 (None이면 오늘 날짜, "YYYY-MM-DD" 형식이면 해당 날짜 지정)
TARGET_DATE = None
# TARGET_DATE = "2025-12-18"

# 크롤링할 페이지 범위 설정
# 평소(TARGET_DATE is None)에는 1~10페이지를 탐색하고,
# 특정 날짜 지정 시에는 아래 범위를 사용하도록 로직을 수정합니다.
# 시작 페이지
TARGET_START_PAGE = 45
# 종료 페이지
TARGET_END_PAGE = 55

# 오늘 날짜를 YYYYMMDDHHMMSS 형태로 변경
todaytime = datetime.today().strftime("%Y%m%d%H%M%S")
# 시간을 HH 형태로 변경
todaytimeHH = datetime.today().strftime("%H")

# KST 시간대 설정
kst_timezone = pytz.timezone("Asia/Seoul")

# 전역 변수 설정
# 꾸르 메인 주소
GGOORR_MAIN_URL = "https://ggoorr.net"
# 꾸르 상세 주소
GGOORR_DETAIL_URL = "https://ggoorr.net/main/page/"
# 저장 폴더
savefolder = Path("D:/ggoorr")
# 에러 발생 URL 모음
errorurls = []
# 파일 변수 글로벌로 이동
nowDate = datetime.now()
# 파일 작성 시간이 길어져서 년월일로 파일명 생성
f = open(savefolder / (nowDate.strftime("%Y-%m-%d") + "_ggoorr.txt"), mode="wt", encoding="utf-8")
# 전체 컨텐츠가 저장되는 dictionary
contentDictionary = {}
# 전체 컨텐츠가 sort 되어 저장되는 dictionary
sortedKeyList = {}
# 대기 시간
waittime = 0.5
# 게시글 url 리스트
detailUrllist = []

# 숫자를 추출하기 위한 정규 표현식
regex1 = r"\d+"
# "embed/" 다음에 있는 유튜브 키값 추출을 위한 정규 표현식
regex2 = r"embed/([a-zA-Z0-9_-]+)"


# 상세 게시글 HTML 수집 함수
def getDetail(detailUrl, option):
    # 2022.12.06 게시글 순번으로 sort
    # 2023.07.10 수정
    match1 = re.search(regex1, detailUrl)
    if match1:
        realwritetime = match1.group()
    try:
        # 봇 방지 웹사이트 회피
        headers = {"User-Agent": generate_user_agent(device_type="desktop")}
        # 상세 주소 요청 및 응답 수신
        detailRes = requests.get(detailUrl, headers=headers)
    except:
        logger.info(
            "오류가 발생했습니다."
            + detailUrl
        )
        # 오류가 발생하면 errorurl에 추가
        errorurls.append(detailUrl)
        return False

    # HTTP 응답 성공 200
    if detailRes.status_code == 200:
        # 게시글의 HTML을 받아 BeautifulSoup 로 파싱 저장
        detailHtml = detailRes.text
        # HTML을 'lxml(XML, HTML 처리)'를 사용하여 분석
        detailSoup = BeautifulSoup(detailHtml, "lxml")
        # 제목
        title = detailSoup.find("h1").get_text().strip()
        # 작성 날짜/시간
        writetimetemp = detailSoup.find("time")["datetime"]
        # ISO 8601 형식의 시간을 datetime 객체로 변환
        utc_time = datetime.fromisoformat(writetimetemp)
        # UTC 시간을 KST로 변환
        writetime = utc_time.astimezone(kst_timezone)

        # [수정 1-2] 기준 날짜(target_base_date) 결정
        if 'TARGET_DATE' in globals() and TARGET_DATE:
            target_base_date = datetime.strptime(TARGET_DATE, "%Y-%m-%d")
            # 지정된 날짜가 있으면 시간(todaytimeHH)과 관계없이 해당 날짜의 05:00 ~ 익일 04:59를 기준으로 설정
            fromdate = datetime(
                target_base_date.year,
                target_base_date.month,
                target_base_date.day,
                5,
                0,
                0,
            ).astimezone(kst_timezone)

            tomorrow = target_base_date + timedelta(days=1)
            todate = datetime(
                tomorrow.year, tomorrow.month, tomorrow.day, 4, 59, 59
            ).astimezone(kst_timezone)
        else:
            # 2023.07.21 실행 시간에 따라서 기준(시작~종료) 시간을 변경
            if todaytimeHH >= "15":
                # 당일 오전 5시
                fromdate = datetime(
                    datetime.today().year,
                    datetime.today().month,
                    datetime.today().day,
                    6,
                    0,
                    0,
                ).astimezone(kst_timezone)

                # 내일 오전 4시 59분 59초
                tomorrow = datetime.today() + timedelta(days=1)
                todate = datetime(
                    tomorrow.year, tomorrow.month, tomorrow.day, 4, 59, 59
                ).astimezone(kst_timezone)
            else:
                # 전일 오전 5시
                yesterday = datetime.today() - timedelta(days=1)
                fromdate = datetime(
                    yesterday.year, yesterday.month, yesterday.day, 5, 0, 0
                ).astimezone(kst_timezone)

                # 당일 오전 4시 59분 59초
                todate = datetime(
                    datetime.today().year,
                    datetime.today().month,
                    datetime.today().day,
                    4,
                    59,
                    59,
                ).astimezone(kst_timezone)

        # 진행
        logger.info(
            title
            + " - "
            + detailUrl
        )

        # 옵션이 Y인경우 기준대로 작성 대상 확인
        if option == "Y":
            # 처리
            if writetime > todate:
                logger.info(
                    "작성 대상 아님 ("
                    + todate.strftime("%Y-%m-%d %H:%M:%S")
                    + " 이후)"
                )
                return
            elif writetime < fromdate:
                logger.info(
                    "작성 대상 아님 - ("
                    + fromdate.strftime("%Y-%m-%d %H:%M:%S")
                    + " 이전)"
                )
                return
            else:
                logger.info(
                    "작성 대상 맞음 ("
                    + fromdate.strftime("%Y-%m-%d %H:%M:%S")
                    + " ~ "
                    + todate.strftime("%Y-%m-%d %H:%M:%S")
                    + ")"
                )

        # 본문을 찾기 위해 article 태그의 데이터만 사용함
        articleBody = detailSoup.find("div", attrs={"id": "article_1"})
        # 문자열로 변환
        articleBodyText = str(articleBody)
        # 2021.06.29 제외되는 게시글들을 URL로 저장
        # gifmp4_video class가 있을 경우
        articleBodyGIFText2 = articleBodyText.find("gifmp4_video")
        # 링크로 보여줘야 되는 것들에 대한 처리
        if articleBodyGIFText2 > 0:
            logger.info(
                "replace with link"
            )
            # 파일에 저장
            fileContent = (
                '<br><br></br></br><article><h1 style="font-size: 2em; line-height: 1.3; word-break: keep-all;">' + title + '</h1>'
            )  # 게시글 제목 앞에 <p> 추가, 제목 뒤에 </p> 추가. 2021.01.03 추가
            fileContent += "\n"
            fileContent += (
                "\n"
                + '<a target=_blank href="'
                + detailUrl
                + '">'
                + detailUrl
                + "</a>"
                + "\n"
            )
            fileContent += "\n" + "<br><br></br></br>" + "\n"
            # realwritetime을 key로해서 html코드를 value로 저장
            contentDictionary[realwritetime] = fileContent
            return
        try:
            n = detailUrllist.index(detailUrl) + 1
        except ValueError:
            n = 1 # 찾을 수 없는 경우 기본값
        # 게시글 머릿말/꼬리말 설정
        articleHeader = f'<div id="article_{n}" class="article-content">'
        articleTail = "</div></article>"
        # 01 게시글 앞에 머릿말 추가
        articleString = articleHeader
        # 20233.07.10 유튜브 키 리스트 초기화
        youtubekeylist = []
        # 02 article 태그 안에서 <p>태그들을 찾아서 저장함

        # p 로 처리하는 방식에서 문제가 많아 child 방식으로 변경
        for pLine in articleBody.div.children:
            # 2024.10.21 "<p> </p>"인 경우 다음으로 진행
            if str(pLine) == "<p> </p>":
                continue
            # 2023.11.11 "<p></p>"인 경우 다음으로 진행
            if str(pLine) == "<p></p>":
                continue
            # 2023.11.24 <ins 존재할 경우 다음으로 진행
            # 2023.11.29 -1 조건 추가
            if pLine.find("ins") is not None and pLine.find("ins") != -1:
                continue
            try:
                # 2023.11.24 title이 Advertisement 있으면 다음으로 진행
                if pLine["title"] == "Advertisement":
                    continue
            except:
                pass
            try:
                # 2024.10.19 fontawesome 있으면 다음으로 진행
                for pLineimg_tag in pLine.find_all("img"):
                    if pLineimg_tag.get("src", "").startswith(
                        "../../common/fontawesome"
                    ):
                        pLineimg_tag.decompose()
            except:
                pass
            # 2024.02.29 불필요 style='width:1px;height:1px;overflow:hidden;' 제외
            try:
                if (
                    pLine["style"] == "width:1px;height:1px;overflow:hidden;"
                    and pLine.get_text().strip() == ""
                ):
                    continue
            except:
                pass
            # 2023.11.29 불필요 <p style="text-align:center;"></p> 제외
            try:
                if (
                    pLine.get("style") == "text-align:center;"
                    and pLine.get_text().strip() == ""
                ):
                    # img 태그 또는 video 태그가 있으면 다음 pLine으로 진행하지 않음
                    if not pLine.find("img") and not pLine.find("video"):
                        continue
            except:
                pass

            # img 태그의 속성 중 src만 남기기
            try:
                if pLine.name == "img":
                    src = pLine.get("src")
                    pLine.attrs = {} # 모든 속성 지우기
                    if src:
                        pLine["src"] = src
                for img in pLine.find_all("img"):
                    src = img.get("src")
                    img.attrs = {}
                    if src:
                        img["src"] = src
            except:
                pass

            # video 태그의 속성 중 src, controls, width, muted, autoplay, loop, playsinline 남기기
            # 2026.04.30 muted, autoplay, loop, playsinline 속성 보존 추가
            # 2026.05.01 controls 유무 관계없이 width="100%" 항상 추가
            try:
                if pLine.name == "video":
                    src = pLine.get("src")
                    has_controls = "controls" in pLine.attrs
                    controls_val = pLine.get("controls")
                    has_muted = "muted" in pLine.attrs
                    has_autoplay = "autoplay" in pLine.attrs
                    has_loop = "loop" in pLine.attrs
                    has_playsinline = "playsinline" in pLine.attrs

                    pLine.attrs = {}  # 모든 속성 지우기

                    if src:
                        pLine["src"] = src
                    if has_controls:
                        pLine["controls"] = controls_val if controls_val is not None else ""
                    pLine["width"] = "100%"          # ← else 없애고 항상 넣기
                    if has_muted:
                        pLine["muted"] = ""
                    if has_autoplay:
                        pLine["autoplay"] = ""
                    if has_loop:
                        pLine["loop"] = ""
                    if has_playsinline:
                        pLine["playsinline"] = ""

                for video in pLine.find_all("video"):
                    src = video.get("src")
                    has_controls = "controls" in video.attrs
                    controls_val = video.get("controls")
                    has_muted = "muted" in video.attrs
                    has_autoplay = "autoplay" in video.attrs
                    has_loop = "loop" in video.attrs
                    has_playsinline = "playsinline" in video.attrs

                    video.attrs = {}  # 모든 속성 지우기

                    if src:
                        video["src"] = src
                    if has_controls:
                        video["controls"] = controls_val if controls_val is not None else ""
                    video["width"] = "100%"          # ← else 없애고 항상 넣기
                    if has_muted:
                        video["muted"] = ""
                    if has_autoplay:
                        video["autoplay"] = ""
                    if has_loop:
                        video["loop"] = ""
                    if has_playsinline:
                        video["playsinline"] = ""
            except:
                pass
            # 2023.11.11 video를 p로 감싸기
            try:
                if pLine.name == "video":
                    pLine = pLine.wrap(detailSoup.new_tag("p"))
            except:
                pass
            # 2023.11.11 img를 p로 감싸기
            try:
                if pLine.name == "img":
                    pLine = pLine.wrap(detailSoup.new_tag("p"))
            except:
                pass
            # tag 없는 일반 문자열만 있을 경우 .select() 실행시 오류 발생하여 분기 처리
            try:
                if isinstance(pLine, NavigableString):
                    # 2023.11.09 '\n'이 아닐 경우에만 처리
                    if pLine == "\n":
                        continue
                    else:
                        pLine = "<div><span>" + pLine + "</span></div>"
            except:
                pass
            try:
                # https://aagag.com/issue 시작하는 a 링크인 경우 다음으로 진행
                if pLine.find("a")["href"].startswith("https://aagag.com/issue"):
                    continue
            except:
                pass
            # 유튜브 주소를 찾아서 링크 url 변경 처리, 유튜브 주소 없을경우는 변경없이 저장
            pLineText = str(pLine)
            # 유튜브 짧은 주소 접두어
            utubeShrotUrlIndex = pLineText.find("https://youtu.be/")
            # 유튜브 긴 주소 접두어
            utubeUrlIndex = pLineText.find("https://youtube.com/watch?v=")
            # 유튜브 www 긴 주소 접두어
            utubewwwUrlIndex = pLineText.find("https://www.youtube.com/watch?v=")
            # 유튜브 모바일 긴 주소 접두어
            utubemobileUrlIndex = pLineText.find("https://m.youtube.com/watch?v=")
            # 유튜브 shorts 주소 접두어
            utubeshortsUrlIndex = pLineText.find("https://youtube.com/shorts/")
            # 유튜브 shorts 긴 주소 접두어
            utubewwwshortsUrlIndex = pLineText.find("https://www.youtube.com/shorts/")
            # 2021.01.03 유튜브 키값 초기화 추가
            utubeKey = ""
            # 2021.01.03 유튜브 키값 초기화 추가
            utubeKeyIndex = 0

            # 유튜브 주소 길이 판단
            if utubeShrotUrlIndex > 0:
                utubeKeyIndex = pLineText.find("https://youtu.be/")
                # 2021.01.03 파싱 수정 추가
                utubeKey = pLineText[utubeKeyIndex + 17 : utubeKeyIndex + 17 + 11]
                # 유튜브 키값을 iframe 태그로 변경
                # 2022.02.27 p 태그 안에 img와 youtube 같이 있는 경우 감안하여 pLine에 iframe tag 추가
                tempStr = (
                    pLineText
                    + '<p><iframe style="width:560; height:315px" src="https://www.youtube.com/embed/'
                    + utubeKey
                    + '?rel=0&vq=hd1080" frameborder="0" allowfullscreen></iframe>'
                )
            elif utubeUrlIndex > 0:
                utubeKeyIndex = pLineText.find("https://youtube.com/watch?v=")
                # 2021.01.03 파싱 수정 추가
                utubeKey = pLineText[utubeKeyIndex + 28 : utubeKeyIndex + 28 + 11]
                # 유튜브 키값을 iframe 태그로 변경
                # 2022.02.27 p 태그 안에 img와 youtube 같이 있는 경우 감안하여 pLine에 iframe tag 추가
                tempStr = (
                    pLineText
                    + '<p><iframe style="width:560; height:315px" src="https://www.youtube.com/embed/'
                    + utubeKey
                    + '?rel=0&vq=hd1080" frameborder="0" allowfullscreen></iframe>'
                )
            elif utubewwwUrlIndex > 0:
                utubeKeyIndex = pLineText.find("https://www.youtube.com/watch?v=")
                # 2021.01.18 파싱 추가
                utubeKey = pLineText[utubeKeyIndex + 32 : utubeKeyIndex + 32 + 11]
                # 유튜브 키값을 iframe 태그로 변경
                # 2022.02.27 p 태그 안에 img와 youtube 같이 있는 경우 감안하여 pLine에 iframe tag 추가
                tempStr = (
                    pLineText
                    + '<p><iframe style="width:560; height:315px" src="https://www.youtube.com/embed/'
                    + utubeKey
                    + '?rel=0&vq=hd1080" frameborder="0" allowfullscreen></iframe>'
                )
            elif utubemobileUrlIndex > 0:
                utubeKeyIndex = pLineText.find("https://m.youtube.com/watch?v=")
                # 2023.02.16 파싱 추가
                utubeKey = pLineText[utubeKeyIndex + 30 : utubeKeyIndex + 30 + 11]
                # 유튜브 키값을 iframe 태그로 변경
                tempStr = (
                    pLineText
                    + '<p><iframe style="width:560; height:315px" src="https://www.youtube.com/embed/'
                    + utubeKey
                    + '?rel=0&vq=hd1080" frameborder="0" allowfullscreen></iframe>'
                )
            elif utubeshortsUrlIndex > 0:
                utubeKeyIndex = pLineText.find("https://youtube.com/shorts/")
                # 2022.10.07 파싱 추가
                utubeKey = pLineText[utubeKeyIndex + 27 : utubeKeyIndex + 27 + 11]
                # 유튜브 키값을 iframe 태그로 변경
                tempStr = (
                    pLineText
                    + '<p><iframe style="width:315; height:560px" src="https://www.youtube.com/embed/'
                    + utubeKey
                    + '?rel=0&vq=hd1080" frameborder="0" allowfullscreen></iframe>'
                )
            elif utubewwwshortsUrlIndex > 0:
                utubeKeyIndex = pLineText.find("https://www.youtube.com/shorts/")
                # 2022.10.07 파싱 추가
                utubeKey = pLineText[utubeKeyIndex + 31 : utubeKeyIndex + 31 + 11]
                # 유튜브 키값을 iframe 태그로 변경
                tempStr = (
                    pLineText
                    + '<p><iframe style="width:315; height:560px" src="https://www.youtube.com/embed/'
                    + utubeKey
                    + '?rel=0&vq=hd1080" frameborder="0" allowfullscreen></iframe>'
                )
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
            # 구. 트위터 주소 찾기
            try:
                # 2023.03.14 추가
                if "https://twitter.com/" in pLine.find("a")["href"]:
                    tempStr = (
                        pLineText
                        + '<p><blockquote class="twitter-tweet" lang="en"><a href="'
                        + pLine.find("a")["href"]
                        + '"></a></blockquote><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'
                    )
            except:
                pass
            # X 주소 찾기
            try:
                # 2024.02.17 추가
                if "https://x.com/" in pLine.find("a")["href"]:
                    tempStr = (
                        pLineText
                        + '<p><blockquote class="twitter-tweet" lang="en"><a href="'
                        + pLine.find("a")["href"].replace(
                            "https://x.com/", "https://twitter.com/"
                        )
                        + '"></a></blockquote><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>'
                    )
            except:
                pass
            # 트위터 iframe 찾기
            try:
                # 2023.08.17 추가
                if "ed-twitter-div" in pLineText:
                    # 제외 처리
                    continue
            except:
                pass
            # ggoorr video 접두어
            ggoorrvideoIndex = pLineText.find('src="/files/')

            # ggoorr video 존재 확인
            if ggoorrvideoIndex > 0:
                # 전체 URL로 변경
                pLineText = pLineText.replace(
                    'src="/files/', 'src="https://ggoorr.net/files/'
                )
                tempStr = pLineText
            # 줄 끝에 줄 바꿈 처리
            # 2023.12.20 pLine 내에 처리 부분 포함 되어 있어서 다시 처리 추가
            articleString += re.sub(r"<p>\xa0*</p>|\xa0|\n", "", tempStr) + "\n"
        # 03 게시글 끝에 꼬릿말 추가
        articleString += articleTail
        # 04 cdn.ggoorr.net은 프록시 서버 경유
        articleString = articleString.replace(
            "https://cdn.ggoorr.net",
            "https://t1.daumcdn.net/thumb/R1024x0/?fname=https://cdn.ggoorr.net",
        )
        # 2021.02.27 05.제목이 포함된 내용 삭제하기
        # 2021.03.07 05-02 제목과 100% 동일한 본문 내용 삭제하기
        articleString = articleString.replace(title, "")
        # 2023.03.15 escape 문자 처리 위해 html.escape 추가
        articleString = articleString.replace(html.escape(title), "")
        # 파일에 저장
        # 2021.01.03 게시글 제목 앞에 <p> 추가, 제목 뒤에 </p> 추가.
        fileContent = '<article><h1 style="font-size: 2em; line-height: 1.3; word-break: keep-all;">' + title + '</h1>'
        fileContent += "\n"
        fileContent += articleString
        fileContent += "\n"
        # writetimetemp + realwritetime을 key로해서 html코드를 value로 저장
        contentDictionary[writetimetemp + ":" + realwritetime] = fileContent
    else:
        logger.error(">>>> GET ERROR.....")
    # 대기
    time.sleep(waittime)


# 게시판 목록 처리 함수 : 게시글 목록에서 해당 게시물이 작성 대상인 경우 게시글 상세 처리(getDetail)를 호출
# 게시글 처리 대상 - 전일 오전 7시 ~ 당일 오전 6시 59분 59초
def searchList(page):

    logger.info(
        " ========== "
        + str(page)
        + " page start =========="
    )
    # 봇 방지 웹사이트 회피
    headers = {"User-Agent": generate_user_agent(device_type="desktop")}
    res = requests.get(GGOORR_DETAIL_URL + str(page), headers=headers)

    if res.status_code == 200:
        # 응답 html코드를 text로 변환
        html = res.text
        # HTML을 'lxml(XML, HTML 처리)'를 사용하여 분석
        soup = BeautifulSoup(html, "lxml")
        listdocument = soup.find("div", attrs={"class": "list-document"})
        # 2022.07.24 가져오는 방식 변경
        listdocumentlis = listdocument.find_all("li")
        # tr - 개별 게시글 확인
        for listdocumentli in listdocumentlis:
            # 중간 광고 있으면 다음으로 진행
            if listdocumentli["class"] == ["code-list-middle"]:
                continue
            # 변수 초기화
            detailUrl = ""

            # URL
            detailUrl = GGOORR_MAIN_URL + listdocumentli.find("a")["href"]
            # 2023.03.09 정확한 시간 파악 위해서 url 먼저 수집
            detailUrllist.append(detailUrl)
        return True
    else:
        logger.error(
            GGOORR_DETAIL_URL
            + str(page)
            + " >>>> GET ERROR....."
        )
    # 대기
    time.sleep(waittime)


# 데이터 정렬하여 파일에 저장 처리
def SaveSortedContentDictionary():
    # 딕셔너리는 key로 정렬하면 튜플 형태의 리스트가 됨
    sortedKeyList = sorted(contentDictionary.items())
    # 정렬 후 value를 파일에 저장
    for tuplekey, tuplevalue in sortedKeyList:
        f.write(str(tuplevalue))

    if f is not None:
        f.close
        logger.info(
            "fileContent write OK "
        )


# 메인 시작 : 1-15 페이지까지 for loop
def startCrawlering():
    # 시간1
    datetime1 = datetime.now()
    logger.info("Starting")

    # 페이지 탐색 범위 결정 로직
    if 'TARGET_DATE' in globals() and TARGET_DATE:
        # 특정 날짜 지정 모드: 설정된 시작~종료 페이지 사용
        s_page = TARGET_START_PAGE
        e_page = TARGET_END_PAGE
        logger.info(f"Target Date Mode: {TARGET_DATE} (Page {s_page} ~ {e_page})")
    else:
        # 일반 모드 (매일 실행): 1 ~ 10 페이지
        s_page = 1
        e_page = 10
        logger.info(f"Daily Routine Mode (Page {s_page} ~ {e_page})")

    # 결정된 범위로 검색 수행
    for page in range(s_page, e_page + 1):
        searchList(page)

    logger.info("Starting Crawling")

    # 크롤링 시작
    for detailUrl in detailUrllist:
        logger.info(
            str(detailUrllist.index(detailUrl) + 1)
            + "/"
            + str(len(detailUrllist))
        )
        getDetail(detailUrl, "Y")
    logger.info("Ending Crawling")

    # 에러 url들이 있을 경우 크롤링 시작
    if len(errorurls) != 0:
        logger.info(
            "Starting Error Crawling"
        )
        # 에러 url들이 사라질 때까지 반복
        while True:
            # 에러 url 가져오기
            for errorurl in errorurls[:]:
                logger.info(
                    str(errorurls.index(errorurl))
                    + "/"
                    + str(len(errorurls))
                )
                # 크롤링 시작
                if False != getDetail(errorurl, "Y"):
                    # 정상 처리 되면 errorurls에서 에러 url 삭제
                    errorurls.remove(errorurl)
            # 에러 url들이 없는 것을 확인
            if len(errorurls) == 0:
                # 에러 url들에 대한 크롤링 종료
                break
        logger.info("Ending Error Crawling")
    # 데이터 정렬하여 파일에 저장 처리
    SaveSortedContentDictionary()
    # 시간1과 시간2의 차이를 구한다
    datetime2 = datetime.now()
    logger.info("Ending"
    )
    logger.info(datetime2 - datetime1)


tempurllist = [
    "https://ggoorr.net/all/17818755",
]
# # 임시 작업일 경우 아래 4개줄 주석 해제
# for tempurl in tempurllist:
#     getDetail(tempurl, 'N')
# SaveSortedContentDictionary()
# sys.exit()

# 크롤링 시작
startCrawlering()
