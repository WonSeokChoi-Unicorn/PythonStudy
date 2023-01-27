from datetime import datetime
from dateutil.relativedelta import relativedelta
from korean_lunar_calendar import KoreanLunarCalendar
# 음력 달력 개체 생성
calendar = KoreanLunarCalendar()
# 오늘 날짜 가져오기
nowDate = datetime.now()
# 1년 전
before1yearYYYY = (nowDate - relativedelta(years = 1)).strftime('%Y')
# 1년 후
after1yearYYYY = (nowDate + relativedelta(years = 1)).strftime('%Y')
# TEST Intercalation 생일
# nowDate = datetime(2023, 3, 22)
# TEST Lunar 생일
# nowDate = datetime(2023, 1, 22)
# TEST Solar 결혼기념일
# nowDate = datetime(2023, 3, 1)
# 날짜를 MMDD 형태로 변경
today = nowDate.strftime('%m%d')
# 날짜를 YYYY 형태로 변경
todayYYYY = nowDate.strftime('%Y')
# 날짜를 MM 형태로 변경
todayMM = nowDate.strftime('%m')
# 날짜를 DD 형태로 변경
todayDD = nowDate.strftime('%d')
# 날짜 자리수 구분
# 첫째 자리 : 양력이면 S, 음력이면 L
# 둘째 자리 : 음력 윤달이면 Y, 음력 평달이면 N, 양력이면 S
# 셋째 자리 ~ 열째 자리 : 생년월일(YYYYMMDD)
Birthdaylist = {
                "TEST Intercalation 생일" : "LY20230201",
                "TEST Lunar 생일"         : "LN20230101",
                "TEST Solar 결혼기념일"    : "SS20230301"
               }
# 기념일 존재 초기화
cnt = 0
# 기념일 리스트 순서대로 확인
for key, value in Birthdaylist.items():
    # 양력 날짜 초기화
    solardate = ''
    # 기념일 초기화
    anniversaryYYYY = ''
    anniversaryMMDD = ''
    # 음력인지 양력인지 확인
    if value[0] == 'L':
        # 날짜 - 일
        day = int(value[-2:])
        # 날짜 - 월
        month = int(value[-4:-2])
        if value[1:1+1] == 'N':
            # 음력을 양력으로 변환 (윤달 아님)
            calendar.setLunarDate(int(todayYYYY), month, day, False)
        else:
            # 음력을 양력으로 변환 (윤달)
            calendar.setLunarDate(int(todayYYYY), month, day, True)
        # 양력
        solardate = calendar.SolarIsoFormat()
        # '-' 제거
        solardate = solardate.replace('-','')
        # 연도 가져옴
        anniversaryYYYY = solardate[:3 + 1]
        # 1년 후 연도가 나오면 1년 전 연도로 다시 확인
        if anniversaryYYYY == after1yearYYYY:
            # 음력을 양력으로 변환 (윤달은 없다고 가정)
            calendar.setLunarDate(int(before1yearYYYY), month, day, False)
            # 양력
            solardate = calendar.SolarIsoFormat()
            # '-' 제거
            solardate = solardate.replace('-','')
            # 연도 가져옴
            anniversaryYYYY = solardate[:3 + 1]
        # 월일만 가져옴
        anniversaryMMDD = solardate[-4:]
    else:
        # 양력이라 현재 연도 가져옴
        anniversaryYYYY = todayYYYY
        # 월일만 가져옴
        anniversaryMMDD = value[-4:]
    # 오늘과 기념일의 연도를 확인
    if anniversaryYYYY != todayYYYY:
        # 다음으로 진행
        print("기념일의 날짜는 오늘지만, 연도가 " + anniversaryYYYY + "라서 알리지 않습니다.")
        continue
    # 오늘의 월일과 기념일의 월일을 확인
    if today == anniversaryMMDD:
        # 기념일 존재
        cnt += 1
        # 안내문구
        text = todayYYYY + "/" + anniversaryMMDD[:2] + "/" + anniversaryMMDD[-2:] + " is " + key
        # 안내문구 출력
        print(text)
# 기념일이 없음
if cnt == 0:
    # 기념일이 없다고 출력
    print("No one has a anniversary today.")