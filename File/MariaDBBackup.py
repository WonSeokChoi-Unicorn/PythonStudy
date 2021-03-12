import pymysql
from os import system
from datetime import datetime

# 서버 주소 적기
host = ' '
# 서버 접속 아이디 적기
dbuser = ' '
# 서버 접속 아이디의 비밀번호 적기
password = ' '
# 백업할 DB명을 적기
dbname = ' '

# 백업할 DB 내 테이블 명 가져오기
conn = pymysql.connect(host=host, user=dbuser, password=password,db=dbname)
c = conn.cursor()
c.execute('SHOW TABLES')
tablelist = [ x[0] for x in c.fetchall() ]
c.close()
conn.close()

# mysqldump.exe 는 미리 Path에 있어야 됨
prefix_date = str(datetime.today().date())
program = 'mysqldump.exe'

# 테이블 단위로 백업하기
# for table in tablelist:
#     print("Backup DB : " + dbname + " / table : " + table)
#     command = '%s -h %s --user=%s --password=%s --tables %s %s > %s_%s_%s_backup.sql' %(program, host, dbuser, password, dbname, table, prefix_date, dbname, table)
#     system(command)

# DB 단위로 백업하기
print("Backup DB : " + dbname)
command = "%s -h %s --user=%s --password=%s %s > %s_%s_backup.sql" %(program, host, dbuser, password, dbname, prefix_date, dbname)
system(command)