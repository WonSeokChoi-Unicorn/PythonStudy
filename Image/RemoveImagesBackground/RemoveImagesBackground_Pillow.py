# https://github.com/danielgatis/rembg
# Installation
# CPU support:
# pip install rembg
from rembg import remove
from PIL import Image

# 배경을 없앨 이미지 
input_path = 'C:\Temp\\sample.jpg'
# 투명 배경 있으니까 png로 저장
output_path = 'C:\Temp\\sample1.png'

input = Image.open(input_path)
output = remove(input)
output.save(output_path)