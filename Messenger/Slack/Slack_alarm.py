# Slack 알림을 사용하기 위한 requests
# pip install requests --upgrade
import requests
# Slack에 알림 보내는 함수
def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
                              headers = {"Authorization" : "Bearer " + token},
                              data = {"channel" : channel, "text" : text}
                            )
    print(response)
# Slack Bot User OAuth Token을 적어 줍니다
myToken = "xoxb-"
# 보낼 내용
text = "테스트입니다."
# 보낼 채널
channel = "#test"
# 채널에 내용 보내기
post_message(myToken, channel, text)