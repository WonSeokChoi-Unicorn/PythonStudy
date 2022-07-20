import json
# pip install vtapi3
from vtapi3 import VirusTotalAPIUrls, VirusTotalAPIError
from datetime import datetime

# 바이러스토탈 API 키
# 1. https://www.virustotal.com/gui/join-us 에서 회원 가입
# 2. 가입시 입력한 이메일로 VirusTotal Community account activation 진행
# 3. https://www.virustotal.com/gui/user/[유저 네임]/apikey 에서 API Key 확인
vt_urls = VirusTotalAPIUrls('')

urllists = [
"URL 1",
"URL 2"
           ]

for url in urllists:
    try:
        # URL ID 얻기
        url_id = VirusTotalAPIUrls.get_url_id_base64(url)
    except VirusTotalAPIError as err:
        # 오류 출력
        print(err, err.err_code)
    else:
        try:
            # 파일 레포트 얻기
            get_report_result = vt_urls.get_report(url_id)
        except VirusTotalAPIError as err:
            # 오류 출력
            print(err, err.err_code)
        else:
            # 레포트 출력
            if vt_urls.get_last_http_error() == vt_urls.HTTP_OK:
                get_report_result = json.loads(get_report_result)
                # get_report_result = json.dumps(get_report_result, sort_keys=False, indent=4)
                # print(get_report_result)
                if get_report_result['data']['attributes'].get('last_final_url') is not None:
                    print("Final URL : " + get_report_result['data']['attributes']['last_final_url'])
                if get_report_result['data']['attributes'].get('last_http_response_code') is not None:
                    print("Status Code : " + str(get_report_result['data']['attributes']['last_http_response_code']))
                if get_report_result['data']['attributes'].get('last_http_response_content_length') is not None:
                    print("Body Length : " + str('{:0,.2f}'.format(get_report_result['data']['attributes']['last_http_response_content_length']/1024)) + " KB(s)")
                if get_report_result['data']['attributes'].get('last_http_response_content_sha256 name') is not None:
                    print("Body SHA-256 : " + get_report_result['data']['attributes']['last_http_response_content_sha256 name'])
                if get_report_result['data']['attributes'].get('title') is not None:
                    print("Title : " + get_report_result['data']['attributes']['title'])
                if get_report_result['data']['attributes'].get('first_submission_date') is not None:
                    firsttime = datetime.utcfromtimestamp(get_report_result['data']['attributes']['first_submission_date'])                
                    print("First Submission UTC : " + firsttime.strftime('%Y-%m-%d %H:%M:%S'))
                if get_report_result['data']['attributes'].get('last_modification_date') is not None:
                    firsttime = datetime.utcfromtimestamp(get_report_result['data']['attributes']['last_modification_date'])                
                    print("Last Submission UTC : " + firsttime.strftime('%Y-%m-%d %H:%M:%S'))
                for i1 in get_report_result['data']['attributes']['html_meta']:
                    list1 = get_report_result['data']['attributes']['html_meta'][i1]
                    print(i1, ":", *list1)
                for i2 in get_report_result['data']['attributes']['last_http_response_headers']:
                    print(i2 + " : " + get_report_result['data']['attributes']['last_http_response_headers'][i2])
                cnt = 1
                for i3 in get_report_result['data']['attributes']['last_analysis_results']:
                    # 검사 결과가 clean, unrated 아닐 경우에만 출력
                    if get_report_result['data']['attributes']['last_analysis_results'][i3]['result'] != 'clean' and get_report_result['data']['attributes']['last_analysis_results'][i3]['result'] != 'unrated':
                        print(str(cnt))
                        for i4 in get_report_result['data']['attributes']['last_analysis_results'][i3]:                        
                            print(i4 + " : " + str(get_report_result['data']['attributes']['last_analysis_results'][i3][i4]))
                        cnt += 1
                print("-------------------------")
            # 오류 출력
            else:
                print('HTTP Error [' + str(vt_urls.get_last_http_error()) +']')