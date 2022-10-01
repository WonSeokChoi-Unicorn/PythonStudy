from datetime import datetime, timedelta
import re

# 숫자 형식을 날짜로 변경
def excel_n2d(num):
	return (datetime(1899,12,30) + timedelta(int(num))).strftime('%Y-%m-%d')

print(excel_n2d(44835))

# 날짜 형식을 숫자로 변경
def excel_d2n(date):
	dd = re.findall('\d+', date)
	return (datetime(int(dd[0]),int(dd[1]),int(dd[2])) - datetime(1899,12,30)).days

print(excel_d2n('2022-10-01'))