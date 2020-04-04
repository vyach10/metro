from telebot import types
import telebot
import re
import psycopg2
from datetime import datetime as dt
import json
from random import randint
#-------------------------------------------------------------
API_TOKEN = os.environ['TOKEN']
bot = telebot.TeleBot(API_TOKEN)
#-------------------------------------------------------------
DB = os.environ['DATABASE_URL']
connect = psycopg2.connect(DB)
#-------------------------------------------------------------
path = 'files/metronames.json'
f=open(path, 'r')
data = []
with open(path) as f:
    for line in f:
        data.append(json.loads(line))
#-------------------------------------------------------------
place=''
c=''
temp=''

@bot.message_handler(commands=['start'])          # команда /start
def start(message):
    kb_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_a = types.KeyboardButton('/start')
    btn_pic = types.KeyboardButton('Показать пример')
    kb_start.add(btn_a,btn_pic)
#------------------------------------------------------------
    bot.send_message(message.from_user.id, text='Предлагаем вызглянуть на метро под другим углом', reply_markup=kb_start)
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
#------------------------------------------------------------   

def change_city(place, newplace, c, city, message):
    global temp
    temp = message
    #bot.send_message(chat_id, ans)
    markup = types.InlineKeyboardMarkup(row_width=3);
    key_yes = types.InlineKeyboardButton(text='Да', callback_data=newplace);
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no');
    markup.add(key_yes, key_no);  # добавляем кнопки Да и Нет в клавиатуру
    message = bot.send_message(message.from_user.id, text='В городе '+c+' запрос не найден, но найден в городе '+city+'. Сменить город?', reply_markup=markup)

def poisk(word, message):
    ans = ''
    shablon = ''
    for i in range(0, len(word)):
        shablon += word[i] + '.*'
    for j in data:
      if j['place'] == place:
        mat = re.search(shablon, j['name'], re.I)
        if mat:
          ans += '\n' + j['name'][0:len(j['name']) - 1]
    if ans == '':
      for j in data:
        mat = re.search(shablon, j['name'], re.I)
        if mat:
          ans += '\n' + j['name'][0:len(j['name']) - 1]
          newplace = j['place']
          city = j['city']
      if ans != '':
        change_city(place, newplace, c, city, message)
        ans = 'False'
    if ans == '':
      ans = 'Запрос не содержится ни в одной из станций'
    return(ans)          

@bot.message_handler(func=lambda message: True)      
def city(message):
    if str(message.text) == 'Показать пример':
      dig=str(randint(1,8))
      photo = open('pic/'+dig+'.JPG', 'rb')
      bot.send_photo(message.from_user.id, photo)
    elif str(message.text).isalpha() and len(str(message.text))<16:
      ans=poisk(str(message.text), message)
      if ans == 'False':
        return();
  #  ===================АНАЛИТИКА===================#   
      else:
        id = message.chat.id
        cursor = connect.cursor()
        connect.cursor()
        cursor.execute('INSERT INTO LOG (id, time, city, message) VALUES (%s, %s, %s, %s)', (id, dt.now(), place, str(message.text)))
        connect.commit() # <- We MUST commit to reflect the inserted data
        cursor.close()
  #  ===================АНАЛИТИКА===================#  
        bot.reply_to(message, ans)
    else:
      bot.reply_to(message, 'Запрос должен содержать текст и быть короче 15 символов')
      bot.send_message(message.chat.id, 'Введите запрос для поиска:')

@bot.callback_query_handler(func=lambda call: True)  # обработчик клавиатуры
def callback_worker(call):
  if call == 'no':
    msg1 = bot.send_message(call.message.chat.id, 'Введите запрос для поиска:')
  else:    
    global place, c
    place = call.data
    for k in data:
      if k['place'] == place:
        c = k['city']
    bot.send_message(call.message.chat.id, 'Установлен город: '+c+'\nЧтобы выбрать другой город, отправьте /start')
    msg1 = bot.send_message(call.message.chat.id, 'Введите запрос для поиска:')

def callback_worker(call, ):
  if call == 'yes':
    msg1 = bot.send_message(call.message.chat.id, 'Введите запрос для поиска:')
  else:    
    global place, c
    place = call.data
    for k in data:
      if k['place'] == place:
        c = k['city']
    bot.send_message(call.message.chat.id, 'Установлен город: '+c+'\nЧтобы выбрать другой город, отправьте /start')
    msg1 = bot.send_message(call.message.chat.id, 'Введите запрос для поиска:')

bot.polling()