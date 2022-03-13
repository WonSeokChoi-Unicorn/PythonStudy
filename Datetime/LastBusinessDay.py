from datetime import datetime
from datetime import timedelta
import holidays

# 한국 휴일 정보
kr_holidays = holidays.KR()

# 어제까지 중 가장 최근의 영업일
def previous_working_day(check_day_, holidays):
    offset = max(1, (check_day_.weekday() + 6) % 7 - 3)
    most_recent = check_day_ - timedelta(offset)
    if most_recent not in holidays:
        return most_recent
    else:
        return previous_working_day(most_recent, holidays)
# 한국
# 오늘 날짜를 YYYY-MM-DD 형태로 변경
today = datetime.today().strftime('%Y-%m-%d')
# 오늘 날짜를 datetime 형식으로
kr_check_day = datetime.strptime(today, '%Y-%m-%d').date()
# 한국 휴일 정보로 어제까지 중 가장 최근의 영업일
kr_beforeday1 = previous_working_day(kr_check_day, kr_holidays)
print("오늘은 " + str(kr_check_day))
print("어제까지 중 가장 최근의 영업일 " + str(kr_beforeday1))