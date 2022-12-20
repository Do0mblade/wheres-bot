# -*- coding: utf-8 -*-


# Импорты

from aiogram import Bot, Dispatcher, executor, types
import time
import random
import sqlite3
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import InputFile
from aiogram.utils.markdown import hlink

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from attributes.config import *
from attributes.connection import *
from attributes.keyboard import *
#from attributes.moduls import *
from attributes.text import *

# Инициализация бота

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


class UserState(StatesGroup):
   gen = State()
   age = State()



# Команды

@dp.message_handler(commands=['set_own_admin'])
async def send_welcome(message: types.Message):
   admin = 619402571
   cur.execute(f"UPDATE users SET admin_mode = 'admin' WHERE user_id = {admin}")
   print()
   print(cur.execute(f"SELECT * FROM users WHERE user_id = {admin}").fetchone())
   print('Владельцу выданы права администратора!')
   print()

@dp.message_handler(commands=['kalibr'])
async def send_welcome(message: types.Message):
   user_id = message.from_user.id

   check = cur.execute(f"""SELECT admin_mode FROM users WHERE user_id = {user_id}""").fetchone()

   if check[0] == 'admin':
      cur.execute("ALTER TABLE users ADD COLUMN referal TEXT")
      conn.commit()
      print('Админ произвёл калибровку!')
   else:
      print('Не админ!')

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
   user_id = message.from_user.id

   check = cur.execute(f"""SELECT * FROM users WHERE user_id = {user_id}""").fetchone()

   if check:
      await message.answer('🗃 Главное меню', reply_markup=MainMenuBtns)
   else:
      await message.reply(f'✋ Привет, <b>{message.from_user.full_name}</b>', parse_mode='HTML', reply_markup=ReplyKeyboardRemove())
      time.sleep(0.7)
      await message.answer(f'''
   Я могу помочь тебе в подборе мест для отдыха.
   
   Если ты не против, пожалуйста, зарегистрируйся, чтобы я мог лучше подбирать тебе места.
   
   ''', reply_markup=register_btns)

@dp.message_handler(lambda message: message.text == "🚫 Нет, спасибо")
async def register_no(message: types.Message):
   await message.reply('❌ Отказано')
   time.sleep(0.7)
   await message.answer(f'❗ Нельзя пойти против системы, {message.from_user.first_name}', reply_markup=register_btns)

@dp.message_handler(lambda message: message.text == "📑 Да, зарегистрируй меня.")
async def register_yes(message: types.Message):
   user_id = message.from_user.id

   check = cur.execute(f"""SELECT * FROM users WHERE user_id = {user_id}""").fetchone()

   if check:
      await message.reply("❗ Вы уже зарегистрированы!", reply_markup=MainMenuBtns)
   else:
      await message.answer("Пожалуйста введите свой пол.", reply_markup=GenderMenus)
      await UserState.next()

@dp.message_handler(state=UserState.gen)
async def get_gender(message: types.Message, state: FSMContext):
   if message.text == 'мужской' or message.text == 'женский' or message.text == 'м' or message.text == 'ж' or message.text == 'Мужской' or message.text == 'Женский' or message.text == 'М' or message.text == 'Ж' or message.text == '👨 Мужской' or message.text == '👩 Женский':
      await state.update_data(gen=message.text)
      await message.answer("Отлично! Теперь введите ваш возраст.", reply_markup=ReplyKeyboardRemove())
      await UserState.next()
   else:
      await message.answer("Вы не правильно указали пол!\nПопробуйте снова.\n\nМужской/Женский")

@dp.message_handler(state=UserState.age)
async def get_age(message: types.Message, state: FSMContext):
   try:
      val = int(message.text)
      if int(message.text) > 5:
         if int(message.text) < 130:
            await state.update_data(age=message.text)
            data = await state.get_data()

            first_name = message.from_user.first_name
            user_id = message.from_user.id

            if data['gen'] == 'мужской' or data['gen'] == 'м' or data['gen'] == 'Мужской' or data['gen'] == 'М' or data['gen'] == '👨 Мужской':
               gender = 'Мужской'
            if data['gen'] == 'женский' or data['gen'] == 'ж' or data['gen'] == 'Женский' or data['gen'] == 'Ж' or data['gen'] == '👩 Женский':
               gender = 'Женский'

            cur.execute(f"""INSERT INTO users (first_name, user_id, age, gender) VALUES ('{first_name}', {user_id}, {data['age']}, '{gender}')""")
            conn.commit()

            await message.reply("✅ Вы успешно зарегистрированы!", reply_markup=MainMenuBtns)
            time.sleep(0.7)
            await message.answer("⚡ Хотите следить за актуальными новостями?", reply_markup=inline_kb_channel)

            if user_id == 619402571:
               msg = await message.answer("🖕 Не души сука!")
               time.sleep(0.8)
               await msg.delete()

            print(cur.execute(f'SELECT * FROM users WHERE user_id = {user_id}').fetchall())

            await state.finish()
         else:
            await message.answer("Введите корректный возраст)")
      else:
         await message.answer("Пользоваться ботом можно только с 6 лет!")
   except ValueError:
      await message.answer("Вы ввели неверные данные!\n")



@dp.message_handler(lambda message: message.text == "📋 Профиль")
async def profile(message: types.Message):

   user_id = message.from_user.id

   check = cur.execute(f"""SELECT * FROM users WHERE user_id = {user_id}""").fetchone()

   if check:

      us = cur.execute(f'SELECT * FROM users WHERE user_id = {message.from_user.id}').fetchall()

      for user in us:
         pass

      if int(user[3]) > 5 and int(user[3]) < 11:
         smile_age = '👶'

      if user[4] == 'Мужской':
         smile_gender = '👨'
         if int(user[3]) > 10 and int(user[3]) < 17:
            smile_age = '👦'
         if int(user[3]) > 16 and int(user[3]) < 60:
            smile_age = '👨'
         if int(user[3]) > 59:
            smile_age = '🧓'
      if user[4] == 'Женский':
         smile_gender = '👩'
         if int(user[3]) > 10 and int(user[3]) < 17:
            smile_age = '👧'
         if int(user[3]) > 16 and int(user[3]) < 60:
            smile_age = '👩'
         if int(user[3]) > 59:
            smile_age = '👵'

      me = await bot.get_me()

      await message.answer(f'''

      🥷 Ваш ассистент `<b> {me.first_name} </b>` 

      👽 <i>Nickname</i>: {user[1]}

      {smile_age} <i>Возраст</i>: {user[3]}

      {smile_gender} <i>Пол</i>: {user[4]}

      💰 <i>Ваши баллы</i>: {user[5]}


      ''', parse_mode='HTML', reply_markup=inline_kb_channel)

   else:
      await message.reply("❗ Пожалуйста зарегистрируйтесь!\n\nВведите <b>/start</b>", parse_mode='HTML')
      await message.answer(
         "На данный момент бот находится в разработке, поэтому возможен сброс базы зарегистрированных пользователей.\n\nПриносим извинения за неудобство.")


@dp.message_handler(lambda message: message.text == "❤ Избранное")
async def admin_menu(message: types.Message):
   data = cur.execute(f"""SELECT * FROM likes WHERE user_id = {message.from_user.id}""").fetchall()
   if len(data) == 0:
      await message.answer(f'<b>{message.from_user.full_name}</b>, вы пока не добавили ни одно место в избранное.', parse_mode='HTML')
   else:
      await message.answer(f'<b>{message.from_user.full_name}</b>, вот все места, которые вам понравились.', parse_mode='HTML')
      for i in data:
         Dislike_menu_btn = InlineKeyboardButton('💔 Dislike', callback_data=f'delete_like_place {i[2]}')
         Dislike_menu_btns = InlineKeyboardMarkup(row_width=2)
         Dislike_menu_btns.add(Dislike_menu_btn)
         dt = cur.execute(f"""SELECT * FROM places WHERE id = {i[2]}""").fetchone()
         if len(dt[3]) > 100:
            text = f'{dt[3][0:100]}...'
         else:
            text = f'{dt[3]}'
         await message.answer(f"""<b>{dt[1]}</b>\n\n{text}""", parse_mode='HTML', reply_markup=Dislike_menu_btns)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('delete_like_place '))
async def Delete_likes_places(callback_query: types.CallbackQuery):
   id = callback_query.data.replace('delete_like_place ', '')
   cur.execute(f"""DELETE FROM likes WHERE user_id = {callback_query.from_user.id} and post_id = {id}""")
   conn.commit()
   await callback_query.message.delete()

@dp.message_handler(lambda message: message.text == "🎁 Бонусы")
async def bonus(message: types.Message):
   user_id = message.from_user.id

   check = cur.execute(f"""SELECT * FROM users WHERE user_id = {user_id}""").fetchone()

   if check:
      check1 = cur.execute(f'SELECT bonus FROM users WHERE user_id = {message.from_user.id}').fetchone()
      if check1[0] == 0:
         score = cur.execute(f'SELECT scores FROM users WHERE user_id = {message.from_user.id}').fetchone()
         cur.execute(f'UPDATE users SET scores = {score[0] + 100} WHERE user_id = {message.from_user.id}')
         cur.execute(f'UPDATE users SET bonus = True WHERE user_id = {message.from_user.id}')
         conn.commit()
         await message.answer('Поздравляю! Вы получили <b>100</b> 💰 баллов на свой баланс!', parse_mode='HTML')
      else:
         if check[8] is None:
            ch = 0
            while ch == 0:
               chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
               promo = ''
               for i in range(10):
                  promo += random.choice(chars)
               if cur.execute(f"""SELECT id FROM users WHERE referal = '{promo}'""") is None:
                  print('Такой промокод уже есть!')
               else:
                  cur.execute(f"""UPDATE users SET referal = '{promo}' WHERE user_id = {message.from_user.id}""")
                  conn.commit()
                  ch = 1
         await message.answer('Простите, но вы уже получали бонус(')
         time.sleep(0.4)
         await message.answer('Если хотите больше бонусов, подключите реферальную систему! <b>[В разработке]</b>', parse_mode='HTML')
   else:
      await message.reply("❗ Пожалуйста зарегистрируйтесь!\n\nВведите <b>/start</b>", parse_mode='HTML')
      await message.answer(
         "На данный момент бот находится в разработке, поэтому возможен сброс базы зарегистрированных пользователей.\n\nПриносим извинения за неудобство.")

@dp.message_handler(lambda message: message.text == "💳 Поддержать")
async def donate(message: types.Message):
   await message.answer("Поддержите проект копейкой)", reply_markup=Donate_money)

@dp.message_handler(lambda message: message.text == "ℹ Инфо")
async def info(message: types.Message):
   user_id = message.from_user.id

   check = cur.execute(f"""SELECT * FROM users WHERE user_id = {user_id}""").fetchone()

   if check:
      await message.answer(development_text.format(VERSION_BOT), reply_markup=inline_kb_channel)
   else:
      await message.reply("❗ Пожалуйста зарегистрируйтесь!\n\nВведите <b>/start</b>", parse_mode='HTML')
      await message.answer(
         "На данный момент бот находится в разработке, поэтому возможен сброс базы зарегистрированных пользователей.\n\nПриносим извинения за неудобство.")




@dp.message_handler(lambda message: message.text == "⚙ Настройки")
async def settings(message: types.Message):
   user_id = message.from_user.id

   check = cur.execute(f"""SELECT * FROM users WHERE user_id = {user_id}""").fetchone()

   if check:
      await message.answer(development_text.format(VERSION_BOT), reply_markup=inline_kb_channel)
   else:
      await message.reply("❗ Пожалуйста зарегистрируйтесь!\n\nВведите <b>/start</b>", parse_mode='HTML')
      await message.answer(
         "На данный момент бот находится в разработке, поэтому возможен сброс базы зарегистрированных пользователей.\n\nПриносим извинения за неудобство.")

@dp.message_handler(lambda message: message.text == "🔎 Поиск")
async def poisk(message: types.Message):

   user_id = message.from_user.id

   check = cur.execute(f"""SELECT * FROM users WHERE user_id = {user_id}""").fetchone()

   if check:
      await message.answer(f'''<b>Настроить ваш поиск?</b>''', parse_mode='HTML', reply_markup=SettingsSearchBox)
   else:
      await message.reply("❗ Пожалуйста зарегистрируйтесь!\n\nВведите <b>/start</b>", parse_mode='HTML')
      await message.answer("На данный момент бот находится в разработке, поэтому возможен сброс базы зарегистрированных пользователей.\n\nПриносим извинения за неудобство.")


@dp.callback_query_handler(lambda c: c.data == 'Search_no_filters')
async def Search_no_filters(callback_query: types.CallbackQuery):

   data = cur.execute(f"""SELECT * FROM places ORDER BY RANDOM() LIMIT 1""").fetchone()

   if data is None:
      await callback_query.message.answer('Пока мы ничего не выложили в бота.\n\nПока мы выкладываем информацию, можете зайти к нам в канал и посмотреть многое там.', reply_markup=inline_kb_channel)
   else:

      user_id = callback_query.message.from_user.id

      check = cur.execute(f"""SELECT * FROM checked WHERE user_id = {user_id}""").fetchall()

      if len(check) > 5:
         cur.execute(f"""DELETE FROM checked WHERE user_id = {user_id}""")
         conn.commit()
         data = cur.execute(f"""SELECT * FROM places ORDER BY RANDOM() LIMIT 1""").fetchone()
      else:
         if len(check) == 1:
            data = cur.execute(f"""SELECT * FROM places WHERE id != {check[0][2]} ORDER BY RANDOM() LIMIT 1""").fetchone()
            if data is None:
               cur.execute(f"""DELETE FROM checked WHERE user_id = {user_id}""")
               conn.commit()
               await callback_query.message.answer('✨ На данный момент вы посмотрели все интересные места.\n💫 Теперь посты будут повторяться до добавления новых.')
               time.sleep(1.5)
               data = cur.execute(f"""SELECT * FROM places ORDER BY RANDOM() LIMIT 1""").fetchone()
         if len(check) == 2:
            data = cur.execute(f"""SELECT * FROM places WHERE id != {check[0][2]} and id != {check[1][2]} ORDER BY RANDOM() LIMIT 1""").fetchone()
            if data is None:
               cur.execute(f"""DELETE FROM checked WHERE user_id = {user_id}""")
               conn.commit()
               await callback_query.message.answer('✨ На данный момент вы посмотрели все интересные места.\n💫 Теперь посты будут повторяться до добавления новых.')
               time.sleep(1.5)
               data = cur.execute(f"""SELECT * FROM places ORDER BY RANDOM() LIMIT 1""").fetchone()
         if len(check) == 3:
            data = cur.execute(f"""SELECT * FROM places WHERE id != {check[0][2]} and id != {check[1][2]} and id != {check[2][2]} ORDER BY RANDOM() LIMIT 1""").fetchone()
            if data is None:
               cur.execute(f"""DELETE FROM checked WHERE user_id = {user_id}""")
               conn.commit()
               await callback_query.message.answer('✨ На данный момент вы посмотрели все интересные места.\n💫 Теперь посты будут повторяться до добавления новых.')
               time.sleep(1.5)
               data = cur.execute(f"""SELECT * FROM places ORDER BY RANDOM() LIMIT 1""").fetchone()
         if len(check) == 4:
            data = cur.execute(f"""SELECT * FROM places WHERE id != {check[0][2]} and id != {check[1][2]} and id != {check[2][2]} and id != {check[3][2]} ORDER BY RANDOM() LIMIT 1""").fetchone()
            if data is None:
               cur.execute(f"""DELETE FROM checked WHERE user_id = {user_id}""")
               conn.commit()
               await callback_query.message.answer('✨ На данный момент вы посмотрели все интересные места.\n💫 Теперь посты будут повторяться до добавления новых.')
               time.sleep(1.5)
               data = cur.execute(f"""SELECT * FROM places ORDER BY RANDOM() LIMIT 1""").fetchone()
         if len(check) == 5:
            data = cur.execute(f"""SELECT * FROM places WHERE id != {check[0][2]} and id != {check[1][2]} and id != {check[2][2]} and id != {check[3][2]} and id != {check[4][2]} ORDER BY RANDOM() LIMIT 1""").fetchone()
            if data is None:
               cur.execute(f"""DELETE FROM checked WHERE user_id = {user_id}""")
               conn.commit()
               await callback_query.message.answer('✨ На данный момент вы посмотрели все интересные места.\n💫 Теперь посты будут повторяться до добавления новых.')
               time.sleep(1.5)
               data = cur.execute(f"""SELECT * FROM places ORDER BY RANDOM() LIMIT 1""").fetchone()
         if len(check) == 0:
            cur.execute(f"""DELETE FROM checked WHERE user_id = {user_id}""")
            conn.commit()
            data = cur.execute(f"""SELECT * FROM places ORDER BY RANDOM() LIMIT 1""").fetchone()
            if data is None:
               cur.execute(f"""DELETE FROM checked WHERE user_id = {user_id}""")
               conn.commit()
               await callback_query.message.answer('✨ На данный момент вы посмотрели все интересные места.\n💫 Теперь посты будут повторяться до добавления новых.')
               time.sleep(1.5)
               data = cur.execute(f"""SELECT * FROM places ORDER BY RANDOM() LIMIT 1""").fetchone()


      cur.execute(f"""INSERT INTO checked (user_id, post_id) VALUES ({user_id}, {data[0]})""")
      conn.commit()

      TextMenuBTNS = InlineKeyboardMarkup(row_width=3)
      send = []

      if data[7] == 'нет':
         pass
      else:
         TextMenuBtns2 = InlineKeyboardButton('🌐 Открыть сайт', url=f'{data[7]}')

      dd = cur.execute(
         f"""SELECT * FROM likes WHERE post_id = {data[0]} and user_id = {callback_query.from_user.id}""").fetchone()

      if dd != None:
         TextMenuBtns3 = InlineKeyboardButton('💔 Dislike', callback_data=f'del_from_favorite {data[0]}')
      else:
         TextMenuBtns3 = InlineKeyboardButton('❤ Like', callback_data=f'add_to_favorite {data[0]}')
      if data[8] == 'нет':
         pass
      else:
         TextMenuBtns4 = InlineKeyboardButton('🗾 Найти на картах', url=f'{data[8]}')
      TextMenuBtns5 = InlineKeyboardButton('➡ Следующий пост', callback_data='Search_no_filters')
      send.extend((TextMenuBtns2, TextMenuBtns3, TextMenuBtns4, TextMenuBtns5))
      TextMenuBTNS.add(*send)

      caption = f"""
      
   {data[1]}
      
   {data[3]}   
         
         """

      await bot.send_photo(chat_id=callback_query.message.chat.id, photo=f'{data[2]}', caption=caption, parse_mode='HTML',
                                 reply_markup=TextMenuBTNS)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('add_to_favorite '))
async def add_to_favorite(callback_query: types.CallbackQuery):
   id = callback_query.data.replace('add_to_favorite ', '')
   cur.execute(f"""INSERT INTO likes (user_id, post_id) VALUES ({callback_query.from_user.id}, {id})""")
   conn.commit()
   data = cur.execute(f"""SELECT * FROM places WHERE id = {id}""").fetchone()

   TextMenuBTNS = InlineKeyboardMarkup(resize_keyboard=True)

   if data[7] == 'нет':
      pass
   else:
      TextMenuBtns2 = InlineKeyboardButton('🌐 Открыть сайт', url=f'{data[7]}')
      TextMenuBTNS.add(TextMenuBtns2)

   dd = cur.execute(
      f"""SELECT * FROM likes WHERE post_id = {data[0]} and user_id = {callback_query.from_user.id}""").fetchone()

   if dd != None:
      TextMenuBtns3 = InlineKeyboardButton('💔 Dislike', callback_data=f'del_from_favorite {data[0]}')
      TextMenuBTNS.add(TextMenuBtns3)
   else:
      TextMenuBtns3 = InlineKeyboardButton('❤ Like', callback_data=f'add_to_favorite {data[0]}')
      TextMenuBTNS.add(TextMenuBtns3)
   if data[8] == 'нет':
      pass
   else:
      TextMenuBtns4 = InlineKeyboardButton('🗾 Найти на картах', url=f'{data[8]}')
      TextMenuBTNS.add(TextMenuBtns4)
   TextMenuBtns5 = InlineKeyboardButton('➡ Следующий пост', callback_data='Search_no_filters')
   TextMenuBTNS.add(TextMenuBtns5)
   await callback_query.message.edit_reply_markup(TextMenuBTNS)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('del_from_favorite '))
async def add_to_favorite(callback_query: types.CallbackQuery):
   id = callback_query.data.replace('del_from_favorite ', '')
   cur.execute(f"""DELETE FROM likes WHERE user_id = {callback_query.from_user.id} and post_id = {id}""")
   conn.commit()
   data = cur.execute(f"""SELECT * FROM places WHERE id = {id}""").fetchone()
   TextMenuBTNS = InlineKeyboardMarkup(resize_keyboard=True)

   if data[7] == 'нет':
      pass
   else:
      TextMenuBtns2 = InlineKeyboardButton('🌐 Открыть сайт', url=f'{data[7]}')
      TextMenuBTNS.add(TextMenuBtns2)

   dd = cur.execute(
      f"""SELECT * FROM likes WHERE post_id = {data[0]} and user_id = {callback_query.from_user.id}""").fetchone()

   if dd != None:
      TextMenuBtns3 = InlineKeyboardButton('💔 Dislike', callback_data=f'del_from_favorite {data[0]}')
      TextMenuBTNS.add(TextMenuBtns3)
   else:
      TextMenuBtns3 = InlineKeyboardButton('❤ Like', callback_data=f'add_to_favorite {data[0]}')
      TextMenuBTNS.add(TextMenuBtns3)
   if data[8] == 'нет':
      pass
   else:
      TextMenuBtns4 = InlineKeyboardButton('🗾 Найти на картах', url=f'{data[8]}')
      TextMenuBTNS.add(TextMenuBtns4)
   TextMenuBtns5 = InlineKeyboardButton('➡ Следующий пост', callback_data='Search_no_filters')
   TextMenuBTNS.add(TextMenuBtns5)
   await callback_query.message.edit_reply_markup(TextMenuBTNS)


@dp.callback_query_handler(lambda c: c.data == 'Search_yes_filters')
async def Search_yes_filters(callback_query: types.CallbackQuery):
   data = cur.execute("""SELECT * FROM categoryes""").fetchall()
   CATEGORYES_BTNS = InlineKeyboardMarkup(row_width=3)
   send = []
   for i in data:
      CATEGORYES_btns = InlineKeyboardButton(f'{i[1]}', callback_data=f'serch_cat {i[0]}')
      send.append(CATEGORYES_btns)
   CATEGORYES_BTNS.add(*send)
   await callback_query.message.answer('Выберайте что вам интересно!', reply_markup=CATEGORYES_BTNS)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('serch_cat '))
async def Search_with_category(callback_query: types.CallbackQuery):
   cat_id = callback_query.data.replace('serch_cat ', '')
   data = cur.execute(f"""SELECT * FROM places WHERE category_id = {cat_id} ORDER BY RANDOM() LIMIT 1""").fetchone()

   if data is None:
      await callback_query.message.answer(
         'Пока мы ничего не выложили в эту категорию.\n\nПока мы выкладываем информацию, можете зайти к нам в канал и посмотреть многое там.',
         reply_markup=inline_kb_channel)
   else:

      user_id = callback_query.message.from_user.id

      check = cur.execute(f"""SELECT * FROM checked WHERE user_id = {user_id}""").fetchall()

      if len(check) > 5:
         cur.execute(f"""DELETE FROM checked WHERE user_id = {user_id}""")
         conn.commit()
         data = cur.execute(f"""SELECT * FROM places WHERE category_id = {cat_id} ORDER BY RANDOM() LIMIT 1""").fetchone()
      else:
         if len(check) == 1:
            data = cur.execute(
               f"""SELECT * FROM places WHERE id != {check[0][2]} and category_id = {cat_id} ORDER BY RANDOM() LIMIT 1""").fetchone()
            if data is None:
               cur.execute(f"""DELETE FROM checked WHERE user_id = {user_id}""")
               conn.commit()
               await callback_query.message.answer(
                  '✨ На данный момент вы посмотрели все интересные места.\n💫 Теперь посты будут повторяться до добавления новых.')
               time.sleep(1.5)
               data = cur.execute(f"""SELECT * FROM places WHERE category_id = {cat_id} ORDER BY RANDOM() LIMIT 1""").fetchone()
         if len(check) == 2:
            data = cur.execute(
               f"""SELECT * FROM places WHERE id != {check[0][2]} and id != {check[1][2]} and category_id = {cat_id} ORDER BY RANDOM() LIMIT 1""").fetchone()
            if data is None:
               cur.execute(f"""DELETE FROM checked WHERE user_id = {user_id}""")
               conn.commit()
               await callback_query.message.answer(
                  '✨ На данный момент вы посмотрели все интересные места.\n💫 Теперь посты будут повторяться до добавления новых.')
               time.sleep(1.5)
               data = cur.execute(f"""SELECT * FROM places WHERE category_id = {cat_id} ORDER BY RANDOM() LIMIT 1""").fetchone()
         if len(check) == 3:
            data = cur.execute(
               f"""SELECT * FROM places WHERE id != {check[0][2]} and id != {check[1][2]} and id != {check[2][2]} and category_id = {cat_id} ORDER BY RANDOM() LIMIT 1""").fetchone()
            if data is None:
               cur.execute(f"""DELETE FROM checked WHERE user_id = {user_id}""")
               conn.commit()
               await callback_query.message.answer(
                  '✨ На данный момент вы посмотрели все интересные места.\n💫 Теперь посты будут повторяться до добавления новых.')
               time.sleep(1.5)
               data = cur.execute(f"""SELECT * FROM places WHERE category_id = {cat_id} ORDER BY RANDOM() LIMIT 1""").fetchone()
         if len(check) == 4:
            data = cur.execute(
               f"""SELECT * FROM places WHERE id != {check[0][2]} and id != {check[1][2]} and id != {check[2][2]} and id != {check[3][2]} and category_id = {cat_id} ORDER BY RANDOM() LIMIT 1""").fetchone()
            if data is None:
               cur.execute(f"""DELETE FROM checked WHERE user_id = {user_id}""")
               conn.commit()
               await callback_query.message.answer(
                  '✨ На данный момент вы посмотрели все интересные места.\n💫 Теперь посты будут повторяться до добавления новых.')
               time.sleep(1.5)
               data = cur.execute(f"""SELECT * FROM places WHERE category_id = {cat_id} ORDER BY RANDOM() LIMIT 1""").fetchone()
         if len(check) == 5:
            data = cur.execute(
               f"""SELECT * FROM places WHERE id != {check[0][2]} and id != {check[1][2]} and id != {check[2][2]} and id != {check[3][2]} and id != {check[4][2]} and category_id = {cat_id} ORDER BY RANDOM() LIMIT 1""").fetchone()
            if data is None:
               cur.execute(f"""DELETE FROM checked WHERE user_id = {user_id}""")
               conn.commit()
               await callback_query.message.answer(
                  '✨ На данный момент вы посмотрели все интересные места.\n💫 Теперь посты будут повторяться до добавления новых.')
               time.sleep(1.5)
               data = cur.execute(f"""SELECT * FROM places ORDER BY RANDOM() LIMIT 1""").fetchone()
         if len(check) == 0:
            cur.execute(f"""DELETE FROM checked WHERE user_id = {user_id}""")
            conn.commit()
            data = cur.execute(f"""SELECT * FROM places ORDER BY RANDOM() LIMIT 1""").fetchone()
            if data is None:
               cur.execute(f"""DELETE FROM checked WHERE user_id = {user_id}""")
               conn.commit()
               await callback_query.message.answer(
                  '✨ На данный момент вы посмотрели все интересные места.\n💫 Теперь посты будут повторяться до добавления новых.')
               time.sleep(1.5)
               data = cur.execute(f"""SELECT * FROM places WHERE category_id = {cat_id} ORDER BY RANDOM() LIMIT 1""").fetchone()

      cur.execute(f"""INSERT INTO checked (user_id, post_id) VALUES ({user_id}, {data[0]})""")
      conn.commit()

      TextMenuBTNS = InlineKeyboardMarkup(row_width=3)
      send = []

      if data[7] == 'нет':
         pass
      else:
         TextMenuBtns2 = InlineKeyboardButton('🌐 Открыть сайт', url=f'{data[7]}')

      dd = cur.execute(
         f"""SELECT * FROM likes WHERE post_id = {data[0]} and user_id = {callback_query.from_user.id}""").fetchone()

      if dd != None:
         TextMenuBtns3 = InlineKeyboardButton('💔 Dislike', callback_data=f'del_from_favorite {data[0]}')
      else:
         TextMenuBtns3 = InlineKeyboardButton('❤ Like', callback_data=f'add_to_favorite {data[0]}')
      if data[8] == 'нет':
         pass
      else:
         TextMenuBtns4 = InlineKeyboardButton('🗾 Найти на картах', url=f'{data[8]}')
      TextMenuBtns5 = InlineKeyboardButton('➡ Следующий пост', callback_data=f'serch_cat {cat_id}')
      send.extend((TextMenuBtns2, TextMenuBtns3, TextMenuBtns4, TextMenuBtns5))
      TextMenuBTNS.add(*send)

      caption = f"""

      {data[1]}

      {data[3]}   

            """

      await bot.send_photo(chat_id=callback_query.message.chat.id, photo=f'{data[2]}', caption=caption,
                           parse_mode='HTML',
                           reply_markup=TextMenuBTNS)




#
#
# АДМИН МЕНЮ КОМАНДЫ
#
#

@dp.message_handler(commands=['admin_menu'])
async def admin_menu(message: types.Message):
   user_id = message.from_user.id

   check = cur.execute(f"""SELECT admin_mode FROM users WHERE user_id = {user_id}""").fetchone()

   if check[0] == 'admin':
      await message.answer(f'{message.from_user.first_name} приветствую в админ панели!', reply_markup=ADMIN_MAIN_MENU)


@dp.message_handler(lambda message: message.text == "🗂 Публикации")
async def admin_menu(message: types.Message):
   user_id = message.from_user.id

   check = cur.execute(f"""SELECT admin_mode FROM users WHERE user_id = {user_id}""").fetchone()

   if check[0] == 'admin':
      await message.answer(f'Что вы хотите?', reply_markup=ADMIN_PUBLICATION_BTNS)

@dp.message_handler(lambda message: message.text == "📑 База Данных")
async def admin_menu(message: types.Message):
   user_id = message.from_user.id

   check = cur.execute(f"""SELECT admin_mode FROM users WHERE user_id = {user_id}""").fetchone()

   if check[0] == 'admin':
      await message.answer(f'Что вы хотите?', reply_markup=ADMIN_MENU_BD)

@dp.message_handler(lambda message: message.text == "Категории")
async def admin_menu(message: types.Message):
   user_id = message.from_user.id

   check = cur.execute(f"""SELECT admin_mode FROM users WHERE user_id = {user_id}""").fetchone()

   if check[0] == 'admin':
      await message.answer(f'Что вы хотите?', reply_markup=ADMIN_BD_MENU_CATEGORYES)


class ADDCategory(StatesGroup):
   name = State()

@dp.message_handler(lambda message: message.text == "Добавить категорию")
async def admin_menu(message: types.Message):
   user_id = message.from_user.id

   check = cur.execute(f"""SELECT admin_mode FROM users WHERE user_id = {user_id}""").fetchone()

   if check[0] == 'admin':
      await message.answer('Введите название категории.')
      await ADDCategory.next()

@dp.message_handler(state=ADDCategory.name)
async def get_head(message: types.Message, state: FSMContext):
   async with state.proxy() as data:
      data['name'] = message.text
   cur.execute(f"""INSERT INTO categoryes (name) VALUES ('{data['name']}')""")
   conn.commit()
   ct_id = cur.execute(f"""SELECT * FROM categoryes WHERE name = '{data['name']}'""").fetchone()
   await message.answer(f'Отлично! Категория добавлена!\n\nID категории: <b>{ct_id[0]}</b>\nНазвание: "<b>{ct_id[1]}</b>"', parse_mode='HTML')
   await state.finish()

class DeleteCategory(StatesGroup):
   id = State()

@dp.message_handler(lambda message: message.text == "Удалить категорию")
async def delete_category(message: types.Message):
   user_id = message.from_user.id

   check = cur.execute(f"""SELECT admin_mode FROM users WHERE user_id = {user_id}""").fetchone()

   if check[0] == 'admin':
      await message.answer('Введите id удаляемой категории.')
      await DeleteCategory.next()

@dp.message_handler(state=DeleteCategory.id)
async def delete_cat_id(message: types.Message, state: FSMContext):
   async with state.proxy() as ct_cat:
      ct_cat['id'] = message.text
   cur.execute(f"""DELETE FROM categoryes WHERE id = {ct_cat['id']}""")
   conn.commit()
   await message.answer(f"Категория была удалена!\n\nID категории: <b>{ct_cat['id']}</b>", parse_mode='HTML')
   await state.finish()

class PlacesState(StatesGroup):
   head = State()
   photo = State()
   description = State()
   price = State()
   sale = State()
   new_price = State()
   site = State()
   adress = State()
   category_id = State()

@dp.callback_query_handler(lambda c: c.data == 'add_post')
async def add_post(message: types.Message):
   await message.answer('Введите загаловок поста.')
   await PlacesState.next()

@dp.message_handler(state=PlacesState.head)
async def get_head(message: types.Message, state: FSMContext):
   async with state.proxy() as data:
      data['head'] = message.text
   await message.answer('Отправте боту фото.')
   await PlacesState.next()

@dp.message_handler(content_types=['photo'], state=PlacesState.photo)
async def get_photo(message: types.Message, state: FSMContext):
   async with state.proxy() as data:
      data['photo'] = message.photo[0].file_id
   await message.answer('Теперь введите описание.')
   await PlacesState.next()

@dp.message_handler(state=PlacesState.description)
async def get_description(message: types.Message, state: FSMContext):
   async with state.proxy() as data:
      data['description'] = message.text
   await message.answer('Введите цену билета.\nЕсли посещение бесплатное, введите "0"\nЕсли цена не указана, введите "-1"')
   await PlacesState.next()

@dp.message_handler(state=PlacesState.price)
async def get_price(message: types.Message, state: FSMContext):
   try:
      val = int(message.text)
      async with state.proxy() as data:
         data['price'] = int(message.text)
      await message.answer('Введите размер скидки в процентах.\nЕсли её нет, введите "0"')
      await PlacesState.next()
   except ValueError:
      await message.answer("Вы ввели неверные данные!\n")

@dp.message_handler(state=PlacesState.sale)
async def get_sale(message: types.Message, state: FSMContext):
   try:
      val = int(message.text)
      async with state.proxy() as data:
         data['sale'] = int(message.text)
      await message.answer('Введите цену со скидкой.\nЕсли её нет, введите "0"')
      await PlacesState.next()
   except ValueError:
      await message.answer("Вы ввели неверные данные!\n")

@dp.message_handler(state=PlacesState.new_price)
async def get_price(message: types.Message, state: FSMContext):
   try:
      val = int(message.text)
      async with state.proxy() as data:
         data['new_price'] = int(message.text)
      await message.answer('Введите сайт.\nЕсли его нет, введите "нет"')
      await PlacesState.next()
   except ValueError:
      await message.answer("Вы ввели неверные данные!\n")

@dp.message_handler(state=PlacesState.site)
async def get_description(message: types.Message, state: FSMContext):
   async with state.proxy() as data:
      data['site'] = message.text
   await message.answer('Введите адрес мероприятия/места.\nЕсли адреса нет, введите "нет"')
   await PlacesState.next()

@dp.message_handler(state=PlacesState.adress)
async def get_adress(message: types.Message, state: FSMContext):
   async with state.proxy() as data:
      data['adress'] = message.text
   cat = cur.execute("""SELECT * FROM categoryes""").fetchall()
   await message.answer('Теперь введите id категории!')
   for i in cat:
      await message.answer(f'id: <b>{i[0]}</b>\nНазвание: "<b>{i[1]}</b>"', parse_mode='HTML')
   await PlacesState.next()

@dp.message_handler(state=PlacesState.category_id)
async def get_adress(message: types.Message, state: FSMContext):
   async with state.proxy() as data:
      data['category_id'] = message.text
   cur.execute(
      f"""INSERT INTO places (head, photo, description, price, sale, new_price, site, adress, category_id) VALUES ('{data['head']}', '{data['photo']}', '{data['description']}', {data['price']}, {data['sale']}, {data['new_price']}, '{data['site']}', '{data['adress']}', {data['category_id']})""")
   conn.commit()
   place_id = cur.execute(f"""SELECT id FROM places WHERE photo = '{data['photo']}'""").fetchone()
   await message.answer(f'Отлично! Место загружено!\n\nID поста: <b>{place_id[0]}</b>', parse_mode='HTML')
   await state.finish()


class DeletePost(StatesGroup):
   id = State()

@dp.callback_query_handler(lambda c: c.data == 'delete_post')
async def add_post(message: types.Message):
   await message.answer('Введите id удаляемого поста.')
   await DeletePost.next()

@dp.message_handler(state=DeletePost.id)
async def delete_post_id(message: types.Message, state: FSMContext):
   async with state.proxy() as dt:
      dt['id'] = message.text
   cur.execute(f"""DELETE FROM places WHERE id = {dt['id']}""")
   conn.commit()
   await message.answer(f"Запись была удалена!\n\nID поста: <b>{dt['id']}</b>", parse_mode='HTML', reply_markup=ADMIN_MAIN_MENU)
   await state.finish()


@dp.message_handler(lambda message: message.text == "🚪 Выйти")
async def admin_menu(message: types.Message):
   user_id = message.from_user.id

   check = cur.execute(f"""SELECT admin_mode FROM users WHERE user_id = {user_id}""").fetchone()

   if check[0] == 'admin':
      await message.answer(f'<b>{message.from_user.first_name}</b> вы вышли из админ панели!', parse_mode='HTML', reply_markup=MainMenuBtns)


# Запуск


print('\nБаза данных пользователей:\n')
print(cur.execute('SELECT * FROM users').fetchall())
time.sleep(0.3)
print('\nБаза данных мест:\n')
print(cur.execute('SELECT * FROM places').fetchall())
print()
print('\nБаза данных категорий:\n')
print(cur.execute('SELECT * FROM categoryes').fetchall())
print()

if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)