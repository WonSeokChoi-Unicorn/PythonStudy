[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FWonSeokChoi-Unicorn%2FPythonStudy&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)
# PythonStudy
Source

파이썬을 배우면서 개발한 프로그램들입니다.

자동 프로그램

1. 토렌트 프로그램에 자석 주소로 추가 (AutoTorrent.py)

2. 구글 번역 기능을 이용하여 영어 파일 읽어서 한국어 파일 저장 (AutoTranslate_google.py)

3. 카카오 번역 기능을 이용하여 영어 파일 읽어서 한국어 파일 저장 (AutoTranslate_kakao.py)

4. korbit을 통해서 리플(XRP)의 현재가를 10분(600초)마다 확인하고, 특정금액(1,500원)이 넘을 경우 slack으로 알림 (KORBIT_inquiry.py)

5. 주식이나 암호화폐의 현재 금액을 확인하고, 목표가를 넘을 경우 slack으로 알림 (Price_inquiry.py)

6. 유튜브 개별이나 플레이리스트 URL들로 다운로드 하는 프로그램 (Youtubedownloader.py)

7. Webp 이미지를 Jpg 이미지로 변환하는 프로그램 (AutoImageConvert_WebptoJpg.py) 

8. Jfif 이미지를 Jpg 이미지로 변환하는 프로그램 (AutoImageConvert_JfiftoJpg.py)

9. 지정한 경로 및 하위 경로에 있는 파일 검색 프로그램 (Subpathsearch.py)

10. 지정한 경로 및 하위 경로에 있는 특정 확장자를 가진 파일 검색 프로그램 (SubpathsearchForExt.py)

11. 카카오 계정으로 로그인하여 다음 카페에 글 작성하는 프로그램 (DaumCafeWrite.py)

12. 카카오 계정으로 로그인하여 다음 카페에 글(HTML) 작성하는 프로그램 (DaumCafeHtmlWrite.py)

13. 이미지 파일을 불러 와서 클립보드로 복사하는 프로그램 (ImagefileToClipboard.py)

14. text1, text2 컬럼이 있는 엑셀을 읽어와서 출력하는 프로그램 (ExcelDataReader.py)

15. PDF 파일을 Jpg 이미지로 변환하는 프로그램 (AutoImageConvert_PdftoJpg.py)


크롤러 프로그램

1. 꾸르 크롤러 (ggoorr_crawler.py)

2. 유튜브 크롤러 (youtube_crawler.py)

3. 정해준 유튜브 URL을 Iframes 태그로 만들기 (youtubeiframe_crawler.py)

4. 한국 증권거래소 상장 법인 크롤러 (KRX_crawler.py)

5. 네이버 ETF 크롤러 (NaverEtf_crawler.py)

6. 한국 증권거래소 상장 법인과 네이버 ETF 크롤러 (KRXEtf_crawler.py)

7. 한국 증권거래소 상장 법인의 1년 뒤 종가 크롤러 (KRX Closing price one year later_crawler.py)

8. 오피넷 API 연동 전국 주유소 평균가격 크롤러 (Opinet_crawler.py)

9. 원하는 사이트 내 이미지들을 원하는 경로/파일명으로 저장하는 크롤러 (imagesave_crawler.py)

10. 사업자 등록 번호로 상태 조회하는 크롤러 (NTS_biznuminquiry_crawler.py)


날짜시간 시리즈

1. Holiday 라이브러리 활용 (Holidays.py)

2. 한국 공공 데이터 API 활용 (Holidays_API.py)

3. UTC <-> 서울 타임존 변환 (TimezoneConverter.py)

4. 어제까지 중 가장 최근의 영업일 확인 (LastBusinessDay.py)


파일 처리 시리즈

1. X일 지난 파일 삭제 (DeleteOldFile.py)

2. Maria DB 백업 (MariaDBBackup.py, MariaDBBackup.bat)


번호 생성기

1. 로또 번호 랜덤 생성기 (RandomLottoNumber.py)


자연어 처리

1. NLTK 설치 및 사용 (nltk.py)

2. SpaCy 설치 및 사용 (SpaCy.py)


이미지를 텍스트론 변환

1. 로컬 또는 웹 상 이미지를 텍스트로 변환 (Tesseract - Sample.py, Tesseract - Web Sample.py)


암호 화폐 거래소 관련

FTX

1. 암호 화폐 리스트 확인 (FTX_Markets.py)

2. 암호 화폐의 시장 정보 출력 (FTX_Market.py)

Upbit

1. 암호 화폐 리스트 확인 (Upbit_Ticker.py)

2. 암호 화폐 현재가 출력 (Upbit_get_current_price.py)

3. 암호 화폐 고가/시가/저가/종가/거래량 출력 (Upbit_get_ohlcv.py)

Korbit

1. 암호 화폐 리스트 확인 (Korbit_Ticker.py)

2. 암호 화폐 24시간 동안의 저가/고가/거래금액/거래량 출력 (Korbit_get_market_detail.py)

3. 암호 화폐 현재가 출력 (Korbit_get_current_price.py)

Bithumb

1. 암호 화폐 리스트 확인 (Bithumb_Ticker.py)

2. 암호 화폐 00시 기준으로 시가/고가/저가/종가/거래량 정보 (Bithumb_get_market_detail.py)

3. 암호 화폐 시가/종가/고가/저가/거래량 정보를 DataFrame으로 출력 (Bithumb_get_candlestick.py)

가 있습니다.
