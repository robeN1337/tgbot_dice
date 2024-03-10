import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import InlineKeyboardButton 
from aiogram.utils.keyboard import InlineKeyboardBuilder
import random
from aiogram import F  # ВОТ ЭТА ХУЙНЯ РАБОТАЕТ С ИНЛАЙН КНОПКАМИ. Я ХЗ КАК
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO)

load_dotenv()

bot = Bot(token=os.getenv("TOKEN"))

dp = Dispatcher()


async def send_inlinekeyboard_test(chat_id):
    keyboard = InlineKeyboardBuilder()
    button = InlineKeyboardButton(text="Нажми меня", callback_data="random_value")
    keyboard.add(button)

    await bot.send_message(chat_id, "Выберите опцию:", reply_markup=keyboard.as_markup())

@dp.callback_query(F.data == "random_value")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(str(random.randint(1,10)))
    await callback.message.answer("ok")
    await callback.answer("/test1 callback ok", show_alert=True)

async def send_dice_inline_keyboard():
    
    keyboard = InlineKeyboardBuilder()
    button1 = InlineKeyboardButton(text="1", callback_data="button1")
    button2 = InlineKeyboardButton(text="2", callback_data="button2")
    button3 = InlineKeyboardButton(text="3", callback_data="button3")
    button4 = InlineKeyboardButton(text="4", callback_data="button4")
    button5 = InlineKeyboardButton(text="5", callback_data="button5")
    button6 = InlineKeyboardButton(text="6", callback_data="button6")
    keyboard.add(button1, button2, button3, button4, button5, button6)

    return keyboard.as_markup(resize_keyboard=True)

# Хэндлер на команду /test2
#@dp.message(Command("test2")) Декоратор не нужен, т.к. функция зарегестрирована в main
async def cmd_test2(message: types.Message):
    await message.send_copy(message.chat.id)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!", reply_markup=types.ReplyKeyboardRemove())

# Хэндлер на команду /test1
@dp.message(Command("test1"))
async def cmd_test1(message: types.Message):
    await send_inlinekeyboard_test(chat_id=message.chat.id)
    
@dp.message(Command("dicerand"))
async def play_random_dice(message):
    cid = message.chat.id
    ##############
    randomnum = random.randint(1,5)
    player_random_result = "Ваше число: " + str(randomnum)
    await bot.send_message(cid, player_random_result)
    ##############
    dicevalue = await bot.send_dice(chat_id=cid, emoji="🎲")
    await asyncio.sleep(3.5)
    bot_result = "Результат бота(рандом): " + str(dicevalue.dice.value)
    await bot.send_message(cid, bot_result)

    if randomnum != dicevalue.dice.value:
        await bot.send_message(cid, "проебал(")
    elif randomnum == dicevalue.dice.value:
        await bot.send_message(cid, "выйграл сука")

@dp.message(Command("dicestat"))
async def static_dice_num(message):

    cid = message.chat.id
    ##############
    keyboard = await send_dice_inline_keyboard()
    await bot.send_message(cid, "Выберите число: ", reply_markup=keyboard)

@dp.callback_query(F.data.startswith("button"))
async def dicestat(call: types.CallbackQuery):
    cid = call.message.chat.id
    userinput = list(call.data)[6]  # разделил callback data методом list на символы и вывел в список
    await call.message.edit_reply_markup()
    await call.message.edit_text("Выбранное число: " + userinput)
    await call.answer()

    dicevalue = await bot.send_dice(chat_id=cid, emoji="🎲")
    await asyncio.sleep(3.5)
    bot_result = "Результат бота(рандом): " + str(dicevalue.dice.value)
    await bot.send_message(cid, bot_result)

    if int(userinput) != dicevalue.dice.value:
        await bot.send_message(cid, "проебал(\n\nПовторить: /dicestat ")
    elif int(userinput) == dicevalue.dice.value:
        await bot.send_message(cid, "выйграл сука\n\nПовторить: /dicestat")


#@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(message.chat.id, reply_to_message_id=message.message_id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")




# Использование


async def main():
    await dp.start_polling(bot)
    dp.message.register(cmd_test2, Command("test2")) # принудительная регистрация хэндлера без декоратора
if __name__ == "__main__":
    asyncio.run(main())

