import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

# 봇 방지 웹사이트 회피
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}

# 검색할 사업자번호
Biznum = [
          "1428145237",
          "214-87-17187"
         ]

# requests post url
url = "https://teht.hometax.go.kr/wqAction.do?actionId=ATTABZAA001R08&screenId=UTEABAAA13&popupYn=false&realScreenId="
# requests data
post = "<map id=\"ATTABZAA001R08\"><pubcUserNo/><mobYn>N</mobYn><inqrTrgtClCd>1</inqrTrgtClCd><txprDscmNo>Biznum</txprDscmNo><dongCode>81</dongCode><psbSearch>Y</psbSearch><map id=\"userReqInfoVO\"/></map><nts<nts>nts>58cKuokaDhrUdtF8gFLDQZU6XMel7xRdgvDvT322quE47"
# name requests url
nameurl = "https://bizno.net/article/"

def biznum(number):
    # requests post
    numres = requests.post(url, data=post.replace("Biznum", number))
    # requests post 결과값에서 smpcBmanTrtCntn 가져오기
    numstatus = ET.fromstring(numres.text).findtext("smpcBmanTrtCntn")
    # requests post 결과값에서 trtCntn 가져오기
    numcomment = ET.fromstring(numres.text).findtext("trtCntn")
    # 출력문구
    biznumstatus = numstatus + " / " + numcomment
    return biznumstatus

def bizname(number):
    # 페이지 요청 및 응답 수신
    namemain = requests.get(nameurl + number, headers=headers)
    # HTML로 받기
    namehtml = namemain.text
    # HTML을 'lxml(XML, HTML 처리)'를 사용하여 분석
    nameSoup = BeautifulSoup(namehtml, 'lxml')
    # 상호 가져오기
    biznumname = str(nameSoup.find(lambda tag : tag.name == 'div' and tag.get('class') == ['titles']).get_text()).strip()
    return biznumname

# Biznum 순서대로 불러오기
for bizno in Biznum:
    # "-"가 있으면 제거
    biz_no = bizno.replace("-", "")
    # 사업자 번호로 상태 조회 함수 호출
    inquirystatus = biznum(biz_no)
    # 사업자 번호로 상호 조회 함수 호출
    inquiryname = bizname(biz_no)
    # 결과 출력
    print(str(Biznum.index(bizno) + 1) + " / " + str(len(Biznum)) + " - " + bizno + ", " + inquiryname + " : " + inquirystatus)