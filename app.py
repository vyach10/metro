import telebot
import re

API_TOKEN = '853778348:AAFSMMu5Lvz9_Jg1j9P7L-efBu3ay1RzPKs'
bot = telebot.TeleBot(API_TOKEN)

f = open('files/listmsk.txt', 'r')   # здесь лежит файл со станциями:
content = f.readlines()

@bot.message_handler(func=lambda message: True)
def echo_message(message):
  poisk=str(message.text)
  if poisk=='start/':
  	bot.reply_to(message, 'Приветствую! Введите имя или слово для поиска.'.format(message.text))
  print(poisk)
  elif:
  	ans = 'Ваш запрос содержится в станциях:\n'
  	shablon = ''
  		for i in range(0,len(poisk)):
    		shablon = shablon+poisk[i]
    		shablon = shablon+'.'
    		shablon = shablon+'*'
  		for i in range(0,len(content)):
    		mat = re.search(shablon, content[i], re.I)
    	if mat:
      		ans=ans+'\n'+content[i][0:len(content[i])-1]
  		if ans=='Ваш запрос содержится в станциях:\n':
    	ans='Запрос не содержится ни в одной из станций :('
  	bot.reply_to(message, ans.format(message.text))
  print(ans)
bot.polling()