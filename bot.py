import asyncio
import types
import io
from os import remove
from PIL import Image
from aiogram import *
import logging
from sys import stdout
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import hbold
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.answer(f'Hello broske {hbold(message.from_user.full_name)}!')
    button = types.InlineKeyboardButton(text='Да, хочу!😊', callback_data='positive')
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[button]])
    await message.answer(f'Хочешь узнать какой ты котик сегодня?', reply_markup=keyboard)
    print('message has been sanded')

@dp.callback_query()
async def what_a_cat(callback_query: types.CallbackQuery):
    bot = callback_query.bot
    if callback_query.data == 'positive':
        from parser import main as parse_main
        data = await parse_main()
        image = Image.open(io.BytesIO(data))
        print(image)
        temp_image_path = 'temp.jpg'
        image.save(temp_image_path)
        ##
        button1 = types.InlineKeyboardButton(text='Ееее я крутышка 😊', callback_data='agree')
        button2 = types.InlineKeyboardButton(text='Я не такой котя! 😞', callback_data='positive')
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[button1, button2]])
        await callback_query.message.answer_photo(
            types.FSInputFile(path=temp_image_path), caption='Такой ты сегодня котик', reply_markup=keyboard
        )
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
        await remove(temp_image_path)
    if callback_query.data == 'agree':
        button = types.InlineKeyboardButton(text='Посмотреть еще котиков', callback_data='positive')
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[[button]])
        await bot.edit_message_caption(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            caption='Сохраняй котика чтобы не потерять 😸'
        )
        await bot.edit_message_reply_markup(
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            reply_markup=keyboard
        )

        await callback_query.answer('Ты крутышка!')

async def main():
    bot = Bot('YOUR_TOKEN', parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=stdout)
    asyncio.run(main())
