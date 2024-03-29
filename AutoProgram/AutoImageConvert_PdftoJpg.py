#-*- coding:utf-8 -*-
import os
# pip install pdf2image
from pdf2image import convert_from_path
# poppler 다운로드
# https://github.com/oschwartz10612/poppler-windows/releases/
# C:\\Program Files\\poppler에 압축 해제

# 폴더 생성
def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

# 읽어 들일 PDF 경로
fromfile = "C:\\test.pdf"
# 저장할 jpg 경로
tofile = "C:\\temp\\pdfimage\\"
# 저장할 jpg 파일명
tofilename = "test"
# 저장할 jpg 경로 체크
createDirectory(tofile)
# 변환
pdfpages = convert_from_path(fromfile, poppler_path = 'C:\\Program Files\\poppler\\library\\bin')
# 파일명용 카운트
cnt = 1
# PDF 페이지별 이미지 읽기
for image in pdfpages:
    # 파일명 지정
    filename = tofile + tofilename + '_' + str(cnt) +'.jpg'
    # jpg 저장
    image.save(filename)
    # 변환 파일명(경로 포함) 출력
    print(filename)
    cnt += 1