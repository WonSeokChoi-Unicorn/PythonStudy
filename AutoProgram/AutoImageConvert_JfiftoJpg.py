# pip install Pillow
from PIL import Image

# test_jfif.jfif를 읽기
im = Image.open('test_jfif.jfif').convert('RGB')
# test_jfif.jpg로 저장
im.save('test_jfif.jpg', 'jpeg')
# Image file formats - https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html