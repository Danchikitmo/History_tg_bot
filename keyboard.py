from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
import dataBase.request

# Создание клавиатуры с кнопками
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Показать всех учеников")],
              [KeyboardButton(text="Отправить задание определенному ученику")],
              [KeyboardButton(text="Добавить нового администратора")],
              [KeyboardButton(text="Показать всех администраторов")],
              [KeyboardButton(text="Отправить задание всем")]],  # Обязательно передаем список кнопок в параметре 'keyboard'
    resize_keyboard=True
)

back_button = KeyboardButton(text="В главное меню")

async def keyboard_users(msg: Message):
    rows = await dataBase.request.show_all()

    if rows:
        # Создаем кнопки для пользователей
        buttons = [KeyboardButton(text=f"{row[0]}) {row[1]} {row[2]}") for row in rows]

        # Определяем количество кнопок в ряду (например, по 2 кнопки в строке)
        num_buttons_per_row = 2
        button_rows = [buttons[i:i + num_buttons_per_row] for i in range(0, len(buttons), num_buttons_per_row)]

        # Добавляем кнопку "Назад" в последний ряд
        button_rows.append([back_button])

        # Создаем клавиатуру
        keyboard = ReplyKeyboardMarkup(
            keyboard=button_rows,
            resize_keyboard=True
        )
    else:
        # Если нет данных, отображаем сообщение и кнопку "Назад"
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Нет данных для отображения.")], [KeyboardButton(text="Назад")]],
            resize_keyboard=True
        )

    await msg.answer("Выберите пользователя:", reply_markup=keyboard)




async def keyboasrd_all_admin(msg: Message):
    rows = await dataBase.request.show_all_admin()

    if rows:
        # Создаем кнопки для пользователей
        buttons = [KeyboardButton(text=f"Админ {row[0]}) {row[1]} {row[2]}") for row in rows]

        # Определяем количество кнопок в ряду
        num_buttons_per_row = 2
        # Организуем кнопки в несколько рядов
        button_rows = [buttons[i:i + num_buttons_per_row] for i in range(0, len(buttons), num_buttons_per_row)]

        # Добавляем кнопку "Назад" в последний ряд
        button_rows.append([back_button])

        # Создаем клавиатуру
        keyboard = ReplyKeyboardMarkup(
            keyboard=button_rows,
            resize_keyboard=True
        )
    else:
        # Если нет данных, отображаем сообщение и кнопку "Назад"
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Нет данных для отображения.")], [back_button]],
            resize_keyboard=True
        )

    await msg.answer("Все администраторы", reply_markup=keyboard)




async def keyboard_users_admin(msg: Message):
    rows = await dataBase.request.show_all()

    if rows:
        # Создаем кнопки для пользователей
        buttons = [KeyboardButton(text=f"Пользователь {row[0]}) {row[1]} {row[2]}") for row in rows]

        # Определяем количество кнопок в ряду (например, по 2 кнопки в строке)
        num_buttons_per_row = 2
        button_rows = [buttons[i:i + num_buttons_per_row] for i in range(0, len(buttons), num_buttons_per_row)]

        # Добавляем кнопку "Назад" в последний ряд
        button_rows.append([back_button])

        # Создаем клавиатуру
        keyboard = ReplyKeyboardMarkup(
            keyboard=button_rows,
            resize_keyboard=True
        )
    else:
        # Если нет данных, отображаем сообщение и кнопку "Назад"
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Нет данных для отображения.")], [KeyboardButton(text="Назад")]],
            resize_keyboard=True
        )

    await msg.answer("Выберите пользователя:", reply_markup=keyboard)



question_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Отправить файл")],
              [KeyboardButton(text="Отправить фото")]],
    resize_keyboard=True
)


async def keyboard_сhildren(msg: Message):
    rows = await dataBase.request.show_all_children()

    if rows:
        # Создаем кнопки для пользователей
        buttons = [KeyboardButton(text=f"Ученик {row[0]}) {row[1]} {row[2]}") for row in rows]

        # Определяем количество кнопок в ряду (например, по 2 кнопки в строке)
        num_buttons_per_row = 2
        button_rows = [buttons[i:i + num_buttons_per_row] for i in range(0, len(buttons), num_buttons_per_row)]

        # Добавляем кнопку "Назад" в последний ряд
        button_rows.append([back_button])

        # Создаем клавиатуру
        keyboard = ReplyKeyboardMarkup(
            keyboard=button_rows,
            resize_keyboard=True
        )
    else:
        # Если нет данных, отображаем сообщение и кнопку "Назад"
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="Нет данных для отображения.")], [KeyboardButton(text="Назад")]],
            resize_keyboard=True
        )

    await msg.answer("Выберите пользователя:", reply_markup=keyboard)
