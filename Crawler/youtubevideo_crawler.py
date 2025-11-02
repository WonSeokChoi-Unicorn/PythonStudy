from selenium import webdriver
from bs4 import BeautifulSoup
import time
from datetime import datetime
import re
import json
import requests
import logging

# 로거 생성
logger = logging.getLogger("YoutubeVideosLogger")
logger.setLevel(logging.INFO)

# 출력 형식 설정
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# 콘솔 출력 설정
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
stream_handler.setLevel(logging.INFO)

# 날짜별 로그 파일 생성
log_file = (
    f"D:\\Python\\LOG\\{datetime.now().strftime('%Y%m%d%H%M%S')}_youtubevideos.log"
)
file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
file_handler.setLevel(logging.INFO)

# 대기 시간 설정
WAIT_TIME_LONG = 3

# 크롤링 카운트 초기화
count = 0

# 대상 채널 목록 - 동영상 탭과 라이브 탭 모두 포함
youtube_channels = [
    {
        "url": "https://www.youtube.com/@Btv%EC%9D%B4%EB%8F%99%EC%A7%84%EC%9D%98%ED%8C%8C%EC%9D%B4%EC%95%84%ED%82%A4%EC%95%84/videos",
        "type": "videos",
    },
    # {
    #     "url": "https://www.youtube.com/@Btv%EC%9D%B4%EB%8F%99%EC%A7%84%EC%9D%98%ED%8C%8C%EC%9D%B4%EC%95%84%ED%82%A4%EC%95%84/streams",
    #     "type": "streams"
    # }
]

# 파일 설정
current_date = datetime.now().strftime("%Y-%m-%d")
output_file = f"{current_date}_youtubevideolist.txt"

# Selenium 설정
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 헤드리스 모드 활성화
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)


def get_continuation_token(contents):
    """Continuation 토큰 추출 함수"""
    for item in reversed(contents):
        if "continuationItemRenderer" in item:
            return item["continuationItemRenderer"]["continuationEndpoint"][
                "continuationCommand"
            ]["token"]
    return None


def fetch_additional_videos(token, session, api_key, context):
    """추가 영상 데이터 요청 함수"""
    api_url = f"https://www.youtube.com/youtubei/v1/browse?key={api_key}"
    payload = {"context": context, "continuation": token}
    response = session.post(api_url, json=payload)
    return response.json()


def extract_video_data(item, content_type):
    """영상 데이터 추출 함수"""
    global count

    # richItemRenderer 확인
    if "richItemRenderer" not in item:
        return None

    # 콘텐츠 타입에 따라 다른 처리
    if content_type == "videos":
        video_renderer = item["richItemRenderer"]["content"].get("videoRenderer", {})
    elif content_type == "streams":
        video_renderer = item["richItemRenderer"]["content"].get("videoRenderer", {})
    else:
        return None

    if not video_renderer:
        return None

    # 공통 데이터 추출
    video_id = video_renderer.get("videoId")
    if not video_id:
        return None

    title = video_renderer.get("title", {}).get("runs", [{}])[0].get("text", "No Title")

    # 콘텐츠 타입 정보 추가
    content_type_label = "라이브" if content_type == "streams" else "동영상"

    # count 증가
    count += 1
    logger.info(
        f"카운트: {count}, 타입: {content_type_label}, 영상 ID: {video_id}, 제목: {title}"
    )

    return f"https://www.youtube.com/watch?v={video_id}, [{content_type_label}] {title} 영상에 대해서 한국어로 자세히 요약해 줘\n"


def process_videos(contents, file_handle, content_type):
    """영상 데이터 처리 및 저장 함수"""
    for item in contents:
        video_data = extract_video_data(item, content_type)
        if video_data:
            file_handle.write(video_data)


def find_tab_index(initial_data, content_type):
    """탭 인덱스 찾기 함수"""
    tabs = initial_data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"]
    for i, tab in enumerate(tabs):
        if "tabRenderer" in tab:
            tab_renderer = tab["tabRenderer"]
            if content_type == "videos" and tab_renderer.get("title") == "동영상":
                return i
            elif content_type == "streams" and tab_renderer.get("title") == "라이브":
                return i
    return 1  # 기본값으로 1 반환 (일반적으로 동영상 탭)


def get_contents_from_tab(initial_data, tab_index):
    """탭에서 콘텐츠 추출 함수"""
    tab = initial_data["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][tab_index]

    # 선택된 탭인지 확인
    if (
        "tabRenderer" in tab
        and "selected" in tab["tabRenderer"]
        and tab["tabRenderer"]["selected"]
    ):
        # 라이브 탭이나 동영상 탭의 콘텐츠 구조 처리
        if "richGridRenderer" in tab["tabRenderer"]["content"]:
            return tab["tabRenderer"]["content"]["richGridRenderer"]["contents"]

    # 선택되지 않은 탭이면 API 요청 필요
    return None


def crawl_channel(channel_info, file_handle):
    """채널 크롤링 메인 함수"""
    url = channel_info["url"]
    content_type = channel_info["type"]

    driver.get(url)
    # 초기 페이지 로딩 대기
    time.sleep(WAIT_TIME_LONG)

    # 초기 데이터 수집
    soup = BeautifulSoup(driver.page_source, "html.parser")
    script_tag = soup.find("script", string=re.compile("ytInitialData"))

    if not script_tag:
        logger.info(f"{content_type} 탭의 초기 데이터를 찾을 수 없습니다.")
        return

    initial_data = json.loads(
        re.search(r"ytInitialData\s*=\s*({.*?});", script_tag.string).group(1)
    )

    # API 키 추출
    api_key_match = re.search(r'"INNERTUBE_API_KEY":"([^"]+)"', str(soup))
    if not api_key_match:
        logger.info("API 키를 찾을 수 없습니다.")
        return

    api_key = api_key_match.group(1)

    # 컨텍스트 설정
    context = initial_data.get(
        "context",
        {
            "client": {
                "hl": "ko",
                "gl": "KR",
                "clientName": "WEB",
                "clientVersion": "2.20210721.00.00",
            }
        },
    )

    # 탭 인덱스 찾기
    tab_index = find_tab_index(initial_data, content_type)

    # 콘텐츠 가져오기
    contents = get_contents_from_tab(initial_data, tab_index)

    if not contents:
        logger.info(f"{content_type} 탭의 콘텐츠를 찾을 수 없습니다.")
        return

    # 초기 영상 데이터 처리
    process_videos(contents, file_handle, content_type)

    # 세션 설정
    session = requests.Session()

    # Continuation 토큰 처리 루프
    while True:
        token = get_continuation_token(contents)
        if not token:
            break

        # 추가 데이터 요청
        try:
            response_data = fetch_additional_videos(token, session, api_key, context)
            if "onResponseReceivedActions" not in response_data:
                logger.info("추가 데이터 응답에 onResponseReceivedActions가 없습니다.")
                break

            new_contents = response_data["onResponseReceivedActions"][0][
                "appendContinuationItemsAction"
            ]["continuationItems"]
            process_videos(new_contents, file_handle, content_type)
            contents = new_contents
        except Exception as e:
            logger.error(f"추가 데이터 처리 중 오류 발생: {str(e)}")
            break


# 메인 실행 블록
if __name__ == "__main__":
    with open(output_file, "a", encoding="utf-8") as f:
        for channel in youtube_channels:
            logger.info(f"크롤링 시작: {channel['url']} ({channel['type']})")
            crawl_channel(channel, f)

    driver.quit()
    logger.info("크롤링 완료. 결과 파일: " + output_file)
