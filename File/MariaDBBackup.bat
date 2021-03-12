REM 년, 월, 일을 변수로 생성
@set YEAR=%date:~0,4%
@set MONTH=%date:~5,2%
@set DAY=%date:~8,2%
REM 아래는 3가지 합한 변수 예시 
@set DATE=%YEAR%%MONTH%%DAY%
REM 백업 경로로 이동
D:
cd Backup
REM D:\MariaDB 10.5\bin\mysqldump.exe는 본인 PC에 맞는 경로로 수정 필요
REM [id], [password]에 괄호 제외하고 입력
REM backup_investar_db_20210312.sql 로 파일 생성
"D:\MariaDB 10.5\bin\mysqldump.exe" -u[id] -p[password] investar > "backup_investar_db_%YEAR%%MONTH%%DAY%.sql"