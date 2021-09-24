# application 실행하기 위한 라이브러리 import
from pywinauto import application
import pywinauto
# 64bit Python 사용하면서 32bit 어플리케이션 자동화시 나오는 UserWarning를 없애기 위해 import
import warnings
warnings.simplefilter('ignore', category=UserWarning)
# 클립보드로 복사하기 위한 라이브러리 import
import clipboard
import time
# application 실행하기 위한 명령어 단축
app = application.Application()
# 클립보드 초기화
clipboard.copy("")
# magnet 주소를 정리한 텍스트 파일을 한 줄씩 읽어 옵니다
# 경로에 기본 확장 문자(escape sequence)를 피하기 위해서 역슬래시를 2개 사용
f = open("자석 주소 파일명.txt", 'r')
# 한 줄씩 읽기
lines = f.readlines()
for line in lines:
    # 빈 줄일 경우 통과
    if line.strip() == "":
        continue
    clipboard.copy(line)
    # 1초 대기
    time.sleep(1.0)
    # 경로에 기본 확장 문자(escape sequence)를 피하기 위해서 역슬래시를 2개 사용
    # 2021.09.24 Application is not loaded correctly (WaitForInputIdle failed) 경고 없애기 위해서 wait_for_idle=False 옵션 추가
    app.start("C:\\Program Files (x86)\\Transmission Remote GUI\\transgui.exe", wait_for_idle=False)
    # 3분 대기
    time.sleep(180.0)
    # 확인 버튼은 Button2
    app.window(title_re="새 토렌트 추가.*").Button2.click()
    # 1초 대기
    time.sleep(1.0)
    # 프로그램 종료
    app.kill()
f.close()

