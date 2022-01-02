# pip install Pillow
from PIL import Image

# test.webp를 읽기
im = Image.open('test_webp.webp').convert('RGB')
# test.jpg로 저장
im.save('test_webp.jpg', 'jpeg')
# Image file formats - https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html