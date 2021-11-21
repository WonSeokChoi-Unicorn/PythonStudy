# 1. 설치 : 
# https://github.com/UB-Mannheim/tesseract/wiki 에서 OS에 맞는 것을 설치합니다 (사용할 language는 선택 필요)
# pip install pytesseract
import pytesseract
# tesseract 설치 경로를 적어줍니다 (시스템 변수로 지정해도 됨)
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
# Page segmentation modes(–psm):
# 0 - Orientation and script detection (OSD) only.
# 1 - Automatic page segmentation with OSD.
# 2 - Automatic page segmentation, but no OSD, or OCR.
# 3 - Fully automatic page segmentation, but no OSD. (Default)
# 4 - Assume a single column of text of variable sizes.
# 5 - Assume a single uniform block of vertically aligned text.
# 6 - Assume a single uniform block of text.
# 7 - Treat the image as a single text line.
# 8 - Treat the image as a single word.
# 9 - Treat the image as a single word in a circle.
# 10 - Treat the image as a single character.
# 11 - Sparse text. Find as much text as possible in no particular order.
# 12 - Sparse text with OSD.
# 13 - Raw line. Treat the image as a single text line, bypassing hacks that are Tesseract-specific.
# .\\testimage1.jpg를 korean으로 변환하고, 단어들 사이에서 감지하는 공간의 수는 1, psm은 1
print(pytesseract.image_to_string('testimage1.jpg',lang='kor', config='-c preserve_interword_spaces=1 --psm 1'))
# .\\testimage2.jpg를 korean으로 변환하고, 단어들 사이에서 감지하는 공간의 수는 1, psm은 1
print(pytesseract.image_to_string('testimage2.jpg',lang='kor', config='-c preserve_interword_spaces=1 --psm 1'))
# 웹페이지의 이미지를 바로 변환할 수 있는 지는 확인 예정