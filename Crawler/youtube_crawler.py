import sys
sys.stdout.reconfigure(encoding="utf-8")

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET

from yt_iframe import yt
from user_agent import generate_user_agent
from googletrans import Translator

import asyncio
import aiohttp
import logging
import pytz
import re


# ============================================================
# 로거
# ============================================================

logger = logging.getLogger("YoutubeLogger")
logger.setLevel(logging.INFO)

# 인터프리터 재실행/IDE 재실행 시 핸들러 중복 방지
logger.handlers.clear()

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

log_file = f"D:\\Python\\LOG\\{datetime.now().strftime('%Y%m%d%H%M%S')}_youtube.log"
file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)


# ============================================================
# 설정값
# ============================================================

datetime1 = datetime.now()
logger.info(f"{datetime1:%Y-%m-%d %H:%M:%S} - Starting")

kst = pytz.timezone("Asia/Seoul")

RETRY_MAX = 3
RETRY_WAIT = 5.0
FETCH_TIMEOUT = 30
SESSION_TIMEOUT = 60

# 현재 검증된 안전한 동시 연결 수
CONNECTOR_LIMIT = 5
CONNECTOR_LIMIT_PER_HOST = 5

width = "560"
height = "315"

englishchannel = [
    "Kurzgesagt – In a Nutshell",
    "TED-Ed",
    "Vox",
    "Nightshift – Kurzgesagt After Dark",
]

translator = Translator()
savefolder = Path("D:/ggoorr")
savefolder.mkdir(parents=True, exist_ok=True)

collected_urls: list[str] = []


# ============================================================
# 날짜 범위
# KST 기준: 전일/당일 오전 05:00 ~ 익일/당일 오전 05:00
# ============================================================

now_kst = datetime.now(kst)

if now_kst.hour >= 15:
    fromdate = kst.localize(
        datetime(now_kst.year, now_kst.month, now_kst.day, 5, 0, 0)
    )
    tomorrow = now_kst + timedelta(days=1)
    todate = kst.localize(
        datetime(tomorrow.year, tomorrow.month, tomorrow.day, 5, 0, 0)
    )
else:
    yesterday = now_kst - timedelta(days=1)
    fromdate = kst.localize(
        datetime(yesterday.year, yesterday.month, yesterday.day, 5, 0, 0)
    )
    todate = kst.localize(
        datetime(now_kst.year, now_kst.month, now_kst.day, 5, 0, 0)
    )

logger.info(
    f"[날짜 범위] {fromdate:%Y-%m-%d %H:%M:%S %Z} "
    f"~ {todate:%Y-%m-%d %H:%M:%S %Z}"
)


# ============================================================
# YouTube Atom/RSS 네임스페이스
# ============================================================

ATOM_NS = "http://www.w3.org/2005/Atom"
YT_NS = "http://www.youtube.com/xml/schemas/2015"

NS = {
    "atom": ATOM_NS,
    "yt": YT_NS,
}


# ============================================================
# 공통 HTTP 요청
# ============================================================

async def get_with_retry(session, url, label=""):
    """
    정상 응답 객체를 반환한다.
    호출 측에서 await response.text()로 본문을 모두 읽은 뒤
    response.release()를 호출하도록 한다.
    """
    for attempt in range(1, RETRY_MAX + 1):
        try:
            response = await session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=FETCH_TIMEOUT),
            )
            return response

        except asyncio.TimeoutError:
            logger.error(f"[타임아웃 {attempt}/{RETRY_MAX}] {label or url}")

            if attempt < RETRY_MAX:
                await asyncio.sleep(RETRY_WAIT)

        except aiohttp.ClientConnectionError as e:
            logger.error(
                f"[연결 오류 {attempt}/{RETRY_MAX}] "
                f"{label or url} → {e}"
            )

            if attempt < RETRY_MAX:
                await asyncio.sleep(RETRY_WAIT)

        except Exception as e:
            logger.error(f"[요청 오류] {label or url} → {e}")
            return None

    logger.error(
        f"[최종 실패] {label or url} — "
        f"{RETRY_MAX}회 모두 요청에 실패"
    )
    return None


# ============================================================
# RSS 피드 처리
# ============================================================

def get_channel_id(channel_url: str) -> str | None:
    """
    https://youtube.com/channel/UC... 형식에서 채널 ID만 뽑는다.
    """
    m = re.search(r"/channel/(UC[a-zA-Z0-9_-]+)", channel_url.rstrip("/"))
    if not m:
        return None

    return m.group(1)


def parse_rss_datetime(value: str) -> datetime | None:
    """
    Atom published 값 예:
    2026-09-11T03:20:00+00:00
    2026-09-11T03:20:00Z
    """
    if not value:
        return None

    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def parse_youtube_rss(xml_text: str) -> tuple[str, list[dict]]:
    """
    반환:
    - channel_name: RSS에 기록된 채널명
    - items: [{video_id, url, title, published_utc, published_kst}, ...]
    """
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        logger.error(f"[RSS XML 파싱 오류] {e}")
        return "", []

    channel_name = (
        root.findtext("atom:title", default="", namespaces=NS).strip()
    )

    items = []

    for entry in root.findall("atom:entry", NS):
        video_id = entry.findtext("yt:videoId", default="", namespaces=NS).strip()
        title = entry.findtext("atom:title", default="", namespaces=NS).strip()
        published_text = entry.findtext(
            "atom:published",
            default="",
            namespaces=NS,
        ).strip()

        published_utc = parse_rss_datetime(published_text)

        if not video_id or not published_utc:
            continue

        published_kst = published_utc.astimezone(kst)

        items.append(
            {
                "video_id": video_id,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "title": title,
                "published_utc": published_utc,
                "published_kst": published_kst,
            }
        )

    return channel_name, items


async def fetch_rss_items(session, channel_url: str) -> tuple[str, list[dict]]:
    """
    채널 RSS를 1회 호출하고, 날짜 범위 내 항목만 반환한다.
    """
    channel_id = get_channel_id(channel_url)

    if not channel_id:
        logger.error(f"[채널 ID 추출 실패] {channel_url}")
        return "", []

    feed_url = (
        "https://www.youtube.com/feeds/videos.xml"
        f"?channel_id={channel_id}"
    )

    response = await get_with_retry(
        session,
        feed_url,
        label=f"RSS {channel_id}",
    )

    if response is None:
        return "", []

    try:
        if response.status != 200:
            logger.error(
                f"[RSS 실패] status={response.status} / {feed_url}"
            )
            return "", []

        xml_text = await response.text()

    except Exception as e:
        logger.error(f"[RSS 읽기 오류] {channel_id} → {e}")
        return "", []

    finally:
        response.release()

    channel_name, all_items = parse_youtube_rss(xml_text)

    in_range_items = [
        item
        for item in all_items
        if fromdate <= item["published_kst"] < todate
    ]

    logger.info(
        f"[RSS] {channel_name or channel_id} | "
        f"전체 {len(all_items)}개 / "
        f"날짜 범위 대상 {len(in_range_items)}개"
    )

    for item in in_range_items:
        logger.info(
            f"[RSS 대상] {item['title']} | "
            f"{item['url']} | "
            f"{item['published_kst']:%Y-%m-%d %H:%M:%S}"
        )

    return channel_name, in_range_items


# ============================================================
# 상세 watch 페이지 최종 확인 및 HTML 생성
# ============================================================

async def translate_title_if_needed(
    channel_name: str,
    title: str,
    video_url: str,
) -> str:
    """
    지정한 영어 채널 제목만 한국어로 번역한다.
    동기 googletrans 호출은 별도 thread에서 실행하여
    asyncio 이벤트 루프가 멈추지 않게 한다.
    """
    if channel_name not in englishchannel:
        return title

    original_title = title

    for attempt in range(1, RETRY_MAX + 1):
        try:
            translated = await asyncio.to_thread(
                translator.translate,
                original_title,
                src="en",
                dest="ko",
            )

            return translated.text

        except Exception as e:
            logger.warning(
                f"[번역 오류 {attempt}/{RETRY_MAX}] "
                f"{video_url} → {e}"
            )

            if attempt < RETRY_MAX:
                await asyncio.sleep(RETRY_WAIT)

    logger.warning(
        f"[번역 최종 실패] 원문 제목 유지 | {video_url}"
    )
    return original_title


async def fetch_video_detail(session, rss_item: dict) -> dict | None:
    """
    RSS에서 날짜 범위를 통과한 항목만 여기로 들어온다.

    최종 확인:
    - HTTP 상태
    - 예정 라이브 제외
    - scheduledStartTime 제외
    - 상세 페이지의 게시일을 다시 확인
    - 제목/실제 채널명 추출
    """
    video_url = rss_item["url"]

    response = await get_with_retry(
        session,
        video_url,
        label=video_url,
    )

    if response is None:
        return None

    try:
        if response.status != 200:
            logger.error(
                f"[상세 fetch 실패] status={response.status} / {video_url}"
            )
            return None

        html_text = await response.text()

        # 예정 라이브 제외
        lbc_match = re.search(
            r'liveBroadcastContent["]*\s*:\s*["]*(\w+)',
            html_text,
        )

        if lbc_match and lbc_match.group(1).lower() == "upcoming":
            logger.info(f"[SKIP-UPCOMING] {video_url}")
            return None

        if re.search(r"scheduledStartTime", html_text):
            logger.info(f"[SKIP-SCHEDULED] {video_url}")
            return None

        soup = BeautifulSoup(html_text, "lxml")

        # 상세 페이지 게시일 재확인
        date_meta = soup.find(
            "meta",
            attrs={"itemprop": "datePublished"},
        )

        if date_meta and date_meta.get("content"):
            published_text = date_meta["content"]
            published_utc = parse_rss_datetime(published_text)

        else:
            published_utc = None

            for script_tag in soup.find_all(
                "script",
                string=re.compile(r"ytInitialPlayerResponse"),
            ):
                match = re.search(
                    r'"publishDate"\s*:\s*"([^"]+)"',
                    script_tag.string or "",
                )

                if match:
                    published_utc = parse_rss_datetime(match.group(1))
                    break

        # watch 페이지에서 날짜를 얻지 못하면 RSS 날짜 사용
        if published_utc is None:
            published_kst = rss_item["published_kst"]
            logger.warning(
                f"[상세 게시일 없음 - RSS 게시일 사용] {video_url}"
            )
        else:
            published_kst = published_utc.astimezone(kst)

        # 상세 페이지의 날짜도 최종 범위 확인
        if published_kst >= todate:
            logger.info(
                f"[대상 아님 - 이후] {video_url} | "
                f"{published_kst:%Y-%m-%d %H:%M:%S}"
            )
            return None

        if published_kst < fromdate:
            logger.info(
                f"[대상 아님 - 이전] {video_url} | "
                f"{published_kst:%Y-%m-%d %H:%M:%S}"
            )
            return None

        title_tag = soup.find("title")
        title = (
            title_tag.get_text().strip()
            .replace(" - YouTube", "")
            .replace("#shorts", "")
            if title_tag
            else rss_item["title"]
        )

        channel_link = soup.find(
            "link",
            attrs={"itemprop": "name"},
        )

        channel_name = (
            channel_link.get("content", "").strip()
            if channel_link
            else ""
        )

        title = await translate_title_if_needed(
            channel_name=channel_name,
            title=title,
            video_url=video_url,
        )

        logger.info(
            f"[대상 맞음] {title} | {video_url} | "
            f"{published_kst:%Y-%m-%d %H:%M:%S}"
        )

        return {
            "url": video_url,
            "title": title,
            "channel_name": channel_name,
            "published_kst": published_kst,
        }

    except Exception as e:
        logger.error(f"[상세 fetch 처리 오류] {video_url} → {e}")
        return None

    finally:
        response.release()


def make_video_html(item: dict) -> str:
    """
    영상/Shorts/스트림 구분 없이 동일 형식으로 기록.
    """
    video_url = item["url"]
    title = item["title"]

    iframe = yt.video(
        video_url,
        width=width,
        height=height,
    )

    tempstr = f"<p>{title}</p>\n"
    tempstr += (
        f'<p><a target=_blank href="{video_url}">'
        f"{video_url}</a></p>\n"
    )
    tempstr += f"<p>{iframe}</p>\n"

    return tempstr


# ============================================================
# 채널 1개 처리
# ============================================================

async def process_channel(session, channel_url: str, filename: Path):
    channel_url = channel_url.rstrip("/")

    rss_channel_name, rss_items = await fetch_rss_items(
        session,
        channel_url,
    )

    # RSS에 제목이 없거나 RSS 요청 실패해도 출력 구조를 유지
    channel_name = rss_channel_name or channel_url.rsplit("/", 1)[-1]
    safe_channel_name = channel_name.replace("--", "—")
    channel_header = f"#####***** {safe_channel_name} *****#####"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"<!-- {channel_header} -->\n")

    if not rss_items:
        logger.info(f"[RSS 대상 없음] {channel_name}")
        return

    # 날짜 범위 안인 항목만 최대 5개 동시 상세 조회
    tasks = [
        fetch_video_detail(session, rss_item)
        for rss_item in rss_items
    ]

    results = await asyncio.gather(*tasks)

    valid_items = [
        item
        for item in results
        if item is not None
    ]

    if not valid_items:
        logger.info(f"[최종 대상 없음] {channel_name}")
        return

    file_content = "\n".join(
        make_video_html(item)
        for item in valid_items
    )

    with open(filename, "a", encoding="utf-8") as f:
        f.write(file_content)

    # 기존 정책 유지: 영어 채널 URL은 마지막 목록에서 제외
    if channel_name not in englishchannel:
        collected_urls.extend(item["url"] for item in valid_items)

    logger.info(
        f"[기록 완료] {channel_name} | "
        f"{len(valid_items)}개"
    )


# ============================================================
# 메인
# ============================================================

async def main(urllist: list[str]):
    filename = savefolder / f"{datetime.now():%Y-%m-%d}_youtube.txt"

    # 같은 날짜 파일을 매 실행마다 새로 생성하려면 "w"를 사용.
    # 기존처럼 누적 기록하려면 "a"로 변경.
    with open(filename, "w", encoding="utf-8") as f:
        f.write("")

    connector = aiohttp.TCPConnector(
        limit=CONNECTOR_LIMIT,
        limit_per_host=CONNECTOR_LIMIT_PER_HOST,
        ttl_dns_cache=300,
    )

    timeout = aiohttp.ClientTimeout(total=SESSION_TIMEOUT)

    async with aiohttp.ClientSession(
        headers=headers,
        connector=connector,
        timeout=timeout,
    ) as session:
        # 채널은 아직 순차 처리:
        # 기존 코드와 비슷한 요청 패턴을 유지하면서,
        # RSS 도입으로 요청 수만 대폭 줄인다.
        for channel_url in urllist:
            await process_channel(
                session=session,
                channel_url=channel_url,
                filename=filename,
            )

    # ========================================================
    # 최종 URL 리스트업
    # ========================================================

    unique_urls = list(dict.fromkeys(collected_urls))

    if unique_urls:
        with open(filename, "a", encoding="utf-8") as f:
            f.write("\n" * 5)
            f.write("\n".join(unique_urls))
            f.write("\n")

        logger.info(
            f"[URL 리스트업] 총 {len(unique_urls)}개 URL 기록 완료 | "
            f"날짜 범위 "
            f"{fromdate:%Y-%m-%d %H:%M} ~ "
            f"{todate:%Y-%m-%d %H:%M} | "
            f"{filename}"
        )
    else:
        logger.info("[URL 리스트업] 수집된 URL 없음")


# ============================================================
# 실행
# ============================================================

if __name__ == "__main__":
    urllist = [
        "https://youtube.com/channel/UCLKuglhGlMmDteQKoniENIQ",
        "https://youtube.com/channel/UCxlv4aOnrRTXMRSL8bVJqEw",
        "https://youtube.com/channel/UCuKKkBSGK4e9fuaquWXorJg",
        "https://youtube.com/channel/UC5aNQ65ADb02zEJxzb_zmYQ",
        "https://youtube.com/channel/UCpcft4FJXgUjnxWoQYsl7Ug",
        "https://youtube.com/channel/UCsG1230uY3XP2QyvSOY1YHg",
        "https://youtube.com/channel/UCt-BApVtJGrvF5pCgbiNVeg",
        "https://youtube.com/channel/UC_uyxB9i4J9O5atc_2fBKww",
        "https://youtube.com/channel/UCDNvRZRgvkBTUkQzFoT_8rA",
        "https://youtube.com/channel/UC2VDsgZ343N9hKnEXQWKnag",
        "https://youtube.com/channel/UCrBpV_pG2kyMMEHCMTNzjAQ",
        "https://youtube.com/channel/UCl8OVxF0iHY3uFEgXz9w00g",
        "https://youtube.com/channel/UCZs4JB7TzuOiKmPrCXQ3Gyg",
        "https://youtube.com/channel/UCiOWYRzOTiUYi9pJ-kscIKw",
        "https://youtube.com/channel/UCKNdfTZCJuOQfWN5Pe5UAAQ",
        "https://youtube.com/channel/UCJS9VvReVkplPwCIbxnbsjQ",
        "https://youtube.com/channel/UC7F6UDq3gykPZHWRhrj_BDw",
        "https://youtube.com/channel/UCgheNMc3gGHLsT-RISdCzDQ",
        "https://youtube.com/channel/UCCsGPRmHOXhF4WTYs7ght9g",
        "https://youtube.com/channel/UC7uDyFIqExDnfXAIZqumFrQ",
        "https://youtube.com/channel/UCjHn_Os5NoCXZyoXzuKth9w",
        "https://youtube.com/channel/UCsJ6RuBiTVWRX156FVbeaGg",
        "https://youtube.com/channel/UCJo6G1u0e_-wS-JQn3T-zEw",
        "https://youtube.com/channel/UCeEM8XgdgUyaWE1Z6_5sHbQ",
        "https://youtube.com/channel/UC_Aly3X5CdojHdRDGmKi1ow",
        "https://youtube.com/channel/UCEKhdkZxxdHWoDmht8nQFxQ",
        "https://youtube.com/channel/UCCQPdv4o4ywVZQkAMOlvFbw",
        "https://youtube.com/channel/UCfcgDLazgMa1L92Kl3r9ZAA",
        "https://youtube.com/channel/UCW-xgKdaPidxpJ6j6HZPC-g",
        "https://youtube.com/channel/UCiDmfbYvuMEVbRxPmFP4sng",
        "https://youtube.com/channel/UCMnFS27HnroIc1D4ct37TUA",
        "https://youtube.com/channel/UCn7WoT17_HlpfOPQHEqgUkw",
        "https://youtube.com/channel/UCgsSoMtSPekGiQF8DS5pI_w",
        "https://youtube.com/channel/UCu3BjLd03jxTVHXTPqZ77iQ",
        "https://youtube.com/channel/UCM3Rlsen-yIDz_5GF2D_SUw",
        "https://youtube.com/channel/UCLcfz3EIgDw01VtRLZmrxDQ",
        "https://youtube.com/channel/UCelFN6fJ6OY6v8pbc_SLiXA",
        "https://youtube.com/channel/UCZUjLw9C0Tt3VECAhQO9buA",
        "https://youtube.com/channel/UC-IBt8pM8hWx8wiwjcDLdIQ",
        "https://youtube.com/channel/UCy5xupkbznNROYQJKca9A7g",
        "https://youtube.com/channel/UCsooa4yRKGN_zEE8iknghZA",
        "https://youtube.com/channel/UCsXVk37bltHxD1rDPwtNM8Q",
        "https://youtube.com/channel/UCq8ZAAsI89IoJ-fn1gYpO3g",
        "https://youtube.com/channel/UCLXo7UDZvByw2ixzpQCufnA",
        "https://youtube.com/channel/UCrIAnDo3VuWex3fywkGpB1g",
        "https://youtube.com/channel/UC4SaZQMdD97YEjs26kSHn9w",
        "https://youtube.com/channel/UCbv7Dcn5iNrAyd3GwgVHkIQ",
        "https://youtube.com/channel/UCSB5FOwUVnAhGo_o99IhxYA",
        "https://youtube.com/channel/UCPq0i_bZeqVoVYm_u8qimDA",
        "https://youtube.com/channel/UCL1lgfyEG71UrPodvuAYx7w",
        "https://youtube.com/channel/UC7A1QdDXcu3zu_KS8DddL1A",
        "https://youtube.com/channel/UCznL5L7iTgTaqSBS5yF6g7w",
        "https://youtube.com/channel/UCOON7HbktJy5i19fyKTOEXw",
    ]

    headers = {
        "User-Agent": generate_user_agent(
            device_type="desktop",
            navigator="chrome",
        ),
        "Accept-Language": "en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7",
        "Accept": (
            "application/atom+xml,application/xml;q=0.9,"
            "text/html;q=0.8,*/*;q=0.7"
        ),
    }

    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )

    try:
        asyncio.run(main(urllist))

    except KeyboardInterrupt:
        logger.warning("[사용자 중단] Ctrl+C로 실행이 중단되었습니다.")

    except Exception as e:
        logger.exception(f"[치명적 오류] {e}")

    finally:
        datetime2 = datetime.now()

        logger.info(
            f"{datetime1:%Y-%m-%d %H:%M:%S} ~ "
            f"{datetime2:%Y-%m-%d %H:%M:%S} - Ending"
        )
        logger.info(datetime2 - datetime1)