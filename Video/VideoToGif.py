# pip install moviepy
from moviepy.editor import *

# 동영상 파일 불러오기
clip = VideoFileClip('C:\\Temp\\TESTVideo.mp4', audio = False)
# GIF로 저장하기, fps 14미만이면 보기 불편함
clip.write_gif('C:\\Temp\\TESTVideo.gif', fps = 14, fuzz = 1)