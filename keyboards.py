from telebot import types

dice_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
numberbutton_1 = types.KeyboardButton("1")
numberbutton_2 = types.KeyboardButton("2")
numberbutton_3 = types.KeyboardButton("3")
numberbutton_4 = types.KeyboardButton("4")
numberbutton_5 = types.KeyboardButton("5")
numberbutton_6 = types.KeyboardButton("6")
dice_keyboard.add(numberbutton_1, 
            numberbutton_2, 
            numberbutton_3, 
            numberbutton_4, 
            numberbutton_5, 
            numberbutton_6
            )


inlinekeyboard = types.InlineKeyboardMarkup()
inlinebutton_1 = types.InlineKeyboardButton("44", callback_data="bruh")
inlinebutton_2 = types.InlineKeyboardButton("Кнопка 2", callback_data='2')
inlinebutton_3 = types.InlineKeyboardButton("Кнопка 3", callback_data='3')
inlinekeyboard.add(inlinebutton_1, inlinebutton_2, inlinebutton_3)