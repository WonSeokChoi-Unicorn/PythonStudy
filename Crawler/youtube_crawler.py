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
# 카카오 번역
# pip install kakaotrans
from kakaotrans import Translator
import pytz
import json
import asyncio
import aiohttp

# 시간1
datetime1 = datetime.now()
print(datetime1.strftime('%Y-%m-%d %H:%M:%S') + " - Starting")

# 미국 태평양 시간(PST, -07:00)
pst = pytz.timezone('America/Los_Angeles')
# 한국 시간(KST, +09:00)
kst = pytz.timezone('Asia/Seoul')

# 대기 시간
waittimedot5 = 0.5

# iframe 태그 생성을 위해 폭과 높이를 설정
width = '560'
height = '315'

# 한국어로 구글 번역할 영어 채널 리스트
englishchannel = ['Kurzgesagt – In a Nutshell', 'TED-Ed', 'Vox']

# 전일 오전 7시
yesterday = datetime.today() - timedelta(days = 1)
fromdate = datetime(yesterday.year, yesterday.month, yesterday.day, 7, 0, 0).astimezone(kst)

# 당일 오전 6시 59분 59초
todate = datetime(datetime.today().year, datetime.today().month, datetime.today().day, 6, 59, 59).astimezone(kst)

# 파일명을 날짜로 이용
nowDate = datetime.now()

# 카카오 번역 선언
translator = Translator()

# 비동기 fetch 함수 정의
async def fetch(session, yt_videoid, ):
    # HTML 요청
    async with session.get(yt_videoid) as response2:
        if response2.status == 200:
            Html2 = await response2.text()
            Soup2 = BeautifulSoup(Html2, 'lxml')

            # meta uploadDate 찾기
            yt_datePublished = Soup2.find('meta', attrs = {"itemprop" : "datePublished"})['content']
            yt_datePublisheddt = datetime.strptime(yt_datePublished, '%Y-%m-%dT%H:%M:%S%z')

            # PST 기준으로 datetime 객체 설정
            yt_datePublisheddtpst = yt_datePublisheddt.astimezone(pst)
            yt_datePublisheddtkst = yt_datePublisheddtpst.astimezone(kst)

            # 제목 추출
            yt_title = Soup2.find('title').get_text().strip().replace(" - YouTube", "")

            # 채널 찾기
            channelname = Soup2.find('link', attrs = {"itemprop" : "name"})['content']

            # 영어 채널일 경우 제목 번역
            if channelname in englishchannel:
                yt_title = translator.translate(yt_title, src = 'en', tgt = 'kr')

            # 날짜 기준 체크
            if yt_datePublisheddtkst > todate:
                print("작성 대상 아님 (당일 7시 이후)")
                print(yt_title)
                print(yt_videoid)
                print(yt_datePublisheddtkst.strftime("%Y-%m-%d %H:%M:%S"))
            elif yt_datePublisheddtkst <= fromdate:
                print("작성 대상 아님 (전일 7시 이전)")
                print(yt_title)
                print(yt_videoid)
                print(yt_datePublisheddtkst.strftime("%Y-%m-%d %H:%M:%S"))
            else:
                print("작성 대상 맞음 (전일 7시 ~ 당일 6시 59분 59초)")
                print(yt_title)
                print(yt_videoid)
                print(yt_datePublisheddtkst.strftime("%Y-%m-%d %H:%M:%S"))

                # iframe 생성
                iframe = yt.video(yt_videoid, width = width, height = height)

                # 파일에 저장할 내용
                tempstr = f"<p>{yt_title}</p>\n"
                tempstr += f'<p><a target=_blank href="{yt_videoid}">{yt_videoid}</a></p>\n'
                tempstr += f"<p>{iframe}</p>\n"

                return tempstr
        return None

async def main(urllist):
    async with aiohttp.ClientSession() as session1:
        for url in urllist:
            response1 = await session1.get(url)
            if response1.status == 200:
                Html1 = await response1.text()
                Soup1 = BeautifulSoup(Html1, 'lxml')
                channelname = Soup1.find('title').get_text().strip().replace(" - YouTube", "")

                # 채널명은 반복문 전 파일에 1번만 저장하도록
                channelheader = "<p>" + "#####*****" + channelname + "</p>"
                channelheader += "\n"

                print("##################################################################")
                print(channelname)
                print("##################################################################")

                fileContent = channelheader

                if fileContent:
                    filename = f"{datetime.now().strftime('%Y-%m-%d')}_youtube.txt"
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(fileContent)
                        print(f"File {filename} updated.")

                del fileContent

                yt_scripttags = Soup1.find_all('script', string = re.compile(r'ytInitialData'))
                if yt_scripttags:
                    yt_datascript = yt_scripttags[0].string
                    yt_initialdata = re.search(r'ytInitialData\s*=\s*({.*?});', yt_datascript, re.DOTALL)

                    if yt_initialdata:
                        yt_initialdatajsonstr = yt_initialdata.group(1)
                        yt_initialdata = json.loads(yt_initialdatajsonstr)
                        yt_videoids = []

                        yt_richgridrenderer = yt_initialdata.get("contents", {}).get("twoColumnBrowseResultsRenderer", {}).get("tabs", [])[1].get("tabRenderer", {}).get("content", {}).get("richGridRenderer", {})
                        yt_gridcontents = yt_richgridrenderer.get("contents", [])

                        for item in yt_gridcontents:
                            yt_richitemrenderer = item.get("richItemRenderer", {})
                            yt_videorenderer = yt_richitemrenderer.get("content", {}).get("videoRenderer", {})
                            yt_videoid = yt_videorenderer.get("videoId", None)
                            if yt_videoid:
                                yt_videoids.append("https://www.youtube.com/watch?v=" + yt_videoid)

                        tasks = [fetch(session1, yt_videoid) for yt_videoid in yt_videoids]
                        results = await asyncio.gather(*tasks)

                        fileContent = "\n".join(filter(None, results))
                        if fileContent:
                            filename = f"{datetime.now().strftime('%Y-%m-%d')}_youtube.txt"
                            with open(filename, 'a', encoding='utf-8') as f:
                                f.write(fileContent)
                                print(f"File {filename} updated.")
# 메인 실행
if __name__ == "__main__":
    # 추출할 유튜브 채널의 동영상 탭
    urllist = [
            'https://www.youtube.com/c/14FMBC/videos',
            'https://www.youtube.com/c/BMan%EC%82%90%EB%A7%A8/videos',
            'https://www.youtube.com/@Btv%EC%9D%B4%EB%8F%99%EC%A7%84%EC%9D%98%ED%8C%8C%EC%9D%B4%EC%95%84%ED%82%A4%EC%95%84/videos',
            'https://www.youtube.com/c/movietrip%EB%AC%B4%EB%B9%84%ED%8A%B8%EB%A6%BD/videos',
            'https://www.youtube.com/channel/UC5aNQ65ADb02zEJxzb_zmYQ/videos',
            'https://www.youtube.com/user/rladndgussla/videos',
            'https://www.youtube.com/@%EA%B9%80%EB%B0%94%EB%B9%84/videos',
            'https://www.youtube.com/c/%EB%8F%88%EB%A6%BD%EB%A7%8C%EC%84%B8/videos',
            'https://www.youtube.com/@ddeunddeun/videos',
            'https://www.youtube.com/c/%EB%A1%9C%EC%9D%B4%EC%96%B4%ED%94%84%EB%A0%8C%EC%A6%88lawyerfriends/videos',
            'https://www.youtube.com/c/Owlsreview/videos',
            'https://www.youtube.com/@nicekiyoung/videos',
            'https://www.youtube.com/@nofeetbird/videos',
            'https://www.youtube.com/@red12734/videos',
            'https://www.youtube.com/@443RohmoohyunFoundation/videos',
            'https://www.youtube.com/@%EC%82%AC%EB%AC%BC%EA%B6%81%EC%9D%B4/videos',
            'https://www.youtube.com/@sebasi15/videos',
            'https://www.youtube.com/@%EC%84%B8%EB%AA%A8%EC%A7%80/videos',
            'https://www.youtube.com/@Sherlock_HJ/videos',
            'https://www.youtube.com/@%EC%86%8C%EB%B9%84%EB%8D%94%EB%A8%B8%EB%8B%88/videos',
            'https://www.youtube.com/@syukaworld/videos',
            'https://www.youtube.com/@syukaworld-comics/videos',
            'https://www.youtube.com/@ens8388/videos',
            'https://www.youtube.com/@yuna_ogura/videos',
            'https://www.youtube.com/@OMG_electronics/videos',
            'https://www.youtube.com/@autoview2009/videos',
            'https://www.youtube.com/@jiaxi_lee/videos',
            'https://www.youtube.com/@%EC%B0%A8%EC%82%B0%EC%84%A0%EC%83%9D%EB%B2%95%EB%A5%A0%EC%83%81%EC%8B%9D-d6j/videos',
            'https://www.youtube.com/@geniussklee/videos',
            'https://www.youtube.com/@geniussklee_act2838/videos',
            'https://www.youtube.com/@choemazon/videos',
            'https://www.youtube.com/@TTimesTV/videos',
            'https://www.youtube.com/@%ED%94%BD%EC%B8%84/videos',
            'https://www.youtube.com/@HanSangKi/videos',
            'https://www.youtube.com/@hansangki9105/videos',
            'https://www.youtube.com/@TEDEd/videos',
            'https://www.youtube.com/@kurzgesagt/videos',
            'https://www.youtube.com/@Vox/videos',
            'https://www.youtube.com/c/LGElectronicsKorea/videos',
            'https://www.youtube.com/user/LGSTORY/videos',
            'https://www.youtube.com/c/DisneyMovieKr/videos',
            'https://www.youtube.com/c/MarvelKorea/videos',
            'https://www.youtube.com/@ArgentUnicorn/videos',
            'https://www.youtube.com/channel/UC7A1QdDXcu3zu_KS8DddL1A/videos',
            'https://www.youtube.com/@bamgongwon/videos',
            'https://www.youtube.com/@haeinleezy/videos',
            ]

    # TEST
    # urllist = [
    # 'https://www.youtube.com/user/dlrldud1111/videos'
    # ]

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main(urllist))
    # 시간1과 시간2의 차이를 구한다
    datetime2 = datetime.now()
    print(datetime1.strftime('%Y-%m-%d %H:%M:%S') + " ~ " + datetime2.strftime('%Y-%m-%d %H:%M:%S') + " - Ending")
    print(datetime2 - datetime1)