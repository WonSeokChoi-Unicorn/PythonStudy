import os

# 파일명에서 유지할 것들
keeplist = [',', '-', '_', '.', ' ', '(', ')', '[', ']', '|', '#', "'"]

def rename_files_in_directory(pathname):
    # 하위 경로 검색
    for (path, dir, files) in os.walk(pathname):
        for filename in files:
            # 파일이 아닌 경우 건너뜁니다.
            if not os.path.isfile(os.path.join(path, filename)):
                continue
            # 파일명 변경
            new_filename = ''.join(c for c in filename if c.isalnum() or c in keeplist)
            # 다를 경우에만 변경
            if filename != new_filename:
                # 파일명 변경 처리
                os.rename(os.path.join(path, filename), os.path.join(path, new_filename))
                # 진행
                print("변경 전 파일명 : " + os.path.join(path, filename) + ", 변경 후 파일명 : " + os.path.join(path, new_filename))

rename_files_in_directory("C:\\Tmp")