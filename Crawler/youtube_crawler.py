# <p>채널명</p><p>제목</p><p><a>URL</a></p><p><iframe></p> 로 작성

# BeautifulSoup4를 import 한다.
# pip install beautifulsoup4 --upgrade
# lxml 설치 필요합니다 (pip install lxml)
from bs4 import BeautifulSoup

# 날짜 시간 처리 위해 datetime, timedelta를 import 한다.
from datetime import datetime, timedelta

# iframe TAG 작성을 위해 yt를 import 한다.
# pip install yt-iframe
from yt_iframe import yt

# 숫자만 추출하기 위한 re를 import 한다.
import re
from user_agent import generate_user_agent
# # 카카오 번역
# # pip install kakaotrans
# from kakaotrans import Translator
# 구글 번역
# pip install googletrans-py
from googletrans import Translator
import pytz
import json
import asyncio
import aiohttp
import time
from pathlib import Path

# 시간1
datetime1 = datetime.now()
print(datetime1.strftime("%Y-%m-%d %H:%M:%S") + " - Starting")

# 미국 태평양 시간(PST, -07:00)
pst = pytz.timezone("America/Los_Angeles")
# 한국 시간(KST, +09:00)
kst = pytz.timezone("Asia/Seoul")

# 대기 시간
waittimedot5 = 0.5
waittime5 = 5

# iframe 태그 생성을 위해 폭과 높이를 설정
width = "560"
height = "315"

# 한국어로 구글 번역할 영어 채널 리스트
englishchannel = ["Kurzgesagt – In a Nutshell", "TED-Ed", "Vox", "Nightshift – Kurzgesagt After Dark"]

# 전일 오전 6시
yesterday = datetime.today() - timedelta(days=1)
fromdate = datetime(yesterday.year, yesterday.month, yesterday.day, 6, 0, 0).astimezone(
    kst
)

# 당일 오전 5시 59분 59초
todate = datetime(
    datetime.today().year, datetime.today().month, datetime.today().day, 5, 59, 59
).astimezone(kst)

# 파일명을 날짜로 이용
nowDate = datetime.now()

# # 카카오 번역 선언
# translator = Translator()
# 구글 번역 선언
translator = Translator()

# 저장 폴더
savefolder = Path("D:/ggoorr")


# 비동기 fetch 함수 정의
async def fetch(
    session,
    yt_videoid,
):
    # HTML 요청
    async with session.get(yt_videoid) as response2:
        if response2.status == 200:
            Html2 = await response2.text()
            Soup2 = BeautifulSoup(Html2, "lxml")

            # meta uploadDate 찾기
            yt_datePublished = Soup2.find("meta", attrs={"itemprop": "datePublished"})[
                "content"
            ]
            yt_datePublisheddt = datetime.strptime(
                yt_datePublished, "%Y-%m-%dT%H:%M:%S%z"
            )

            # PST 기준으로 datetime 객체 설정
            yt_datePublisheddtpst = yt_datePublisheddt.astimezone(pst)
            yt_datePublisheddtkst = yt_datePublisheddtpst.astimezone(kst)

            # 제목 추출
            yt_title = Soup2.find("title").get_text().strip().replace(" - YouTube", "").replace("#shorts", "")

            # 채널 찾기
            channelname = Soup2.find("link", attrs={"itemprop": "name"})["content"]

            # 영어 채널일 경우 제목 번역
            if channelname in englishchannel:
                while True:
                    try:
                        # # 카카오 번역
                        # yt_title = translator.translate(yt_title, src = 'en', tgt = 'kr')
                        # 구글 번역
                        yt_title = translator.translate(
                            yt_title, src="en", dest="ko"
                        ).text
                        break
                    except:
                        time.sleep(waittime5)

            # 날짜 기준 체크
            if yt_datePublisheddtkst > todate:
                print(
                    "작성 대상 아님 (" + todate.strftime("%Y-%m-%d %H:%M:%S") + " 이후)"
                )
                print(yt_title)
                print(yt_videoid)
                print(yt_datePublisheddtkst.strftime("%Y-%m-%d %H:%M:%S"))
            elif yt_datePublisheddtkst <= fromdate:
                print(
                    "작성 대상 아님 ("
                    + fromdate.strftime("%Y-%m-%d %H:%M:%S")
                    + " 이전)"
                )
                print(yt_title)
                print(yt_videoid)
                print(yt_datePublisheddtkst.strftime("%Y-%m-%d %H:%M:%S"))
            else:
                print(
                    "작성 대상 맞음 ("
                    + fromdate.strftime("%Y-%m-%d %H:%M:%S")
                    + " ~ "
                    + todate.strftime("%Y-%m-%d %H:%M:%S")
                    + ")"
                )
                print(yt_title)
                print(yt_videoid)
                print(yt_datePublisheddtkst.strftime("%Y-%m-%d %H:%M:%S"))

                # iframe 생성
                iframe = yt.video(yt_videoid, width=width, height=height)

                # 파일에 저장할 내용
                tempstr = f"<p>{yt_title}</p>\n"
                tempstr += (
                    f'<p><a target=_blank href="{yt_videoid}">{yt_videoid}</a></p>\n'
                )
                tempstr += f"<p>{iframe}</p>\n"

                return tempstr
        return None


async def main(urllist):
    async with aiohttp.ClientSession(headers = headers) as session1:
        for base_url in urllist:
            base_url = base_url.rstrip("/")

            # 1. 채널명 추출을 위해 기본 URL에 먼저 접속
            response1 = await session1.get(base_url)
            if response1.status != 200:
                continue

            Html1 = await response1.text()
            Soup1 = BeautifulSoup(Html1, "lxml")
            try:
                channelname = Soup1.find("title").get_text().strip().replace(" - YouTube", "")
            except:
                channelname = base_url.split("/")[-1]

            # 채널명은 반복문 전 파일에 1번만 저장하도록
            channelheader = "\n" + "#####***** " + channelname + " *****#####\n"
            print("##################################################################")
            print(channelname)
            print("##################################################################")

            filename = savefolder / f"{datetime.now().strftime('%Y-%m-%d')}_youtube.txt"
            with open(filename, "a", encoding="utf-8") as f:
                f.write(channelheader)

            # 2. 채널 내 3가지 탭(videos, streams, shorts) 순차적 크롤링
            for tab_name in ["videos", "streams", "shorts"]:
                url = f"{base_url}/{tab_name}"
                response_tab = await session1.get(url)
                if response_tab.status != 200:
                    continue

                Html_tab = await response_tab.text()
                Soup_tab = BeautifulSoup(Html_tab, "lxml")

                yt_scripttags = Soup_tab.find_all("script", string=re.compile(r"ytInitialData"))
                if not yt_scripttags:
                    continue

                yt_datascript = yt_scripttags[0].string
                yt_initialdata_match = re.search(r"ytInitialData\s*=\s*({.*?});", yt_datascript, re.DOTALL)
                if not yt_initialdata_match:
                    continue

                yt_initialdata = json.loads(yt_initialdata_match.group(1))

                # 접속한 탭(selected=True)의 컨텐츠 데이터 찾기
                yt_tabs = yt_initialdata.get("contents", {}).get("twoColumnBrowseResultsRenderer", {}).get("tabs", [])
                yt_gridcontents = []
                for tab in yt_tabs:
                    tab_renderer = tab.get("tabRenderer", {})
                    if tab_renderer.get("selected", False):
                        content = tab_renderer.get("content", {})
                        if "richGridRenderer" in content:
                            yt_gridcontents = content.get("richGridRenderer", {}).get("contents", [])
                        break

                yt_videoids = []
                for item in yt_gridcontents:
                    yt_richitemrenderer = item.get("richItemRenderer", {})
                    if not yt_richitemrenderer:
                        continue

                    content_item = yt_richitemrenderer.get("content", {})

                    yt_videoid = None
                    is_upcoming = False
                    is_members_only = False

                    # 일반 동영상 및 라이브 스트리밍 처리 (videoRenderer)
                    if "videoRenderer" in content_item:
                        yt_videorenderer = content_item["videoRenderer"]
                        yt_videoid = yt_videorenderer.get("videoId")

                        # 예정된 동영상 확인
                        if "upcomingEventData" in yt_videorenderer:
                            continue

                        thumbnails_overlays = yt_videorenderer.get("thumbnailOverlays", [])
                        is_upcoming = any(
                            overlay.get("thumbnailOverlayTimeStatusRenderer", {}).get("style") == "UPCOMING"
                            for overlay in thumbnails_overlays
                        )
                        if is_upcoming:
                            continue

                        # 회원 전용 확인
                        badges = yt_videorenderer.get("badges", [])
                        for badge in badges:
                            badge_renderer = badge.get("metadataBadgeRenderer", {})
                            style = badge_renderer.get("style", "")
                            if style == "BADGE_STYLE_TYPE_MEMBERS_ONLY" or "회원" in badge_renderer.get("label", ""):
                                is_members_only = True
                                break
                        if is_members_only:
                            continue

                    # 쇼츠 동영상 처리 (shortsLockupViewModel) - 유튜브 구조 변경 대응
                    elif "shortsLockupViewModel" in content_item:
                        shorts_lockup = content_item["shortsLockupViewModel"]
                        url_path = shorts_lockup.get("onTap", {}).get("innertubeCommand", {}).get("commandMetadata", {}).get("webCommandMetadata", {}).get("url", "")

                        if url_path.startswith("/shorts/"):
                            yt_videoid = url_path.replace("/shorts/", "").split("?")[0]
                        else:
                            entity_id = shorts_lockup.get("entityId", "")
                            if entity_id.startswith("shorts-shelf-item-"):
                                yt_videoid = entity_id.replace("shorts-shelf-item-", "")

                    if yt_videoid:
                        # Shorts도 일반 youtube watch 링크로 접근이 가능하여 기존 fetch 함수 재사용 가능
                        yt_videoids.append("https://www.youtube.com/watch?v=" + yt_videoid)

                if not yt_videoids:
                    continue

                # 비동기 정보 수집(기존 fetch 함수 호출)
                tasks = [fetch(session1, yt_videoid) for yt_videoid in yt_videoids]
                results = await asyncio.gather(*tasks)
                fileContent = "\n".join(filter(None, results))

                if fileContent:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(f"--------------- {tab_name} ---------------\n")
                        f.write(fileContent)
                    print(f"[{tab_name}] 탭에서 조건에 맞는 영상 기록 완료")


# 메인 실행
if __name__ == "__main__":
    # 추출할 유튜브 채널의 동영상 탭
    urllist = [
        "https://www.youtube.com/@14FMBC",
        "https://www.youtube.com/@%EC%82%90%EB%A7%A8",
        "https://www.youtube.com/@Btv%EC%9D%B4%EB%8F%99%EC%A7%84%EC%9D%98%ED%8C%8C%EC%9D%B4%EC%95%84%ED%82%A4%EC%95%84",
        "https://www.youtube.com/@Gajoo",
        "https://www.youtube.com/@%EA%B3%A0%EB%AA%BD",
        "https://www.youtube.com/@%EA%B9%80%EB%B0%94%EB%B9%84",
        "https://www.youtube.com/@%EB%A8%B8%EB%8B%88%EC%95%A4%EB%9D%BC%EC%9D%B4%ED%94%84",
        "https://www.youtube.com/@ddeunddeun",
        "https://www.youtube.com/@lawyerfriends",
        "https://www.youtube.com/@%EB%A6%AC%EB%B7%B0%EC%97%89%EC%9D%B4",
        "https://www.youtube.com/@nicekiyoung",
        "https://www.youtube.com/@pyeongsanbooks",
        "https://www.youtube.com/@nofeetbird",
        "https://www.youtube.com/@red12734",
        "https://www.youtube.com/@443RohmoohyunFoundation",
        "https://www.youtube.com/@%EC%82%AC%EB%AC%BC%EA%B6%81%EC%9D%B4",
        "https://www.youtube.com/@sebasi15",
        "https://www.youtube.com/@%EC%84%B8%EB%AA%A8%EC%A7%80",
        "https://www.youtube.com/@Sherlock_HJ",
        "https://www.youtube.com/@%EC%86%8C%EB%B9%84%EB%8D%94%EB%A8%B8%EB%8B%88",
        "https://www.youtube.com/@syukaworld",
        "https://www.youtube.com/@moneymoneycomics",
        "https://www.youtube.com/@ens8388",
        "https://www.youtube.com/@yuna_ogura",
        "https://www.youtube.com/@OMG_electronics",
        "https://www.youtube.com/@autoview2009",
        "https://www.youtube.com/@jiaxi_lee",
        "https://www.youtube.com/@genreismoney",
        "https://www.youtube.com/@%EC%B0%A8%EC%82%B0%EC%84%A0%EC%83%9D%EB%B2%95%EB%A5%A0%EC%83%81%EC%8B%9D-d6j",
        "https://www.youtube.com/@geniussklee",
        "https://www.youtube.com/@geniussklee_act2838",
        "https://www.youtube.com/@choemazon",
        "https://www.youtube.com/@TTimesTV",
        "https://www.youtube.com/@%ED%94%BD%EC%B8%84",
        "https://www.youtube.com/@HanSangKi",
        "https://www.youtube.com/@hansangki9105",
        "https://www.youtube.com/@TEDEd",
        "https://www.youtube.com/@kurzgesagt",
        "https://www.youtube.com/@nightshift_kurzgesagt",
        "https://www.youtube.com/@Vox",
        "https://www.youtube.com/@LGElectronicsKorea",
        "https://www.youtube.com/@LGSTORY",
        "https://www.youtube.com/@DisneyMovieKr",
        "https://www.youtube.com/@MarvelKorea",
        "https://www.youtube.com/@ArgentUnicorn",
        "https://www.youtube.com/@ArgentUnicornPlayground",
        "https://www.youtube.com/@kfoodrecipes",
        "https://www.youtube.com/@bamgongwon",
        "https://www.youtube.com/@haeinleezy",
        "https://www.youtube.com/@%EB%B0%A4%EA%B3%B5%EC%9B%90",
    ]

    # TEST
    # urllist = [
    # 'https://www.youtube.com/user/dlrldud1111/videos'
    # ]
    headers = {"User-Agent" : generate_user_agent(device_type = 'desktop', navigator='chrome'),
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1"}
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main(urllist))
    # 시간1과 시간2의 차이를 구한다
    datetime2 = datetime.now()
    print(
        datetime1.strftime("%Y-%m-%d %H:%M:%S")
        + " ~ "
        + datetime2.strftime("%Y-%m-%d %H:%M:%S")
        + " - Ending"
    )
    print(datetime2 - datetime1)
