from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler

import os
import datetime
import re

token = "본인의 텔레그램봇 토큰 key 입력" # 자신의 텔레그램봇 token key 를 넣어주세요.
filepath = r"C:\Users\infomax\Documents\K-Bond Messenger Chat" # 본인 PC의 K-Bond 대화내역 갈무리 위치를 넣어주세요.

# updater 
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

def search_text(code, chatname):

    # 오늘 날짜를 yyyymmdd 형식으로 가져옵니다. (갈무리 파일명 검색을 위해)
    date_today = datetime.datetime.today().strftime('%Y%m%d')

    entries = os.listdir(filepath)
    for entry in entries:
        if (chatname + "_" + date_today) in entry:
            filename = entry
    with open(os.path.join(filepath, filename), 'r') as f:
        lines = f.readlines()

    result = []
    p = re.compile('[0-9]{1,2}-[0-9]{1,2}')
    if p.search(code) == None: # 21-2 와 같은 종목명 형식이 아니면
        matches = [code] # 검색어 전체로 검색합니다.
    else: # 검색단어가 21-2와 같은 종목명 형식이면 전화번호와도 겹치는것을 피하고자 검색어를 좀 조정합니다.
        matches = [': '+code, code+' ', code+'+', code+'-']
    for line in lines:
        if any(x in line for x in matches):
            result.append(line)
    return result[-50:]

def search1(update, context): # /1 명령시 호출되는 함수
    log(update)
    result = search_text(context.args[0], "블커본드")
    context.bot.send_message(chat_id=update.effective_chat.id, text="블커본드 대화방 검색결과입니다.")
    context.bot.send_message(chat_id=update.effective_chat.id, text="".join(result))

def search2(update, context): # /2 명령시 호출되는 함수
    log(update)
    result = search_text(context.args[0], "막무가내")
    context.bot.send_message(chat_id=update.effective_chat.id, text="막무가내 대화방 검색결과입니다.")
    context.bot.send_message(chat_id=update.effective_chat.id, text="".join(result))

def log(update): # user의 unique id 와 검색어를 터미널 화면에 출력합니다. (정상작동 모니터링)
    user_id = update.effective_chat.id
    user_text = update.message.text
    nowTime = datetime.datetime.now().strftime('%H:%M:%S')
    
    print(nowTime, user_id, user_text)

# message handler
def echo(update, context): # /1, /2 등의 명령어 형태가 아니라 단순 검색어 입력시
    log(update)
    result = search_text(update.message.text, "블커본드")
    context.bot.send_message(chat_id=update.effective_chat.id, text="블커본드 대화방 검색결과입니다.")
    context.bot.send_message(chat_id=update.effective_chat.id, text="".join(result))

search1_handler = CommandHandler('1', search1, pass_args=True)
dispatcher.add_handler(search1_handler)

search2_handler = CommandHandler('2', search2, pass_args=True)
dispatcher.add_handler(search2_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

# polling
updater.start_polling()
