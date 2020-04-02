from telebot import types
import telebot
import re

API_TOKEN = '853778348:AAFSMMu5Lvz9_Jg1j9P7L-efBu3ay1RzPKs'
bot = telebot.TeleBot(API_TOKEN)

place=''

@bot.message_handler(commands=['start'])          # команда /start
def start(message):
    keyboard = types.InlineKeyboardMarkup(row_width=3);
    key_msk = types.InlineKeyboardButton(text='Москва', callback_data='moscow');
    key_stp = types.InlineKeyboardButton(text='Санкт-Петербург', callback_data='saintp');
    key_kzn = types.InlineKeyboardButton(text='Казань', callback_data='kazan');
    key_ekb = types.InlineKeyboardButton(text='Екатеринбург', callback_data='ekaterin');
    key_niz = types.InlineKeyboardButton(text='Нижний Новгород', callback_data='nizhniy');
    key_nsk = types.InlineKeyboardButton(text='Новосибирск', callback_data='novosibirsk');
    key_vlg = types.InlineKeyboardButton(text='Волгоград', callback_data='volgograd');
    key_sam = types.InlineKeyboardButton(text='Самара', callback_data='samara');
    keyboard.add(key_msk);  # добавляем кнопку Москвы в клавиатуру
    keyboard.add(key_stp);  # добавляем кнопку Питера в клавиатуру
    keyboard.add(key_nsk, key_ekb, key_niz);  # добавляем кнопки в клавиатуру
    keyboard.add(key_kzn, key_sam, key_vlg);  # добавляем кнопку в клавиатуру
    bot.send_message(message.from_user.id, text='Выберите город:', reply_markup=keyboard)

def poisk(dicti, word):
    ans = ''
    shablon = ''
    for i in range(0, len(word)):
        shablon += word[i] + '.*'
    for i in range(0, len(dicti)):
        mat = re.search(shablon, dicti[i], re.I)
        if mat:
            ans += '\n' + dicti[i][0:len(dicti[i]) - 1]
    if ans == '':
        ans = 'Запрос не содержится ни в одной из станций'
    return(ans)

@bot.message_handler(func=lambda message: True)      
def city(message):
    if len(str(message.text))>1:
      f = open('files/'+place+'.txt', 'r')   # здесь лежит файл со станциями:
      content = f.readlines()
      req = str(message.text)
      ans=poisk(content,req)
      print(ans)
      bot.reply_to(message, ans)
    else:
      bot.reply_to(message, 'Запрос должен быть длиннее, чем 1 символ')
      bot.send_message(message.chat.id, 'Введите запрос для поиска:')

@bot.callback_query_handler(func=lambda call: True)  # обработчик клавиатуры
def callback_worker(call):
    global place
    if call.data=='moscow':
      bot.send_message(call.message.chat.id, 'Установлен город: Москва\nЧтобы сменить город, отправьте /start')
    if call.data=='saintp':
      bot.send_message(call.message.chat.id, 'Установлен город: Санкт-Петербург\nЧтобы сменить город, отправьте /start')
    if call.data=='novosibirsk':
      bot.send_message(call.message.chat.id, 'Установлен город: Новосибирск\nЧтобы сменить город, отправьте /start')
    if call.data=='ekaterinburg':
      bot.send_message(call.message.chat.id, 'Установлен город: Екатеринбург\nЧтобы сменить город, отправьте /start')
    if call.data=='nizhniy':
      bot.send_message(call.message.chat.id, 'Установлен город: Нижний Новгород\nЧтобы сменить город, отправьте /start')
    if call.data=='kazan':
      bot.send_message(call.message.chat.id, 'Установлен город: Казань\nЧтобы сменить город, отправьте /start')
    if call.data=='samara':
      bot.send_message(call.message.chat.id, 'Установлен город: Самара\nЧтобы сменить город, отправьте /start')
    if call.data=='volgograd':
      bot.send_message(call.message.chat.id, 'Установлен город: Волгоград\nЧтобы сменить город, отправьте /start')
    msg1 = bot.send_message(call.message.chat.id, 'Введите запрос для поиска:')
    place = call.data

bot.polling()