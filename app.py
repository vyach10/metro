from telebot import types
import telebot
import re
import psycopg2
from datetime import datetime as dt
import json
from random import randint
import random
import os
import ast
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
@bot.message_handler(commands=['start', 'Сменить город'])          # команда /start
def start(message):
    kb_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_a = types.KeyboardButton('Сменить город')
    btn_pic = types.KeyboardButton('Показать пример')
#   btn_lnk   # ссылка на меня в инстике    
    kb_start.add(btn_a,btn_pic)
#------------------------------------------------------------
    keyboard = types.InlineKeyboardMarkup(row_width=3);
    key_msk = types.InlineKeyboardButton(text='Москва', callback_data='msk');
    key_stp = types.InlineKeyboardButton(text='Санкт-Петербург', callback_data='stp');
    key_kzn = types.InlineKeyboardButton(text='Казань', callback_data='kzn');
    key_ekb = types.InlineKeyboardButton(text='Екатеринбург', callback_data='ekb');
    key_niz = types.InlineKeyboardButton(text='Н. Новгород', callback_data='niz');
    key_nsk = types.InlineKeyboardButton(text='Новосибирск', callback_data='nsk');
    key_vlg = types.InlineKeyboardButton(text='Волгоград', callback_data='vlg');
    key_sam = types.InlineKeyboardButton(text='Самара', callback_data='sam');
    keyboard.add(key_msk, key_stp);  # добавляем кнопку Москвы в клавиатуру
    keyboard.add(key_nsk, key_ekb, key_niz);  # добавляем кнопки в клавиатуру
    keyboard.add(key_kzn, key_sam, key_vlg);  # добавляем кнопку в клавиатуру
    if random.uniform(0,1)<0.1:
      key_inst = types.InlineKeyboardButton(text='Автор в Instagram', url='https://instagram.com/vy4c/')
      keyboard.add(key_inst)
    if random.uniform(0,1)<0.2:
      bot.send_message(message.from_user.id, text='Хеш-тег #ИменаМетро', reply_markup=kb_start)
    bot.send_message(message.from_user.id, text='Выберите город:', reply_markup=keyboard)
#------------------------------------------------------------   

def poisk(word, message):
    t = message
    print(message)

    id = message.chat.id
    cursor = connect.cursor()
    connect.cursor()
    b=cursor.execute("select city from city_db where id=%s", (id,))
    records = cursor.fetchone()
    cursor.close()
    place=records[0]
    print(place)
    
    #----------------------------------
    for k in data:
      if k['place'] == place:
        c = k['city']
    #----------------------------------
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
        markup = types.InlineKeyboardMarkup(row_width=3);
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='1'+newplace);
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no');
        markup.add(key_yes, key_no);  # добавляем кнопки Да и Нет в клавиатуру
        message = bot.send_message(message.from_user.id, text='В городе '+c+' запрос не найден, но найден в городе '+city+'. Сменить город?', reply_markup=markup)
        message = t
        ans = 'False'
    if ans == '':
      ans = 'Запрос не содержится ни в одной из станций'
    return(ans)          

@bot.message_handler(func=lambda message: True)      
def city(message):
    id = message.chat.id
    cursor = connect.cursor()
    connect.cursor()
    b=cursor.execute("select city from city_db where id=%s", (id,))
    records = cursor.fetchone()
    cursor.close()
    place=records[0]
    
    #---------------- ЗАПИСЫВАЕМ СООБЩЕНИЕ ------------------
    mes = json.dumps(str(message))
    cursor = connect.cursor()
    connect.cursor()
    cursor.execute("select message from message where id=%s", (id,))
    records = cursor.fetchone()
    print('"',id,'","',records,'"')
    if (records=='[]') or (records==' [] ') or records is None:
      cursor.execute('INSERT INTO message (id, message) VALUES (%s, %s)', (id, mes))
      connect.commit() # <- We MUST commit to reflect the inserted data
    else:
      cursor.execute('UPDATE message SET message = %s WHERE id = %s', (mes, id))
      connect.commit() # <- We MUST commit to reflect the inserted data
    cursor.close()
    #----------------  ЗАПИСАЛИ СООБЩЕНИЕ  ------------------
    
    print(place)
    if str(message.text) == 'Сменить город':
      start(message)
    elif str(message.text) == 'Показать пример':
      dig=str(randint(1,8))
      photo = open('pic/'+dig+'.JPG', 'rb')
      bot.send_photo(message.from_user.id, photo)
    elif str(message.text).isalpha() and len(str(message.text))<16:
      ans=poisk(str(message.text), message)
      if ans == 'False':
        return();
    #--------------------  АНАЛИТИКА  -----------------------   
      else:
        id = message.chat.id
        name = message.chat.username
        cursor = connect.cursor()
        connect.cursor()
        cursor.execute('INSERT INTO LOG (id, time, city, message) VALUES (%s, %s, %s, %s)', (id, dt.now(), place, str(message.text)))
        connect.commit() # <- We MUST commit to reflect the inserted data
        cursor.close()
    #--------------------  АНАЛИТИКА  ----------------------- 
        bot.reply_to(message, ans)
    else:
      bot.reply_to(message, 'Запрос должен содержать текст и быть короче 15 символов')
      bot.send_message(message.chat.id, 'Введите запрос для поиска:')

@bot.callback_query_handler(func=lambda call: True)  # обработчик клавиатуры
def callback_worker(call):

  if call.data[0] == '1':
    id = call.message.chat.id
    #---------------- ЧИТАЕМ СООБЩЕНИЕ ------------------
    cursor = connect.cursor()
    connect.cursor()
    b = cursor.execute("select message from message where id=%s", (id,))
    records = cursor.fetchone()
    cursor.close()
    #---------------- ПРОЧИТАЛИ СООБЩЕНИЕ ------------------
    place = call.data[1:]
    print(place)
    for k in data:
      if k['place'] == place:
        c = k['city']
    change_city(call.message.chat.id, place)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Установлен город: '+c)
    mes = records[0]
    print(mes)
    mes = mes.replace("\'", "\"")
    mes = json.loads(mes)
    #mes = json.dumps(mes)
    city(mes)

  elif call.data == 'no':
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Введите запрос для поиска:');
  
  else:    
    place = call.data
    for k in data:
      if k['place'] == place:
        c = k['city']
    change_city(call.message.chat.id, place)  # меняем город в БД
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Установлен город: '+c+'\nВведите запрос для поиска:')

def change_city(id, new_city):
  cursor = connect.cursor()
  connect.cursor()
  a=cursor.execute("select city from city_db where id=%s", (id,))
  records = cursor.fetchone()
  print('"',id,'","',records,'"')
  if (records=='[]') or (records==' [] ') or records is None:
    cursor.execute('INSERT INTO CITY_DB (id, city) VALUES (%s, %s)', (id, new_city))
    connect.commit()
  else:
    cursor.execute('UPDATE city_db SET city = %s WHERE id = %s', (new_city, id))
    connect.commit()
  #connect.commit()
  cursor.close()

bot.polling()