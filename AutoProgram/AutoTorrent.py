# application 실행하기 위한 라이브러리 import
from pywinauto import application
# application 실행하기 위한 명령어 단축
app = application.Application()
# 경로에 기본 확장 문자(escape sequence)를 피하기 위해서 역슬래시를 2개 사용
app.start("C:\\Program Files (x86)\\Transmission Remote GUI\\transgui.exe")
