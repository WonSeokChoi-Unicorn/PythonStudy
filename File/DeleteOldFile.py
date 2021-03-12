import os
from datetime import datetime

def delete_old_files(path_target, days_elapsed):
    # path_target : 삭제할 파일이 있는 디렉토리, days_elapsed:경과일 수
    # 디렉토리를 확인
    for f in os.listdir(path_target): 
        f = os.path.join(path_target, f)
        # 삭제할 파일을 확인
        if os.path.isfile(f): 
            # 타임 스탬프 (단위:초)
            timestamp_now = datetime.now().timestamp()
            # st_mtime(마지막으로 수정된 시간) 기준으로 X일 경과 여부
            is_old = os.stat(f).st_mtime < timestamp_now - (days_elapsed * 24 * 60 * 60)
            # X일 경과했다면
            if is_old: 
                try:
                    # 파일을 지운다
                    os.remove(f) 
                    # 삭제 완료 출력
                    print(f, 'is deleted') 
                # Device or resource busy (다른 프로세스가 사용 중)등의 이유
                except OSError: 
                    # 삭제 불가 출력
                    print(f, 'can not delete') 

# D:\Backup 폴더에 대해서 31일 지나면 삭제토록
delete_old_files("D:\Backup", 31)