


from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

register_btn = KeyboardButton('📑 Да, зарегистрируй меня.')
register_btn1 = KeyboardButton('🚫 Нет, спасибо')

register_btns = ReplyKeyboardMarkup(resize_keyboard=True)
register_btns.add(register_btn)
register_btns.add(register_btn1)


MainMenuBTNS = ['📋 Профиль', '❤ Избранное', '🎁 Бонусы', '🔎 Поиск', '⚙ Настройки', 'ℹ Инфо', '💳 Поддержать']

MainMenuBtns = ReplyKeyboardMarkup(resize_keyboard=True)
MainMenuBtns.add(*MainMenuBTNS)

GenderMenu = ['👨 Мужской', '👩 Женский']

GenderMenus = ReplyKeyboardMarkup(resize_keyboard=True)
GenderMenus.add(*GenderMenu)


inline_kb_channel = InlineKeyboardMarkup()
inline_kb_channel.add(InlineKeyboardButton('✨ Last Moment Channel', url='https://t.me/wheres_official'))

Donate_money = InlineKeyboardMarkup()
Donate_money.add(InlineKeyboardButton('🔮 Last Moment ', url='https://www.donationalerts.com/r/last_moment'))


SettingsSearch = InlineKeyboardButton('🔎 Поиск без фильтров', callback_data='Search_no_filters')
SettingsSearchFilters = InlineKeyboardButton('⚙ Настроить поиск', callback_data='Search_yes_filters')
SettingsSearchBox = InlineKeyboardMarkup()
SettingsSearchBox.add(SettingsSearch, SettingsSearchFilters)


ADMIN_MAIN_MENU_BTNS = ['📑 База Данных', '🗂 Публикации', '🚪 Выйти']
ADMIN_MAIN_MENU = ReplyKeyboardMarkup(resize_keyboard=True)
ADMIN_MAIN_MENU.add(*ADMIN_MAIN_MENU_BTNS)

ADMIN_PUBLICATION_BTN_1 = InlineKeyboardButton('📚 Добавить запись', callback_data='add_post')
ADMIN_PUBLICATION_BTN_2 = InlineKeyboardButton('❌ Удалить запись', callback_data='delete_post')
ADMIN_PUBLICATION_BTN_3 = InlineKeyboardButton('✒ Изменить запись', callback_data='edit_post')
ADMIN_PUBLICATION_BTNS = InlineKeyboardMarkup(row_width=2)
ADMIN_PUBLICATION_BTNS.add(ADMIN_PUBLICATION_BTN_1, ADMIN_PUBLICATION_BTN_2, ADMIN_PUBLICATION_BTN_3)

ADMIN_MENU_BD_BTNS = ['Пользователи', 'Посты', 'Категории']
ADMIN_MENU_BD = ReplyKeyboardMarkup(resize_keyboard=True)
ADMIN_MENU_BD.add(*ADMIN_MENU_BD_BTNS)


ADMIN_BD_MENU_CATEGORYES_BTNS = ['Добавить категорию', 'Удалить категорию']
ADMIN_BD_MENU_CATEGORYES = ReplyKeyboardMarkup(resize_keyboard=True)
ADMIN_BD_MENU_CATEGORYES.add(*ADMIN_BD_MENU_CATEGORYES_BTNS)




