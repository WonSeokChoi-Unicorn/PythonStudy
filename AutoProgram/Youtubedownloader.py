import os
# 유튜브 영상을 다운로드 해주는 라이브러리
# python -m pip install git+https://github.com/pytube/pytube
import pytube 
# 유튜브 영상 다운로드 진행율을 보여주는 라이브러리
from pytube.cli import on_progress 
# 유튜브 재생목록 내 영상을 다운로드 해주는 라이브러리
from pytube import Playlist

# 유튜브 URL
urls = [
         "https://www.youtube.com/watch?v=LQotmaEt-TQ"
       ]
# 유튜브 재생목록 URL
playlisturls = [
               "https://www.youtube.com/watch?v=eZTxU90MStY&list=PL3Eb1N33oAXhnfBUpXlIfGHxlGTBFccYY",
               "https://www.youtube.com/watch?v=eqnVfTJh1qI&list=PL3Eb1N33oAXhxzXBbBqmLG0XZDXxPZmfZ"
              ]

# 저장 경로
save_dir = "C:\\tmp\\"

def youtubeurls():        
    # urls에 있는 url을 담기
    for url in urls:
        # 진행 과정을 표시
        yt = pytube.YouTube(url, on_progress_callback=on_progress)
        # 유튜브 객체에서 스트리밍 관련 모든 것 가져오기
        # vids = yt.streams
        # 유튜브 객체에서 스트리밍 관련 모든 것 확인
        # for i in range(len(vids)):
        #     print(i,'. ', vids[i])
        # 다운로드 오류 발생할 것을 대비
        try:
            # progressive가 true, mp3 video만, 해상도 내림차순으로 sort해서 1번째 나오는 최고 해상도로 다운로드
            yt.streams.filter(progressive=True, file_extension='mp4').order_by("resolution").desc().first().download(save_dir)
            print("\n<" + str(urls.index(url)+1) + '/' + str(len(urls)) + "> (" + yt.author + ' - ' + yt.title + "." + yt.streams.filter(progressive=True, file_extension='mp4').order_by("resolution").desc().first().subtype + "[" + yt.streams.filter(progressive=True, file_extension='mp4').order_by("resolution").desc().first().resolution + "]" + ") 다운로드가 완료되었습니다.")
        except Exception as x:
            # 다양한 이유로 다운로드가 실패했을 경우 안내
            print("<" + str(urls.index(url)+1) + '/' + str(len(urls)) + "> (" + yt.author + ' - ' + yt.title + "." + yt.streams.filter(progressive=True, file_extension='mp4').order_by("resolution").desc().first().subtype + ") 다운로드는 아래와 같은 이유로 실패했습니다.")
            print(x)
            file = save_dir + yt.title + "." + yt.streams.filter(progressive=True, file_extension='mp4').order_by("resolution").desc().first().subtype
            # 다운로드가 실패하면 0 byte 파일이 남아서 삭제
            if os.path.isfile(file):
                os.remove(file)
                print("다운로드 실패하여 0 byte인 " + file + " 파일을 삭제했습니다.")
            else:
                print("특수 문자로 인해서 삭제 실패했을 수 있으니 0 byte인 파일(" + yt.title + ")은 삭제해주세요.")

def youtubeplaylist():
    # playlisturls에 있는 playlisturl를 담기
    for playlisturl in playlisturls:
        # Playlist 클래스에 playlisturl을 담기
        playlist = Playlist(playlisturl)
        # 진행율 표시
        print("{" + str(playlisturls.index(playlisturl)+1) + '/' + str(len(playlisturls)) + ' Playlists}')
        # urls에 있는 url을 담기
        for url in playlist:
            # 진행 과정을 표시
            yt = pytube.YouTube(url, on_progress_callback=on_progress)
            # 유튜브 객체에서 스트리밍 관련 모든 것 가져오기
            # vids = yt.streams
            # 유튜브 객체에서 스트리밍 관련 모든 것 확인
            # for i in range(len(vids)):
            #     print(i,'. ', vids[i])
            # 다운로드 오류 발생할 것을 대비
            try:
                # progressive가 true, mp3 video만, 해상도 내림차순으로 sort해서 1번째 나오는 최고 해상도로 다운로드
                yt.streams.filter(progressive=True, file_extension='mp4').order_by("resolution").desc().first().download(save_dir)
                print("\n<" + str(playlist.index(url)+1) + '/' + str(len(playlist)) + "> (" + yt.author + ' - ' + yt.title + "." + yt.streams.filter(progressive=True, file_extension='mp4').order_by("resolution").desc().first().subtype + "[" + yt.streams.filter(progressive=True, file_extension='mp4').order_by("resolution").desc().first().resolution + "]" + ") 다운로드가 완료되었습니다.")
            except Exception as x:
                # 다양한 이유로 다운로드가 실패했을 경우 안내
                print("<" + str(playlist.index(url)+1) + '/' + str(len(playlist)) + "> (" + yt.author + ' - ' + yt.title + "." + yt.streams.filter(progressive=True, file_extension='mp4').order_by("resolution").desc().first().subtype + ") 다운로드는 아래와 같은 이유로 실패했습니다.")
                print(x)
                file = save_dir + yt.title + "." + yt.streams.filter(progressive=True, file_extension='mp4').order_by("resolution").desc().first().subtype
                # 다운로드가 실패하면 0 byte 파일이 남아서 삭제
                if os.path.isfile(file):
                    os.remove(file)
                    print("다운로드 실패하여 0 byte인 " + file + " 파일을 삭제했습니다.")
                else:
                    print("특수 문자로 인해서 삭제 실패했을 수 있으니 0 byte인 파일(" + yt.title + ")은 삭제해주세요.")

run = int(input("1 : 유튜브 개별 URL 다운로드, 2 : 유튜브 재생목록 다운로드 >>"))
if run == 1:
    # url들을 다운로드 할 경우 사용
    youtubeurls()
elif run == 2:
    # playlist들을 다운로드 할 경우 사용
    youtubeplaylist()
else:
    print("잘못된 입력입니다. 1, 2 중에서 입력해주시기 바랍니다.")