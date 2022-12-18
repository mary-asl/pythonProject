from aiogram import types

from dispatcher import dp
import re
from bot import BotDB

markup_inline = types.InlineKeyboardMarkup()
item_old = types.InlineKeyboardButton(text='2004-2006', callback_data='get_old')
item_new = types.InlineKeyboardButton(text='2022', callback_data='get_new')
markup_inline.add(item_old, item_new)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.bot.send_message(message.from_user.id,
                                   "Добро пожаловать! С помощью данного бота Вы можете узнать, "
                                   "как выглядели здания Санкт-Петербурга в разный период времени. "
                                   "Для этого просто введите адрес интересного "
                                   "вам объекта в формате \"улица номер дома\". \n"
                                   "Например: Большая Пушкарская 5")


@dp.message_handler(content_types=types.ContentType.TEXT)
async def get_text(message: types.Message):
    global address_clear
    address = message.text.lower()
    address_clear = re.sub("[-.?!)(,:]", "", address)
    address_clear = re.sub("набережная", "наб", address_clear)
    address_clear = re.sub("площадь", "пл", address_clear)
    f_condition = BotDB.address_old_exist(address_clear)
    s_condition = BotDB.address_new_exist(address_clear)

    if f_condition or s_condition:
        await message.reply("Получить фото за год: ", reply_markup=markup_inline)
    else:
        await message.bot.send_message(message.from_user.id, "Извините, такого адреса ещё нет в галерее")


@dp.callback_query_handler(text='get_old')
async def get_old(callback: types.CallbackQuery):
    links = " ".join(map(str, BotDB.get_link_old(address_clear)))
    if len(links) == 0:
        await callback.message.answer("Фотографий этого дома за данный год пока нет")
        await callback.answer()
    else:
        links_clear = re.sub("[)(,']", "", links)
        links = links_clear.split(' ')
        for link in links:
            link_good = "".join(link)
            await dp.bot.send_photo(callback.from_user.id, link_good)
        await dp.bot.edit_message_reply_markup(message_id=callback.message.message_id, chat_id=callback.message.chat.id,
                                               reply_markup=None)
        await callback.answer()


@dp.callback_query_handler(text='get_new')
async def get_new(callback: types.CallbackQuery):
    links = " ".join(map(str, BotDB.get_link_new(address_clear)))
    if len(links) == 0:
        await callback.message.answer("Фотографий этого дома за данный год пока нет")
        await callback.answer()
    else:
        links_clear = re.sub("[)(,']", "", links)
        links = links_clear.split(' ')
        for link in links:
            link_good = "".join(link)
            await dp.bot.send_photo(callback.from_user.id, link_good)
            await dp.bot.edit_message_reply_markup(message_id=callback.message.message_id,
                                                   chat_id=callback.message.chat.id,
                                                   reply_markup=None)
        await callback.answer()
