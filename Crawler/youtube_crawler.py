import sys
sys.stdout.reconfigure(encoding="utf-8")

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from yt_iframe import yt
import re
from user_agent import generate_user_agent
from googletrans import Translator
import pytz
import json
import asyncio
import aiohttp
import time
import logging
from pathlib import Path

# 로거 생성
logger = logging.getLogger("YoutubeLogger")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
stream_handler.setLevel(logging.INFO)

log_file = f"D:\\Python\\LOG\\{datetime.now().strftime('%Y%m%d%H%M%S')}_youtube.log"
file_handler = logging.FileHandler(log_file, encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
file_handler.setLevel(logging.DEBUG)

# 설정값
datetime1 = datetime.now()
logger.info(datetime1.strftime("%Y-%m-%d %H:%M:%S") + " - Starting")

pst = pytz.timezone("America/Los_Angeles")
kst = pytz.timezone("Asia/Seoul")

waittime5 = 5
tab_delay = 1.5
channel_delay = 2.0

RETRY_MAX = 3
RETRY_WAIT = 5.0
FETCH_TIMEOUT = 30
SESSION_TIMEOUT = 60

width = "560"
height = "315"

englishchannel = [
    "Kurzgesagt – In a Nutshell",
    "TED-Ed",
    "Vox",
    "Nightshift – Kurzgesagt After Dark",
]

yesterday = datetime.today() - timedelta(days=1)
fromdate = datetime(yesterday.year, yesterday.month, yesterday.day, 5, 0, 0).astimezone(kst)
todate = datetime(datetime.today().year, datetime.today().month, datetime.today().day, 4, 59, 59).astimezone(kst)

translator = Translator()
savefolder = Path("D:/ggoorr")

TAB_TITLES = {
    "videos": ["동영상", "Videos"],
    "streams": ["라이브", "Live"],
    "shorts": ["Shorts", "쇼츠"],
}


def detect_available_tabs(html_text: str) -> list[str]:
    m = re.search(r"ytInitialData\s*=\s*({.*?});\s*(?:var |window\.|)", html_text, re.DOTALL)
    if not m:
        m = re.search(r"ytInitialData\s*=\s*({.*});", html_text, re.DOTALL)
    if not m:
        return ["videos", "streams", "shorts"]

    try:
        data = json.loads(m.group(1))
    except Exception:
        return ["videos", "streams", "shorts"]

    tabs_data = (
        data.get("contents", {})
        .get("twoColumnBrowseResultsRenderer", {})
        .get("tabs", [])
    )

    found_tabs = []
    for tab in tabs_data:
        tr = tab.get("tabRenderer", {})
        title = tr.get("title", "")
        endpoint = tr.get("endpoint", {})
        url_path = (
            endpoint.get("commandMetadata", {})
            .get("webCommandMetadata", {})
            .get("url", "")
        )

        for key, keywords in TAB_TITLES.items():
            if any(kw.lower() == title.lower() for kw in keywords):
                found_tabs.append(key)
                break
            if url_path.endswith(f"/{key}"):
                found_tabs.append(key)
                break

    ordered = [t for t in ["videos", "streams", "shorts"] if t in found_tabs]
    if not ordered:
        return ["videos", "streams", "shorts"]
    return ordered


async def get_with_retry(session, url, label=""):
    for attempt in range(1, RETRY_MAX + 1):
        try:
            resp = await session.get(url, timeout=aiohttp.ClientTimeout(total=FETCH_TIMEOUT))
            return resp
        except asyncio.TimeoutError:
            logger.error(f"[타임아웃 {attempt}/{RETRY_MAX}] {label or url}")
            if attempt < RETRY_MAX:
                await asyncio.sleep(RETRY_WAIT)
        except aiohttp.ClientConnectionError as e:
            logger.error(f"[연결 오류 {attempt}/{RETRY_MAX}] {label or url} → {e}")
            if attempt < RETRY_MAX:
                await asyncio.sleep(RETRY_WAIT)
        except Exception as e:
            logger.error(f"[요청 오류] {label or url} → {e}")
            return None

    logger.error(f"[최종 실패] {label or url} — {RETRY_MAX}회 모두 타임아웃")
    return None


async def fetch(session, yt_videoid):
    resp = await get_with_retry(session, yt_videoid, label=yt_videoid)
    if resp is None:
        return None

    try:
        if resp.status != 200:
            logger.error(f"[fetch 실패] status={resp.status} / {yt_videoid}")
            return None

        Html2 = await resp.text()
        Soup2 = BeautifulSoup(Html2, "lxml")

        lbc_match = re.search(r'liveBroadcastContent[\"]*\s*:\s*[\"]*(\w+)', Html2)
        if lbc_match and lbc_match.group(1) == "upcoming":
            logger.info(f"[SKIP-UPCOMING] {yt_videoid}")
            return None

        if re.search(r'scheduledStartTime', Html2):
            logger.info(f"[SKIP-SCHEDULED] {yt_videoid}")
            return None

        date_meta = Soup2.find("meta", attrs={"itemprop": "datePublished"})
        if not date_meta:
            script_tags = Soup2.find_all("script", string=re.compile(r"ytInitialPlayerResponse"))
            yt_datePublished = None

            for st in script_tags:
                mm = re.search(r'"publishDate"\s*:\s*"([^"]+)"', st.string or "")
                if mm:
                    yt_datePublished = mm.group(1)
                    break

            if not yt_datePublished:
                logger.error(f"[날짜 없음] {yt_videoid}")
                return None

            yt_datePublisheddt = datetime.strptime(yt_datePublished, "%Y-%m-%dT%H:%M:%S%z")
        else:
            yt_datePublished = date_meta["content"]
            yt_datePublisheddt = datetime.strptime(yt_datePublished, "%Y-%m-%dT%H:%M:%S%z")

        yt_datePublisheddtkst = yt_datePublisheddt.astimezone(pst).astimezone(kst)

        title_tag = Soup2.find("title")
        yt_title = (
            title_tag.get_text().strip()
            .replace(" - YouTube", "")
            .replace("#shorts", "")
            if title_tag else "제목 없음"
        )

        channel_link = Soup2.find("link", attrs={"itemprop": "name"})
        channelname = channel_link["content"] if channel_link else ""

        if channelname in englishchannel:
            while True:
                try:
                    yt_title = translator.translate(yt_title, src="en", dest="ko").text
                    break
                except Exception:
                    time.sleep(waittime5)

        if yt_datePublisheddtkst > todate:
            logger.info(f"[대상 아님 - 이후] {yt_title} | {yt_videoid} | {yt_datePublisheddtkst:%Y-%m-%d %H:%M:%S}")
            return None
        elif yt_datePublisheddtkst <= fromdate:
            logger.info(f"[대상 아님 - 이전] {yt_title} | {yt_videoid} | {yt_datePublisheddtkst:%Y-%m-%d %H:%M:%S}")
            return None
        else:
            logger.info(f"[대상 맞음] {yt_title} | {yt_videoid} | {yt_datePublisheddtkst:%Y-%m-%d %H:%M:%S}")

        iframe = yt.video(yt_videoid, width=width, height=height)

        tempstr  = f"<p>{yt_title}</p>\n"
        tempstr += (
            f'<p><a target=_blank href="{yt_videoid}">{yt_videoid}</a></p>\n'
        )
        tempstr += f"<p>{iframe}</p>\n"

        return tempstr

    except Exception as e:
        logger.error(f"[fetch 처리 오류] {yt_videoid} → {e}")
        return None


def is_members_only_text(text: str) -> bool:
    if not text:
        return False
    text = text.lower()
    keywords = [
        "회원 전용",
        "멤버 전용",
        "members only",
        "members-only",
        "member only",
        "for members",
        "가입",
    ]
    return any(k.lower() in text for k in keywords)


def has_members_only_badge_in_lockup(lv: dict) -> bool:
    metadata_rows = (
        lv.get("metadata", {})
        .get("lockupMetadataViewModel", {})
        .get("metadata", {})
        .get("contentMetadataViewModel", {})
        .get("metadataRows", [])
    )

    for row in metadata_rows:
        badges = row.get("badges", [])
        for badge in badges:
            bv = badge.get("badgeViewModel", {})
            badge_text = bv.get("badgeText", "")
            acc_label = (
                bv.get("rendererContext", {})
                .get("accessibilityContext", {})
                .get("label", "")
            )
            if is_members_only_text(badge_text) or is_members_only_text(acc_label):
                return True

    lv_text = json.dumps(lv, ensure_ascii=False).lower()
    members_keywords = [
        "회원 전용",
        "멤버 전용",
        "members only",
        "members-only",
        "member only",
        "badge_style_type_members_only",
        "sponsorsonly",
        "sponsoronly",
    ]
    return any(k in lv_text for k in members_keywords)


def parse_rich_item(content_item: dict) -> str | None:
    # 패턴 A: videoRenderer
    if "videoRenderer" in content_item:
        vr = content_item["videoRenderer"]
        yt_videoid = vr.get("videoId")
        if not yt_videoid:
            return None

        if "upcomingEventData" in vr:
            return None

        overlays = vr.get("thumbnailOverlays", [])
        if any(
            ov.get("thumbnailOverlayTimeStatusRenderer", {}).get("style") == "UPCOMING"
            for ov in overlays
        ):
            return None

        badges = vr.get("badges", [])
        if any(
            b.get("metadataBadgeRenderer", {}).get("style") == "BADGE_STYLE_TYPE_MEMBERS_ONLY"
            or "회원" in b.get("metadataBadgeRenderer", {}).get("label", "")
            for b in badges
        ):
            return None

        vr_text = json.dumps(vr, ensure_ascii=False).lower()
        if any(k in vr_text for k in ["회원 전용", "멤버 전용", "members only", "members-only"]):
            return None

        return "https://www.youtube.com/watch?v=" + yt_videoid

    # 패턴 B: shortsLockupViewModel
    if "shortsLockupViewModel" in content_item:
        sl = content_item["shortsLockupViewModel"]

        sl_text = json.dumps(sl, ensure_ascii=False).lower()
        if any(k in sl_text for k in ["회원 전용", "멤버 전용", "members only", "members-only"]):
            return None

        url_path = (
            sl.get("onTap", {})
            .get("innertubeCommand", {})
            .get("commandMetadata", {})
            .get("webCommandMetadata", {})
            .get("url", "")
        )
        if url_path.startswith("/shorts/"):
            vid_id = url_path.replace("/shorts/", "").split("?")[0]
        else:
            entity_id = sl.get("entityId", "")
            vid_id = (
                entity_id.replace("shorts-shelf-item-", "")
                if entity_id.startswith("shorts-shelf-item-")
                else None
            )

        return ("https://www.youtube.com/watch?v=" + vid_id) if vid_id else None

    # 패턴 C: lockupViewModel
    if "lockupViewModel" in content_item:
        lv = content_item["lockupViewModel"]

        content_type = lv.get("contentType", "")
        if content_type not in (
            "LOCKUP_CONTENT_TYPE_VIDEO",
            "LOCKUP_CONTENT_TYPE_LIVE",
            "LOCKUP_CONTENT_TYPE_SHORTS",
            "",
        ):
            return None

        # 회원 전용 체크
        if has_members_only_badge_in_lockup(lv):
            return None

        # 예정 동영상 체크
        lv_text = json.dumps(lv, ensure_ascii=False).lower()
        if any(k in lv_text for k in ["upcoming", "scheduledstarttime", "livebroadcastcontent"]):
            if "upcoming" in lv_text or "scheduledstarttime" in lv_text:
                return None

        vid_id = lv.get("contentId")
        if not vid_id:
            vid_id = (
                lv.get("rendererContext", {})
                .get("commandContext", {})
                .get("onTap", {})
                .get("innertubeCommand", {})
                .get("watchEndpoint", {})
                .get("videoId")
            )

        return ("https://www.youtube.com/watch?v=" + vid_id) if vid_id else None

    # 패턴 D: reelItemRenderer
    if "reelItemRenderer" in content_item:
        rr = content_item["reelItemRenderer"]
        rr_text = json.dumps(rr, ensure_ascii=False).lower()
        if any(k in rr_text for k in ["회원 전용", "멤버 전용", "members only", "members-only"]):
            return None

        vid_id = rr.get("videoId")
        return ("https://www.youtube.com/watch?v=" + vid_id) if vid_id else None

    return None


def get_selected_tab_contents(yt_initialdata: dict) -> list:
    yt_tabs = (
        yt_initialdata
        .get("contents", {})
        .get("twoColumnBrowseResultsRenderer", {})
        .get("tabs", [])
    )

    for tab in yt_tabs:
        tr = tab.get("tabRenderer", {})
        if not tr.get("selected", False):
            continue

        content = tr.get("content", {})
        if "richGridRenderer" in content:
            return content["richGridRenderer"].get("contents", [])

        if "sectionListRenderer" in content:
            items = content["sectionListRenderer"].get("contents", [])
            merged = []
            for item in items:
                isr = item.get("itemSectionRenderer", {})
                if isr:
                    merged.extend(isr.get("contents", []))
                else:
                    merged.append(item)
            return merged
        break

    return []


def extract_video_ids_from_html(html_text: str, tab_name: str) -> list:
    Soup_tab = BeautifulSoup(html_text, "lxml")
    yt_scripttags = Soup_tab.find_all("script", string=re.compile(r"ytInitialData"))
    if not yt_scripttags:
        logger.error(f"[{tab_name}] ytInitialData 없음 (봇 차단 / 로그인 유도 가능성)")
        return []

    yt_datascript = yt_scripttags[0].string

    m = re.search(
        r"ytInitialData\s*=\s*({.*?});\s*(?:var |window\.|)",
        yt_datascript,
        re.DOTALL,
    )
    if not m:
        m = re.search(r"ytInitialData\s*=\s*({.*});", yt_datascript, re.DOTALL)

    if not m:
        logger.error(f"[{tab_name}] ytInitialData JSON 추출 실패")
        return []

    try:
        yt_initialdata = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        logger.error(f"[{tab_name}] JSON 파싱 오류: {e}")
        return []

    tab_contents = get_selected_tab_contents(yt_initialdata)
    if not tab_contents:
        logger.error(f"[{tab_name}] selected 탭 contents 없음")
        return []

    yt_videoids = []
    for item in tab_contents:
        rir = item.get("richItemRenderer", {})
        content_item = rir.get("content", {}) if rir else item
        vid = parse_rich_item(content_item)
        if vid:
            yt_videoids.append(vid)

    yt_videoids = list(dict.fromkeys(yt_videoids))
    return yt_videoids


async def main(urllist):
    async with aiohttp.ClientSession(
        headers=headers,
        connector=aiohttp.TCPConnector(limit=5),
        timeout=aiohttp.ClientTimeout(total=SESSION_TIMEOUT),
    ) as session1:
        for base_url in urllist:
            base_url = base_url.rstrip("/")

            response1 = await get_with_retry(session1, base_url, label=f"채널홈 {base_url}")
            if response1 is None:
                logger.error(f"[채널 skip] {base_url} → 접속 최종 실패")
                await asyncio.sleep(channel_delay)
                continue

            if response1.status != 200:
                logger.error(f"[채널 skip] {base_url} → HTTP {response1.status}")
                await asyncio.sleep(channel_delay)
                continue

            try:
                Html1 = await response1.text()
            except Exception as e:
                logger.error(f"[채널 HTML 읽기 오류] {base_url} → {e}")
                await asyncio.sleep(channel_delay)
                continue

            Soup1 = BeautifulSoup(Html1, "lxml")
            title1 = Soup1.find("title")
            channelname = (
                title1.get_text().strip().replace(" - YouTube", "")
                if title1 else base_url.split("/")[-1]
            )

            available_tabs = detect_available_tabs(Html1)

            logger.info("##################################################################")
            logger.info(f"{channelname} → 탭: {available_tabs}")
            logger.info("##################################################################")

            channelheader = "\n#####***** " + channelname + " *****#####\n"
            filename = savefolder / f"{datetime.now().strftime('%Y-%m-%d')}_youtube.txt"

            with open(filename, "a", encoding="utf-8") as f:
                f.write(channelheader)

            for tab_name in available_tabs:
                url = f"{base_url}/{tab_name}"

                response_tab = await get_with_retry(session1, url, label=f"[{tab_name}] {url}")
                if response_tab is None:
                    logger.error(f"[{tab_name}] 최종 실패 → skip")
                    await asyncio.sleep(tab_delay)
                    continue

                if response_tab.status != 200:
                    logger.error(f"[{tab_name}] skip → HTTP {response_tab.status} ({url})")
                    await asyncio.sleep(tab_delay)
                    continue

                try:
                    Html_tab = await response_tab.text()
                except Exception as e:
                    logger.error(f"[{tab_name}] HTML 읽기 오류: {e}")
                    await asyncio.sleep(tab_delay)
                    continue

                yt_videoids = extract_video_ids_from_html(Html_tab, tab_name)
                if not yt_videoids:
                    logger.error(f"[{tab_name}] 영상 ID 없음 → skip")
                    await asyncio.sleep(tab_delay)
                    continue

                logger.info(f"[{tab_name}] 영상 {len(yt_videoids)}개 수집")

                tasks = [fetch(session1, vid) for vid in yt_videoids]
                results = await asyncio.gather(*tasks)

                fileContent = "\n".join(filter(None, results))
                if fileContent:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(f"--------------- {tab_name} ---------------\n")
                        f.write(fileContent)

                    logger.info(f"[{tab_name}] 조건에 맞는 영상 기록 완료")

                await asyncio.sleep(tab_delay)

            await asyncio.sleep(channel_delay)


if __name__ == "__main__":
    urllist = [
        "https://youtube.com/channel/UCLKuglhGlMmDteQKoniENIQ",
        "https://youtube.com/channel/UCxlv4aOnrRTXMRSL8bVJqEw",
        "https://youtube.com/channel/UCuKKkBSGK4e9fuaquWXorJg",
        "https://youtube.com/channel/UC5aNQ65ADb02zEJxzb_zmYQ",
        "https://youtube.com/channel/UCpcft4FJXgUjnxWoQYsl7Ug",
        "https://youtube.com/channel/UCsG1230uY3XP2QyvSOY1YHg",
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
        "https://youtube.com/channel/UC_Aly3X5CdojHdRDGmKi1ow",
        "https://youtube.com/channel/UCEKhdkZxxdHWoDmht8nQFxQ",
        "https://youtube.com/channel/UCCQPdv4o4ywVZQkAMOlvFbw",
        "https://youtube.com/channel/UCfcgDLazgMa1L92Kl3r9ZAA",
        "https://youtube.com/channel/UCW-xgKdaPidxpJ6j6HZPC-g",
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
        "User-Agent": generate_user_agent(device_type="desktop", navigator="chrome"),
        "Accept-Language": "en-US,en;q=0.9,ko-KR;q=0.8,ko;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
    }

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main(urllist))

    datetime2 = datetime.now()
    logger.info(
        datetime1.strftime("%Y-%m-%d %H:%M:%S")
        + " ~ "
        + datetime2.strftime("%Y-%m-%d %H:%M:%S")
        + " - Ending"
    )
    logger.info(datetime2 - datetime1)