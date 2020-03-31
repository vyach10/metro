from telebot import types
import telebot
import re

API_TOKEN = '853778348:AAFSMMu5Lvz9_Jg1j9P7L-efBu3ay1RzPKs'
bot = telebot.TeleBot(API_TOKEN)

city = ''

@bot.callback_query_handler(func=lambda call: True)     #обработчик клавиатуры
def callback_worker(call):
    if call.data == "moscow": #call.data это callback_data, которую мы указали при объявлении кнопки
        f = open('files/moscow.txt', 'r')   # здесь лежит файл со станциями Москвы
        bot.send_message(call.message.chat.id, 'Установлен город: Москва')
        msg = bot.send_message(call.message.chat.id, 'Введите слово для поиска:')
    if call.data == "saintp":
        f = open('files/saintp.txt', 'r')   # здесь лежит файл со станциями Питера
        bot.send_message(call.message.chat.id, 'Установлен город: Санкт-Петербург')
        msg = bot.send_message(call.message.chat.id, 'Введите слово для поиска:')
    if call.data == "kazan":
        f = open('files/kazan.txt', 'r')   # здесь лежит файл со станциями Питера
        bot.send_message(call.message.chat.id, 'Установлен город: Казань')
        msg = bot.send_message(call.message.chat.id, 'Введите слово для поиска:')
    if call.data == "ekaterin":
        f = open('files/ekaterin.txt', 'r')   # здесь лежит файл со станциями Питера
        bot.send_message(call.message.chat.id, 'Установлен город: Екатеринбург')
        msg = bot.send_message(call.message.chat.id, 'Введите слово для поиска:')
    if call.data == "nizhniy":
        f = open('files/nizhniy.txt', 'r')   # здесь лежит файл со станциями Питера
        bot.send_message(call.message.chat.id, 'Установлен город: Нижний Новгород')
        msg = bot.send_message(call.message.chat.id, 'Введите слово для поиска:')
    if call.data == "volgograd":
        f = open('files/volgograd.txt', 'r')   # здесь лежит файл со станциями Питера
        bot.send_message(call.message.chat.id, 'Установлен город: Волгоград')
        msg = bot.send_message(call.message.chat.id, 'Введите слово для поиска:')
    if call.data == "novosibirsk":
        f = open('files/novosibirsk.txt', 'r')   # здесь лежит файл со станциями Питера
        bot.send_message(call.message.chat.id, 'Установлен город: Новосибирск')
        msg = bot.send_message(call.message.chat.id, 'Введите слово для поиска:')
    if call.data == "samara":
        f = open('files/samara.txt', 'r')   # здесь лежит файл со станциями Питера
        bot.send_message(call.message.chat.id, 'Установлен город: Самара')
        msg = bot.send_message(call.message.chat.id, 'Введите слово для поиска:')
city == str(call.data)
content = f.readlines()
bot.register_next_step_handler(msg, echo_message);
    
    
#if city == "Moscow":
#  print('Москва')
#  f = open('/content/drive/My Drive/Colab Notebooks/MetroPeople/list_msk.txt', 'r')   # здесь лежит файл со станциями:
#else:

@bot.message_handler(func=lambda message: True)

def start(message):
  if message.text == '/start':
      keyboard = types.InlineKeyboardMarkup(row_width=4); #наша клавиатура
      key_msk = types.InlineKeyboardButton(text='Москва', callback_data='moscow'); #кнопка "Москва"
      keyboard.add(key_msk); #добавляем кнопку в клавиатуру
      key_stp = types.InlineKeyboardButton(text='Санкт-Петербург', callback_data='saintp'); #кнопка "Санкт-Петербург"
      keyboard.add(key_stp); #добавляем кнопку в клавиатуру
      key_kzn = types.InlineKeyboardButton(text='Казань', callback_data='kazan'); #кнопка "Казань"
      keyboard.add(key_kzn); #добавляем кнопку в клавиатуру
      key_ekb = types.InlineKeyboardButton(text='Екатеринбург', callback_data='ekaterin'); #кнопка "Екатеринбург"
      keyboard.add(key_ekb); #добавляем кнопку в клавиатуру
      key_niz = types.InlineKeyboardButton(text='Нижний Новгород', callback_data='nizhniy'); #кнопка "Нижний Новгород"
      keyboard.add(key_niz); #добавляем кнопку в клавиатуру
      key_nsk = types.InlineKeyboardButton(text='Новосибирск', callback_data='novosibirsk'); #кнопка "Новосибирск"
      keyboard.add(key_nsk); #добавляем кнопку в клавиатуру
      key_vlg = types.InlineKeyboardButton(text='Волгоград', callback_data='volgograd'); #кнопка "Волгоград"
      keyboard.add(key_vlg); #добавляем кнопку в клавиатуру
      key_sam = types.InlineKeyboardButton(text='Самара', callback_data='samara'); #кнопка "Самара"
      keyboard.add(key_sam); #добавляем кнопку в клавиатуру
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