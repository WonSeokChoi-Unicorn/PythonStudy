from datetime import date
from datetime import datetime
from datetime import timedelta

# 오늘
today = date.today()
print("오늘 : " + today.strftime("%Y-%m-%d"))
# 지난 주 timedelta(weeks = 1) 금요일 5 구하기
lastweekfriday = datetime.strptime((today - timedelta(weeks = 1)).strftime("%Y%W") + "-5", '%Y%W-%w')
print("지난 주 금요일 : " + lastweekfriday.strftime("%Y-%m-%d"))
# 이번 주 목요일 4 구하기
thisweekthursday = datetime.strptime(today.strftime("%Y%W") + "-4", '%Y%W-%w')
print("이번 주 목요일 : " + thisweekthursday.strftime("%Y-%m-%d"))