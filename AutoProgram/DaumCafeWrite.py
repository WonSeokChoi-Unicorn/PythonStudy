# -*- coding: utf-8 -*-
from selenium import webdriver
import time

# 참고 - https://david-kim2028.tistory.com/8
options = webdriver.ChromeOptions()
# 로그를 없애는 설정
options.add_experimental_option("excludeSwitches", ["enable-logging"])
# 크롬 브라우저 안 보이게 하려면 아래 주석 해제
# options.add_argument('headless')
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
# id.send_keys("unicorn97")
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
subjecttext = ""
subject = browser.find_element_by_css_selector("#article-title > input")
subject.send_keys(subjecttext)
# 본문 작성 
# 프레임 전환
browser.switch_to.frame(browser.find_element_by_css_selector("#keditorContainer_ifr"))
contenttext = ''
content = browser.find_element_by_css_selector("#tinymce")
content.send_keys(contenttext)
# 제일 바깥으로 빠져나옴.
browser.switch_to.default_content()
# 프레임 전환
browser.switch_to.frame(browser.find_element_by_css_selector("#down"))
# 발행 버튼 클릭
browser.find_element_by_css_selector("#primaryContent > div > div.cont_btn.area_btn_g > div.area_r > button").click()
time.sleep(3)
browser.quit()