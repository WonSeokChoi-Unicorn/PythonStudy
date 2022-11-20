# https://github.com/danielgatis/rembg
# Installation
# CPU support:
# pip install rembg
from rembg import remove
import cv2

# 배경을 없앨 이미지 
input_path = 'C:\Temp\\sample.jpg'
# 투명 배경 있으니까 png로 저장
output_path = 'C:\Temp\\sample3.png'

input = cv2.imread(input_path)
output = remove(input)
cv2.imwrite(output_path, output)