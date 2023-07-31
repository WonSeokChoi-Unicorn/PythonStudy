import requests

def get_latest_chromedriver_version():
    url = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.strip()
    else:
        print(f"Failed to fetch data from the URL. Status code: {response.status_code}")
        return None

# Bot User OAuth Token을 적어 줍니다
myToken = "xoxb-"

def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers = {"Authorization" : "Bearer " + token},
        data = {"channel" : channel, "text" : text})
    print(response)

if __name__ == "__main__":
    latest_version = get_latest_chromedriver_version()
    if latest_version:
        # 출력
        print(f"The latest version of ChromeDriver is : {latest_version}")
        # message
        post_message(myToken, "#pricealarm", f"The latest version of ChromeDriver is : {latest_version}")