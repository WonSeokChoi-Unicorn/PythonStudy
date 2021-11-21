# coding=UTF-8
# 1. 설치 : pip instll nltk
# 2. 코드 작성 전 실행
# import nltk
# nltk.download()
# tokenize를 사용하기 위해서는 punkt 다운로드 필요
# nltk.download('punkt')
# 3. 첫 줄에 인코딩 방식을 주석으로 선언 필요
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

text = '에스페란토는 유대계 폴란드인 안과의사였던 루도비코 라자로 자멘호프가 국제적 의사소통을 위한 공용어를 목표로 하여 1887년에 발표한 인공어이다. 에스페란토라는 명칭은 에스페란토로 "희망하는 사람"이라는 뜻이며 자멘호프가 에스페란토 문법서를 처음 발표할 당시에 사용한 가명(D-ro Esperanto)에서 유래하였다. 흔히 "에스페란토어"라고 쓰기도 하는데, 에스페란토라는 사람 무리나 에스페란토라는 나라에서 쓰는 말이 아니기 때문에 엄밀히는 겹말이지만 산스크리트어의 예도 있고 해서 무작정 틀린 말이라고 할 수는 없다. 에스페란토 사용자는 전 세계적으로 200만 명에 이르는 것으로 추산되며, 이는 인공어 중에서는 가장 많은 수치이다. 에스페란토를 모국어로 구사하는 사람도 수천 명으로 추정되고 있는데, 이 경우는 부모가 모두 에스페란토를 구사해 자연스럽게 이를 모국어로 습득한 경우다. 세계 에스페란토 대회(Universala Kongreso de Esperanto)도 있는데, 1905년부터 지금까지 매년 열린다. 1994년에는 대한민국 서울특별시에서 개최되기도 했고, 2015년에는 대망의 100차 대회가 프랑스의 도시 릴에서 개최되었다. 또한 2017년 대회가 다시 대한민국 서울 한국외국어대학교에서 7월 29일까지 진행되었다.'

# 텍스트에서 어절별로 키워드를 반환한다
word_tokens = word_tokenize(text) 
# 텍스트에서 문단별로 키워드를 반환한다
sent_tokens = sent_tokenize(text)

print(word_tokens)
print(sent_tokens)