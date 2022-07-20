import json
from vtapi3 import VirusTotalAPIFiles, VirusTotalAPIError
from datetime import datetime

# 바이러스토탈 API 키
# 1. https://www.virustotal.com/gui/join-us 에서 회원 가입
# 2. 가입시 입력한 이메일로 VirusTotal Community account activation 진행
# 3. https://www.virustotal.com/gui/user/[유저 네임]/apikey 에서 API Key 확인
vt_files = VirusTotalAPIFiles('API Key')

filelists = [
"C:\\Temp\\VirusScan\\file1.exe",
"C:\\Temp\\VirusScan\\file2.exe"
            ]

for file in filelists:
    try:
        # 파일ID 얻기
        file_id = VirusTotalAPIFiles.get_file_id(file)
    except VirusTotalAPIError as err:
        # 오류 출력
        print(err, err.err_code)
    else:
        try:
            # 파일 레포트 얻기
            get_report_result = vt_files.get_report(file_id)
        except VirusTotalAPIError as err:
            # 오류 출력
            print(err, err.err_code)
        else:
            # 레포트 출력
            if vt_files.get_last_http_error() == vt_files.HTTP_OK:
                get_report_result = json.loads(get_report_result)
                if get_report_result['data']['attributes'].get('names') is not None:
                    print("Names : " + get_report_result['data']['attributes']['names'][0])
                if get_report_result['data']['attributes']['signature_info'].get('product') is not None:
                    print("Product : " + get_report_result['data']['attributes']['signature_info']['product'])
                if get_report_result['data']['attributes']['signature_info'].get('description') is not None:
                    print("Description : " + get_report_result['data']['attributes']['signature_info']['description'])
                if get_report_result['data']['attributes']['signature_info'].get('original name') is not None:
                    print("Original Name : " + get_report_result['data']['attributes']['signature_info']['original name'])
                if get_report_result['data']['attributes']['signature_info'].get('internal name') is not None:
                    print("Internal Name : " + get_report_result['data']['attributes']['signature_info']['internal name'])
                if get_report_result['data']['attributes']['signature_info'].get('file version') is not None:
                    print("File Version : " + get_report_result['data']['attributes']['signature_info']['file version'])
                if get_report_result['data']['attributes'].get('size') is not None:
                    print("File size : " + str('{:,}'.format(get_report_result['data']['attributes']['size'])) + " byte(s)")
                if get_report_result['data']['attributes']['signature_info'].get('copyright') is not None:
                    print("Copyright : " + get_report_result['data']['attributes']['signature_info']['copyright'])
                if get_report_result['data']['attributes'].get('creation_date') is not None:
                    createtime = datetime.utcfromtimestamp(get_report_result['data']['attributes']['creation_date'])
                    print("Creation Time UTC : " + createtime.strftime('%Y-%m-%d %H:%M:%S'))
                if get_report_result['data']['attributes'].get('first_submission_date') is not None:
                    firsttime = datetime.utcfromtimestamp(get_report_result['data']['attributes']['first_submission_date'])                
                    print("First Submission UTC : " + firsttime.strftime('%Y-%m-%d %H:%M:%S'))
                if get_report_result['data']['attributes'].get('last_submission_date') is not None:
                    lasttime = datetime.utcfromtimestamp(get_report_result['data']['attributes']['last_submission_date'])
                    print("Last Submission UTC : " + lasttime.strftime('%Y-%m-%d %H:%M:%S'))
                if get_report_result['data']['attributes'].get('md5') is not None:
                    print("MD5 : " + get_report_result['data']['attributes']['md5'])
                if get_report_result['data']['attributes'].get('sha1') is not None:
                    print("SHA-1 : " + get_report_result['data']['attributes']['sha1'])
                if get_report_result['data']['attributes'].get('sha256') is not None:
                    print("SHA-256 : " + get_report_result['data']['attributes']['sha256'])
                cnt = 1
                for i1 in get_report_result['data']['attributes']['last_analysis_results']:
                    # 검사 결과가 None이 아닐 경우에만 출력
                    if get_report_result['data']['attributes']['last_analysis_results'][i1]['result'] is not None:
                        print(str(cnt))
                        for i2 in get_report_result['data']['attributes']['last_analysis_results'][i1]:                        
                            print(i2 + " : " + str(get_report_result['data']['attributes']['last_analysis_results'][i1][i2]))
                        cnt += 1
                print("-------------------------")
            # 오류 출력
            else:
                print('HTTP Error [' + str(vt_files.get_last_http_error()) +']')