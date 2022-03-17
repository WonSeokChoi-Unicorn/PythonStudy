from io import BytesIO
import win32clipboard
from PIL import Image

def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()

filepath = 'testimage.jpg'
image = Image.open(filepath)

output = BytesIO()
image.convert("RGB").save(output, "BMP")
data = output.getvalue()[14:]
output.close()

# 아래 명령어 실행 후 그림판에 붙혀 넣기 하면 testimage.jpg가 보입니다
send_to_clipboard(win32clipboard.CF_DIB, data)