# Telegram 알림을 사용하기 위한 telegram
# pip install python-telegram-bot --upgrade
import telegram

# Telegram 봇의 토큰(HTTP API)을 적어 줍니다
telegrambot = telegram.Bot(token = "0000000000:")
# 고정으로 사용할 채팅방 아이디를 적어 줍니다
telegramchatid = 0000000000
# 가장 최근에 온 메세지의 정보 중, chat id만 가져옴
# telegramchatid  =  telegrambot.getUpdates()[-1].message.chat.id 
# 보낼 내용
text = "테스트입니다."
# 채팅방에 내용 보내기
telegrambot.sendMessage(chat_id = telegramchatid, text = text)