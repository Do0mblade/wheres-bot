cur.execute(f"""INSERT INTO users (first_name, user_id) VALUES ('{first_name}', {user_id})""")
      conn.commit()

      await message.reply("✅ Вы успешно зарегистрированы!", reply_markup=MainMenuBtns)
      time.sleep(0.7)
      await message.answer("⚡ Хотите следить за актуальными новостями?", reply_markup=inline_kb_channel)


if user[4] == 'Мужской':
      smile_gender = '👨'
if user[4] == 'Женский':
      smile_gender = '👩'

if int(user[3]) > 5 and int(user[3]) < 11:
      smile_age = '👶'
if int(user[3]) > 10 and int(user[3]) < 17 and user['4'] == 'Мужской':
      smile_age = '👦'
if int(user[3]) > 10 and int(user[3]) < 17 and user['4'] == 'Женский':
      smile_age = '👧'
if int(user[3]) > 16 and int(user[3]) < 60 and user['4'] == 'Мужской':
      smile_age = '👨'
if int(user[3]) > 16 and int(user[3]) < 60 and user['4'] == 'Женский':
      smile_age = '👩'
if int(user[3]) > 59 and user['4'] == 'Мужской':
      smile_age = '🧓'
if int(user[3]) > 59 and user['4'] == 'Женский':
      smile_age = '👵'





cur.execute("""CREATE TABLE IF NOT EXISTS places(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    head TEXT NOT NULL,
    photo TEXT NOT NULL,
    description TEXT NOT NULL,
    price INTEGER NOT NULL,
    sale INTEGER NOT NULL,
    new_price INTEGER NOT NULL,
    site TEXT NOT NULL,
    adress TEXT NOT NULL;
)""")







TextMenuBtns1 = InlineKeyboardButton('📑 Подробнее', callback_data='more_info_for_post')
TextMenuBtns1_2 = InlineKeyboardButton('📑 Скрыть', callback_data='less_info_for_post')
TextMenuBtns2 = InlineKeyboardButton('🌐 Открыть сайт', url='http://ranepa.ru/')
TextMenuBtns3 = InlineKeyboardButton('❤ В избранное', callback_data='add_to_favorite')
TextMenuBtns4 = InlineKeyboardButton('🗾 Найти на картах', url='https://yandex.ru/maps/org/rossiyskaya_akademiya_narodnogo_khozyaystva_i_gosudarstvennoy_sluzhby/1313411848/?ll=37.479227%2C55.665088&source=entity_search&z=15')

TextMenuBTNS = InlineKeyboardMarkup(resize_keyboard=True)
TextMenuBTNS.add(TextMenuBtns1, TextMenuBtns2, TextMenuBtns3, TextMenuBtns4)
TextMenuBTNS.add(InlineKeyboardButton('✨ Last Moment Channel', url='https://t.me/wheres_official'))


TextMenuBTNS2 = InlineKeyboardMarkup(resize_keyboard=True)
TextMenuBTNS2.add(TextMenuBtns1_2, TextMenuBtns2, TextMenuBtns3, TextMenuBtns4)
TextMenuBTNS2.add(InlineKeyboardButton('✨ Last Moment Channel', url='https://t.me/wheres_official'))






