import requests
# pip install scrapy
from scrapy import Selector
# pip install cfscrape
import cfscrape
from requests.exceptions import ProxyError, SSLError, ConnectTimeout
# pip install fake-useragent
from fake_useragent import UserAgent
# 403 forbidden 방지
scraper = cfscrape.create_scraper()
# UserAgent 객체
# 에러 발생해도 사용에는 문제 없음
ua = UserAgent()
# 대기 시간
waittime = 5
# 빈 리스트 선언
proxy_server_list = []
# 프록시 서버 리스트 가져오기
def get_proxy_list():
    server_list = []
    # 무료 프록시 정보 제공하는 사이트들
    proxy_urls = [
                  "https://free-proxy-list.net/",
                  "https://www.sslproxies.org/"
                 ]
    # 무료 프록시 정보 제공하는 사이트 확인
    for proxy_url in proxy_urls:
        # 접속
        resp = requests.get(proxy_url)
        # 응답 값 확인
        sel = Selector(resp)
        # free-proxy-list.net 확인
        if proxy_url == "https://free-proxy-list.net/":
            # 테이블 확인
            tr_list = sel.xpath('//*[@id="list"]/div/div[2]/div/table/tbody/tr')
            # 테이블 내 ip, port, https 항목 확인
            for tr in tr_list:
                ip = tr.xpath('td[1]/text()').extract_first()
                port = tr.xpath('td[2]/text()').extract_first()
                https = tr.xpath('td[7]/text()').extract_first()
                # https가 yes 인 것만 확인
                if https == "yes":
                    server = f"{ip}:{port}"
                    server_list.append(server)
        # www.sslproxies.org 확인
        elif proxy_url == "https://www.sslproxies.org/":
            # 테이블 확인
            tr_list = sel.xpath('//*[@id="list"]/div/div[2]/div/table/tbody/tr')
            # 테이블 내 ip, port, https 항목 확인
            for tr in tr_list:
                ip = tr.xpath('td[1]/text()').extract_first()
                port = tr.xpath('td[2]/text()').extract_first()
                https = tr.xpath('td[7]/text()').extract_first()
                # https가 yes 인 것만 확인
                if https == "yes":
                    server = f"{ip}:{port}"
                    server_list.append(server)
    # 중복 제거
    for value in server_list:
        if value not in proxy_server_list:
            proxy_server_list.append(value)
    # 접속 성공 프록시
    Success_proxy_server_list = []
    # 프록시 접속 성공 테스트
    for proxy_server in proxy_server_list:
        # 프록시 정의
        proxies = {"http": proxy_server, 'https': proxy_server}
        try:
            # 주소 요청 및 응답 수신
            Res = scraper.get("https://www.naver.com/", headers = {"User-Agent": ua.random}, proxies = proxies, timeout = waittime)
            if Res.status_code == 200:
                Success_proxy_server_list.append(proxy_server)
                print(str(proxy_server_list.index(proxy_server) + 1) + "/" + str(len(proxy_server_list)) + " Success - " + proxy_server)
        except (ProxyError, SSLError, ConnectTimeout) as e:
            print(str(proxy_server_list.index(proxy_server) + 1) + "/" + str(len(proxy_server_list)) + " Fail - " + proxy_server)
            continue
    return proxy_server_list
# 무료 프록시 리스트 생성
print(get_proxy_list())