# -*- coding: utf-8 -*-
import socket
from datetime import datetime
from getmac import get_mac_address
import multiprocessing
import time

# 쓰레드 시작 간격 50ms
threadInterval = 0.05 

def scan(addr, queue):
   # AF_INET는 IP version 4 사용하겠다는 의미
   # SOCK_STREAM는 TCP 패킷을 받겠다는 의미
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   # 객체의 기본 시간 제한(초) 
   socket.setdefaulttimeout(1)
   # s.connect_ex((host, port))
   # 135번 포트
   # 컴퓨팅에서 분산 컴퓨팅 환경(DCE)에 사용되는 포트
   # 인터넷에서 원격 프로시저 호출(RPC)에 사용되는 포트
   result = s.connect_ex((addr, 135))
   if result == 0:
      # IP가 있으면 queue 에 해당 IP 추가   
      queue.put(addr)
      return 1
   else :
      return 0

if __name__ == '__main__':
   # C-Class IP 입력 받음
   cclassipfull = input("Enter the C-Class IP address (XXX.XXX.XXX.XXX): ")
   # IP 구분자
   splitdot = '.'
   # IP를 구분자로 나누기
   cclassipsplit = cclassipfull.split(splitdot)
   # IP를 C-Class로 만들기
   cclassip = cclassipsplit[0] + splitdot + cclassipsplit[1] + splitdot + cclassipsplit[2] + splitdot
   # 시작 IP
   start = int(input("Enter the Starting Number (1~255): "))
   # 종료 IP
   end = int(input("Enter the Last Number (1~255): "))
   # 현재 시간
   t1 = datetime.now()
   # multiprocessing Manager 객체 생성
   m = multiprocessing.Manager()
   # multiprocessing용 큐
   queue = m.Queue()
   # threadpool 리스트
   threadpool = []
   for ip in range(start, end + 1):
      # 검색 IP 만들기
      addr = cclassip + str(ip)
      # multiprocessing으로 쓰레드 생성
      p = multiprocessing.Process(target = scan, args=(addr, queue))
      # threadpool에 추가
      threadpool.append(p)

   # 쓰레드 시작
   for th in threadpool:
      th.start()
      time.sleep(threadInterval)

   # 모든 쓰레드가 종료될 때까지 대기
   for th in threadpool:
      th.join()

  # queue에 있는 IP주소 화면에 출력  
   while queue.empty() == False:
      # 실행 결과가 1인 경우만
      ip = queue.get(1)
      # 출력
      print ("IP :", ip, ", Macaddress :", get_mac_address(ip = ip), "is live")         

   # 현재 시간
   t2 = datetime.now()
   # 소요 시간
   total = t2 - t1
   # 소요 시간 출력
   print ("Scanning completed in: ", total)