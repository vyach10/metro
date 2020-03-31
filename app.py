from telebot import types
import telebot
import re

API_TOKEN = '853778348:AAFSMMu5Lvz9_Jg1j9P7L-efBu3ay1RzPKs'
bot = telebot.TeleBot(API_TOKEN)
city = ''
content = ''

@bot.callback_query_handler(func=lambda call: True)     #обработчик клавиатуры
def callback_worker(call):
    if call.data == "Moscow": #call.data это callback_data, которую мы указали при объявлении кнопки
        f = open('files/moscow.txt', 'r')   # здесь лежит файл со станциями:
        content = f.readlines()
        city == str(call.data)
        msg = bot.send_message(call.message.chat.id, 'Установлен город: Москва\nВведите слово для поиска:');        
    bot.register_next_step_handler(msg, echo_message);
    
#if city == "Moscow":
#  print('Москва')
#  f = open('/content/drive/My Drive/Colab Notebooks/MetroPeople/list_msk.txt', 'r')   # здесь лежит файл со станциями:
#else:

@bot.message_handler(func=lambda message: True)

def echo_message(message):
  if message.text == '/start':
      keyboard = types.InlineKeyboardMarkup(row_width=4); #наша клавиатура
      key_yes = types.InlineKeyboardButton(text='Москва', callback_data='Moscow'); #кнопка "Москва"
      keyboard.add(key_yes); #добавляем кнопку в клавиатуру
      bot.send_message(message.from_user.id, text='Выберите город:', reply_markup=keyboard)
  else:
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