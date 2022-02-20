from datetime import datetime
from dateutil import tz

# 타임존 리스트 https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
# 타임존 설정
# UTC
utc_zone = tz.gettz('UTC')
# South Korea - Seoul
seoul_zone = tz.gettz('Asia/Seoul')

# 현재 UTC 시간
before_time1 = datetime.utcnow()
print("Now UTC Time : " + str(before_time1))

# UTC에서 Seoul로 타임존 변환
after_time1 = before_time1.replace(tzinfo=utc_zone).astimezone(seoul_zone)
print("Now Seoul Time : " + str(after_time1))

# 현재 Seoul 시간
before_time2 = datetime.now()
print("Now Seoul Time : " + str(before_time2))

# Seoul에서 UTC로 타임존 변환
after_time2 = before_time2.replace(tzinfo=seoul_zone).astimezone(utc_zone)
print("Now UTC Time : " + str(after_time2))