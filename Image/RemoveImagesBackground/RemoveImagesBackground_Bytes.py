# https://github.com/danielgatis/rembg
# Installation
# CPU support:
# pip install rembg
from rembg import remove

# 배경을 없앨 이미지 
input_path = 'C:\Temp\\sample.jpg'
# 투명 배경 있으니까 png로 저장
output_path = 'C:\Temp\\sample2.png'

with open(input_path, 'rb') as i:
    with open(output_path, 'wb') as o:
        input = i.read()
        output = remove(input)
        o.write(output)