# pip install psutil
import psutil
from datetime import datetime
# 파일 존재 여부 확인 위한 os를 import 한다.
import os
# 파이썬 내장 쓰레딩 함수 
import threading
import time

# 폴더 생성
def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")
# CPU, RAM 모니터링
def monitoring():
    while True:
        # 1시간(3,600초)마다 반복 실행
        time.sleep(3600)
        # 오늘 날짜를 YYYYMMDD 형태로 변경
        today = datetime.today().strftime('%Y%m%d')
        # log 저장할 경로
        savepath = "D:\\temp\\" + today + "_monitoring\\"
        # log 저장할 경로 체크 및 생성
        createDirectory(savepath)
        contents = ""
        # 시간1
        datetime1 = datetime.now()
        print(datetime1.strftime('%Y-%m-%d %H:%M:%S') + " - Starting")
        cpu_percent = psutil.cpu_percent()
        contents += datetime1.strftime('%Y-%m-%d %H:%M:%S') + " / CPU : " + str(cpu_percent) + "\r"
        mem_percent = psutil.virtual_memory()
        contents += datetime1.strftime('%Y-%m-%d %H:%M:%S') + " / RAM : Total - " + format(int(str(mem_percent[0])[:-6]), ',') + "MB, Used - " + format(int(str(mem_percent[3])[:-6]), ',') + "MB, Free - " + format(int(str(mem_percent[4])[:-6]), ',') + "MB"
        f = open(savepath + datetime1.strftime('%Y%m%d%H%M%S') + ".txt", 'a')
        f.write(contents)
        f.close
        # 시간2
        datetime2 = datetime.now()
        print(datetime2.strftime('%Y-%m-%d %H:%M:%S') + " - Ending")
        # 시작 시간과 종료 시간의 차이를 구한다
        print(datetime1.strftime('%Y-%m-%d %H:%M:%S') + " ~ " + datetime2.strftime('%Y-%m-%d %H:%M:%S'))
        print(datetime2 - datetime1)

# 함수 실행 명령어
monitoringrun = threading.Thread(target = monitoring)
# 함수 실행
monitoringrun.start()