import requests
import xml.etree.ElementTree as ET

# 검색할 사업자번호
Biznum = [
          "1428145237",
          "214-87-17187"
         ]

# requests post url
url = "https://teht.hometax.go.kr/wqAction.do?actionId=ATTABZAA001R08&screenId=UTEABAAA13&popupYn=false&realScreenId="
# requests data
post = "<map id=\"ATTABZAA001R08\"><pubcUserNo/><mobYn>N</mobYn><inqrTrgtClCd>1</inqrTrgtClCd><txprDscmNo>Biznum</txprDscmNo><dongCode>81</dongCode><psbSearch>Y</psbSearch><map id=\"userReqInfoVO\"/></map><nts<nts>nts>58cKuokaDhrUdtF8gFLDQZU6XMel7xRdgvDvT322quE47"
def biznum(number):
    # requests post
    res = requests.post(url, data=post.replace("Biznum", number))
    # requests post 결과값에서 smpcBmanTrtCntn 가져오기
    status = ET.fromstring(res.text).findtext("smpcBmanTrtCntn")
    # requests post 결과값에서 trtCntn 가져오기
    comment = ET.fromstring(res.text).findtext("trtCntn")
    # 출력문구
    result = status + " / " + comment
    return result

# Biznum 순서대로 불러오기
for bizno in Biznum:
    # "-"가 있으면 제거
    biz_no = bizno.replace("-", "")
    # 사업자 조회 함수 호출
    inquiry = biznum(biz_no)
    # 결과 출력
    print(str(Biznum.index(bizno) + 1) + " / " + str(len(Biznum)) + " - " + bizno + " : " + inquiry)