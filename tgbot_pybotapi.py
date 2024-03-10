import telebot
from telebot import types
import logging
#import simpleparser
import random
import time
from gpttest import askwithgpt

from dotenv import load_dotenv
import os

load_dotenv()

bot = telebot.TeleBot(os.getenv("TOKEN"))

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)


def gen_markup():
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(types.InlineKeyboardButton("Yes", callback_data="2"),
                               types.InlineKeyboardButton("No", callback_data="cb_no"))
    return markup


#########################################	
@bot.message_handler(commands=['start'])
def send_welcome(message):
	cid = message.chat.id
	bot.send_message(cid, ''' Добро пожаловать! ''', reply_markup=types.ReplyKeyboardRemove(selective=False))


@bot.message_handler(commands=["gpt"])
def typingprompt(message):
    sent_msg = bot.send_message(message.chat.id, "Введите ваш запрос: \n\n(Генерация занимает около 5-10 секунд, пожалуйста подождите после ввода запроса.)")
    bot.register_next_step_handler(sent_msg, enteredprompt) #Next message will call the enteredprompt function #Ждёт сообщение и как получает - переходит к функции, так ведь?
def enteredprompt(message):
    prompt = message.text
    result = askwithgpt(prompt)
    bot.send_message(message.chat.id, text=f"Ответ:\n-----------------------------\n\n{result}\n\n-----------------------------\nНовый запрос: /gpt")


#@bot.message_handler(commands=['ultrasecretfunction'])
#def send_blogs(message):
#	cid = message.chat.id
#	bot.send_message(cid, str(simpleparser.blogs_soc_func()))


@bot.message_handler(commands=['dicerand'])
def play_random_dice(message):
	cid = message.chat.id
	##############
	randomnum = random.randint(1,5)
	player_random_result = "Ваше число: " + str(randomnum)
	bot.send_message(cid, player_random_result)
	##############
	dicevalue = bot.send_dice(cid, "🎲")
	time.sleep(3.5)
	bot_result = "Результат бота(рандом): " + str(dicevalue.dice.value)
	bot.send_message(cid, bot_result)

	if randomnum != dicevalue.dice.value:
		bot.send_message(cid, "проебал(")
	elif randomnum == dicevalue.dice.value:
		bot.send_message(cid, "выйграл сука")
#########################################	



	
@bot.message_handler(func=lambda message: message.text == 'ok')
def sendok(message):
	bot.send_message(message.chat.id, "ok")

@bot.message_handler(commands=['dicestat'])
def play_static_dice(message):
	cid = message.chat.id
	
	bot.send_message(cid, '''Добро пожаловать в dice!\nВыберите ваше счастливое число:''', reply_markup=gen_markup())


	button_1 = telebot.types.KeyboardButton("1")
	button_2 = telebot.types.KeyboardButton("2")
	button_3 = telebot.types.KeyboardButton("3")
	button_4 = telebot.types.KeyboardButton("4")
	button_5 = telebot.types.KeyboardButton("5")
	button_6 = telebot.types.KeyboardButton("6")
	markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	markup.row(button_1, button_2, button_3, button_4, button_5, button_6)
	 #keyboards.dice_keyboard) #from keyboards.py
#	bot.register_next_step_handler(message, diceuservalue)

def diceuservalue(message):
	userinput = message.text
	bot.send_message(message.chat.id, ("Ваше число: " + userinput))
	
@bot.message_handler(func=lambda message: message.text == "testinl")
def message_handler(message):
    bot.send_message(message.chat.id, "Yes/no?", reply_markup=gen_markup())	



#########################################
@bot.message_handler(commands=['getbotname'])
def get_bot_name(message):
	getme = str(bot.get_my_name()).split("\'")
	bot.send_message(message.chat.id, getme[3])




#@bot.message_handler(func=lambda message: True)
#def logging(message):
#	print("Пользователь " + str(message.from_user.first_name) + " (id " + str(message.from_user.id) + ") " + "написал: " + message.text)
##############


@bot.callback_query_handler(func=lambda call: call.data == "2")
def callback_query(call):
	bot.answer_callback_query(call.id, "ok", show_alert=False)


def main():
	bot.infinity_polling()

if __name__ == "__main__":
    main()
	