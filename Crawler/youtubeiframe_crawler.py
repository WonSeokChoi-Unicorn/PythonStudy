import os
import requests
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# 저장 폴더
savefolder = Path("D:/ggoorr")

# 유튜브 URL 정리한 텍스트 파일을 한 줄씩 읽어 옵니다
fr = open("D:\\youtubeurl.txt", "r", encoding="utf-8")
# 한 줄씩 읽기
lines = fr.readlines()

# 파일명을 날짜로 이용하기 위해 글로벌로 이동
nowDate = datetime.now()

# 결과 파일 경로
outfile = savefolder / (nowDate.strftime("%Y-%m-%d") + "_youtubeonce.txt")

# 파일에 저장 (시작)
if os.path.isfile(outfile):
    # 파일이 존재할 경우 추가, 파일 작성 시간이 길어져서 년월일로 파일명 생성
    fw = open(outfile, mode="at", encoding="utf-8")
else:
    # 파일이 존재하지 않을 경우 생성, 파일 작성 시간이 길어져서 년월일로 파일명 생성
    fw = open(outfile, mode="wt", encoding="utf-8")


# oEmbed 요청 함수[web:19]
def get_oembed_data(video_url: str):
    endpoint = "https://www.youtube.com/oembed"
    params = {
        "url": video_url,
        "format": "json",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; youtube-oembed-bot/1.0)"
    }

    resp = requests.get(endpoint, params=params, headers=headers, timeout=10)
    if resp.status_code != 200:
        raise RuntimeError(f"oEmbed 요청 실패: {resp.status_code} {resp.text}")
    return resp.json()


# Shorts URL을 oEmbed용 watch URL로 변환[web:23]
def normalize_youtube_url(url: str) -> str:
    url = url.strip()

    if not url:
        return url

    if "/shorts/" in url:
        video_id = url.split("/shorts/")[1]
        if "?" in video_id:
            video_id = video_id.split("?", 1)[0]
        return f"https://www.youtube.com/watch?v={video_id}"

    # watch, youtu.be 등은 그대로 사용[web:19]
    return url


# 다양한 형태의 유튜브 URL에서 Video ID 추출
def extract_video_id(url: str) -> str:
    url = url.strip()
    if not url:
        return ""

    # shorts
    if "/shorts/" in url:
        video_id = url.split("/shorts/")[1]
        if "?" in video_id:
            video_id = video_id.split("?", 1)[0]
        return video_id

    parsed = urlparse(url)

    # watch?v= 형태
    if parsed.path == "/watch":
        qs = parse_qs(parsed.query)
        if "v" in qs:
            return qs["v"][0]

    # youtu.be 단축 URL
    if "youtu.be" in parsed.netloc and parsed.path:
        return parsed.path.lstrip("/")

    # /embed/ID 형태
    if "/embed/" in parsed.path:
        return parsed.path.split("/embed/")[1]

    return ""


for line in reversed(lines):
    # 빈 줄일 경우 통과
    if line.strip() == "":
        continue

    original_url = line.strip()

    # oEmbed용 URL 정규화 (특히 shorts → watch)[web:23]
    normalized_url = normalize_youtube_url(original_url)

    try:
        data = get_oembed_data(normalized_url)
    except Exception as e:
        print("################################################################################################")
        print(f"oEmbed 실패: {original_url}")
        print(e)
        print("################################################################################################")
        continue

    # oEmbed 응답에서 제목만 사용[web:19]
    title = data.get("title", "").strip()

    # 최종 iframe 생성을 위해 Video ID 추출
    video_id = extract_video_id(original_url)
    if not video_id:
        print("VIDEO ID 추출 실패: ", original_url)
        continue

    # 원하는 최종 형태의 iframe 직접 생성
    iframe_html = (
        f'<iframe width="560" height="315" '
        f'src="https://www.youtube.com/embed/{video_id}" '
        f'frameborder="0" '
        f'allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" '
        f'allowfullscreen></iframe>'
    )

    print("################################################################################################")
    print(title)
    print("################################################################################################")

    # 출력 형식:
    # <p>제목</p>
    # <p><a target=_blank href="URL">URL</a></p>
    # <p><iframe ...></iframe></p>
    tempstr = ""
    tempstr += f'<p>{title}</p>\n'
    tempstr += f'<p><a target=_blank href="{original_url}">{original_url}</a></p>\n'
    tempstr += f'<p>{iframe_html}</p>\n\n'

    fileContent = tempstr

    if (fw is not None) and fw.write(fileContent):
        print("fileContent write OK ")
    else:
        fw.close()

fr.close()
fw.close()
