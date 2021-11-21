# coding=UTF-8
# 1. 설치 : 
# pip install -U pip setuptools wheel
# pip install -U spacy
# 2. 한국어는 공식 지원하지 않아서 다국어 모듈 필요 
# https://spacy.io/models/xx
# python -m spacy download xx_ent_wiki_sm
# python -m spacy download xx_sent_ud_sm
# 3. 첫 줄에 인코딩 방식을 주석으로 선언 필요
import spacy

# GPU 사용하기 위한 명령어 (또는 spacy.require_gpu())
spacy.prefer_gpu()

text = '에스페란토는 유대계 폴란드인 안과의사였던 루도비코 라자로 자멘호프가 국제적 의사소통을 위한 공용어를 목표로 하여 1887년에 발표한 인공어이다. 에스페란토라는 명칭은 에스페란토로 "희망하는 사람"이라는 뜻이며 자멘호프가 에스페란토 문법서를 처음 발표할 당시에 사용한 가명(D-ro Esperanto)에서 유래하였다. 흔히 "에스페란토어"라고 쓰기도 하는데, 에스페란토라는 사람 무리나 에스페란토라는 나라에서 쓰는 말이 아니기 때문에 엄밀히는 겹말이지만 산스크리트어의 예도 있고 해서 무작정 틀린 말이라고 할 수는 없다. 에스페란토 사용자는 전 세계적으로 200만 명에 이르는 것으로 추산되며, 이는 인공어 중에서는 가장 많은 수치이다. 에스페란토를 모국어로 구사하는 사람도 수천 명으로 추정되고 있는데, 이 경우는 부모가 모두 에스페란토를 구사해 자연스럽게 이를 모국어로 습득한 경우다. 세계 에스페란토 대회(Universala Kongreso de Esperanto)도 있는데, 1905년부터 지금까지 매년 열린다. 1994년에는 대한민국 서울특별시에서 개최되기도 했고, 2015년에는 대망의 100차 대회가 프랑스의 도시 릴에서 개최되었다. 또한 2017년 대회가 다시 대한민국 서울 한국외국어대학교에서 7월 29일까지 진행되었다.'

nlp1 = spacy.load('xx_ent_wiki_sm')
# 문장 경계 감지를 위한 파이프라인 구성 요소
nlp1.add_pipe('sentencizer')
doc1 = nlp1(text)
word_tokenized_sentence1 = [token1.text for token1 in doc1]
sentence_tokenized_list1 = [sent1.text for sent1 in doc1.sents]
print("xx_ent_wiki_sm")
print(word_tokenized_sentence1)
print(sentence_tokenized_list1)

nlp2 = spacy.load('xx_sent_ud_sm')
# 문장 경계 감지를 위한 파이프라인 구성 요소
nlp2.add_pipe('sentencizer')
doc2 = nlp2(text)
word_tokenized_sentence2 = [token2.text for token2 in doc2]
sentence_tokenized_list2 = [sent2.text for sent2 in doc2.sents]
print("xx_sent_ud_sm")
print(word_tokenized_sentence2)
print(sentence_tokenized_list2)