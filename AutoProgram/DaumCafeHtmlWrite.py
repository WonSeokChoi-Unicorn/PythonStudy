# -*- coding: utf-8 -*-
from selenium import webdriver
# 키 입력 위해 필요한 2가지
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
# 클립보드로 복사하기 위한 라이브러리 import
import clipboard
import time

# 참고 - https://david-kim2028.tistory.com/8
options = webdriver.ChromeOptions()
# 로그를 없애는 설정
options.add_experimental_option("excludeSwitches", ["enable-logging"])
# 크롬 브라우저 안 보이게 하면 커서 위치 잡을 수 없어서 options.add_argument('headless') 옵션 사용하지 않아야 정상 처리 됨
# 창 크기 
options.add_argument("window-size=1200x600")
# 카카오 아이디
kakaoid = ""
# 카카오 비밀번호
kakaopw = ""
browser = webdriver.Chrome(executable_path='chromedriver', options=options)
browser.get("https://accounts.kakao.com/login?continue=https%3A%2F%2Flogins.daum.net%2Faccounts%2Fksso.do%3Frescue%3Dtrue%26url%3Dhttps%253A%252F%252Fwww.daum.net%252F")
id = browser.find_element_by_css_selector("#id_email_2")
id.send_keys(kakaoid)
pw = browser.find_element_by_css_selector("#id_password_3")
pw.send_keys(kakaopw)
# 카카오톡으로 로그인 알림
browser.find_element_by_css_selector("#login-form > fieldset > div.wrap_btn > button.btn_g.btn_confirm.submit").click()
time.sleep(3)
browser.get("https://cafe.daum.net/rezzoclub")
time.sleep(3)
# 자유 게시판 클릭
# 프레임 전환 #태그명 생략해도 됨 iframe 지워도 됨
browser.switch_to.frame(browser.find_element_by_css_selector("#down"))
browser.find_element_by_css_selector("#fldlink_2S31_233").click()
time.sleep(3)
# 글쓰기 버튼 클릭
browser.find_element_by_css_selector("#article-write-btn").click()
time.sleep(3)
# 제목 작성
subjecttext = "개와 고양이"
subject = browser.find_element_by_css_selector("#article-title > input")
subject.send_keys(subjecttext)
# 본문 작성 
contenttext = '<img src="https://cdn.pixabay.com/photo/2020/05/08/16/06/dog-5146351_960_720.jpg"><br><br><img src="https://cdn.pixabay.com/photo/2021/02/23/09/26/cat-6042858_960_720.jpg">'
# HTML 클릭
browser.find_element_by_css_selector("#mceu_5-button").click()
# 클립보드 초기화
clipboard.copy("")
# 클립보드로 복사
clipboard.copy(contenttext)
# 클립보드에서 붙혀넣기
ActionChains(browser).key_down(Keys.CONTROL).send_keys('v').perform()
# 확인 클릭
browser.find_element_by_css_selector("#cafeLayout > div.mce-codeblock-dialog-container.mce-window.ke-dialog-html.mce-in > div.mce-codeblock-dialog > div.mce-foot.mce-container > div > div.mce-btn.mce-primary.mce-codeblock-btn-submit > button > span").click()
# 제일 바깥으로 빠져나옴.
browser.switch_to.default_content()
# 프레임 전환
browser.switch_to.frame(browser.find_element_by_css_selector("#down"))
# 발행 버튼 클릭
browser.find_element_by_css_selector("#primaryContent > div > div.cont_btn.area_btn_g > div.area_r > button").click()
time.sleep(3)
browser.quit()