# pip install Pillow
from PIL import Image

# test_webp.webp를 읽기
im = Image.open('test_webp.webp').convert('RGB')
# test_webp.jpg로 저장
im.save('test_webp.jpg', 'jpeg')
# Image file formats - https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html