from telebot import types
import telebot
import re

API_TOKEN = '853778348:AAFSMMu5Lvz9_Jg1j9P7L-efBu3ay1RzPKs'
bot = telebot.TeleBot(API_TOKEN)

f = open('files/moscow.txt', 'r')   # здесь лежит файл со станциями:
content = f.readlines()

@bot.message_handler(func=lambda message: True)

def echo_message(message):
  poisk=str(message.text)
  print(poisk)
  ans = ''
  shablon = ''
  for i in range(0,len(poisk)):
    shablon = shablon+poisk[i]
    shablon = shablon+'.'
    shablon = shablon+'*'
  for i in range(0,len(content)):
    mat = re.search(shablon, content[i], re.I)
    if mat:
      ans=ans+'\n'+content[i][0:len(content[i])-1]
  if ans=='':
    ans='Запрос не содержится ни в одной из станций'
  msg2 = bot.reply_to(message, ans.format(message.text))
  print(ans)
  bot.register_next_step_handler(msg2, echo_message)

bot.polling(none_stop=True)