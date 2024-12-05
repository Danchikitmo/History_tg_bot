from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import re

import dataBase.request
import main
from keyboard import main_keyboard, back_button, keyboard_users
import keyboard
import Notifacation


router = Router()


class UserForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_surname = State()
    waiting_for_chat = State()


@router.message(Command("start"))
async def start_handler(msg: Message, state: FSMContext):
    await msg.answer("Привет. Это чат-бот в помощь Арины Костиной!!!!", reply_markup=ReplyKeyboardRemove())
    await msg.answer("Введи своё имя")
    await state.set_state(UserForm.waiting_for_name)


@router.message(UserForm.waiting_for_name)
async def get_name(msg: Message, state: FSMContext):
    name_user = msg.text
    tg_id = msg.from_user.id
    chat_id = msg.chat.id

    await state.update_data(name_user=name_user, tg_id=tg_id, chat_id = chat_id)

    await msg.answer("Введи свою фамилию")
    await state.set_state(UserForm.waiting_for_surname)


@router.message(UserForm.waiting_for_surname)
async def get_surname(msg: Message, state: FSMContext):
    surname = msg.text

    user_data = await state.get_data()
    name_user = user_data.get("name_user")
    tg_id = user_data.get("tg_id")
    chat_id = user_data.get("chat_id")

    await dataBase.request.insert_data(name_user, surname, tg_id, chat_id)

    await state.clear()

    if await dataBase.request.check_user(tg_id):
        await msg.answer("Отлично! Вы есть в нашей таблице!")

    if await dataBase.request.check_admin(tg_id) == 'True':
        await msg.answer(f"Вы авторизовались как администратор", reply_markup=main_keyboard)


@router.message(lambda message: message.text == "Показать всех учеников")
async def show_all_handler(msg: Message):
    await keyboard_users(msg)


@router.message(lambda message: re.match(r'^\d+\)', message.text))
async def handle_user_selection(msg: Message):
    selected_user = msg.text
    user_id_match = re.match(r'^\d+', selected_user)
    if user_id_match:
        user_id = user_id_match.group(0)
        tg_id = await dataBase.request.get_tg_id(user_id)
        print(f"Selected user ID: {user_id}, Telegram ID: {tg_id}")
        await msg.answer(f"Вы выбрали: {selected_user} \nTelegram ID: {tg_id}", reply_markup=main_keyboard)
    else:
        await msg.answer("Не удалось распознать формат сообщения.")



@router.message(lambda message: message.text == "Отправить задание определенному ученику")
async def show_all_handler(msg: Message):
    await keyboard.keyboard_сhildren(msg)

@router.message(lambda message: re.match(r'^\d+\)', message.text))
async def handle_user_selection(msg: Message):
    selected_user = msg.text
    user_id_match = re.match(r'^\d+', selected_user)
    if user_id_match:
        user_id = user_id_match.group(0)
        tg_id = await dataBase.request.get_tg_id(user_id)
        # print(f"Selected user ID: {user_id}, Telegram ID: {tg_id}")
        await msg.answer(f"Вы выбрали: {selected_user} \nTelegram ID: {tg_id}", reply_markup=main_keyboard)
    else:
        await msg.answer("Не удалось распознать формат сообщения.")


@router.message(lambda message: message.text == "В главное меню")
async def main_menu(msg: Message):
    await msg.answer("Вы в главном меню", reply_markup=main_keyboard)


@router.message(lambda message: message.text == "Показать всех администраторов")
async def show_admin(msg: Message):
    await keyboard.keyboasrd_all_admin(msg)

@router.message(lambda message: message.text == "Добавить нового администратора")
async def add_new_admin(msg: Message):
    await keyboard.keyboard_users_admin(msg)

@router.message(lambda message: re.match(r'^Пользователь \d+\)', message.text))
async def handler_admin_selection(msg: Message, bot: Bot):
    selected_user = msg.text
    user_id_match = re.match(r'Пользователь (\d+)', selected_user)
    user_id = user_id_match.group(1)
    tg_id = await dataBase.request.get_tg_id(user_id)

    # Добавляем администратора
    id = await dataBase.request.insert_admin(tg_id)

    chat_id = await dataBase.request.get_chat_id(id)

    # Отправляем сообщение пользователю о выборе
    await msg.answer(f"Вы выдали права администратора: {selected_user}", reply_markup=main_keyboard)

    await Notifacation.notify_admin(bot, chat_id)

@router.message(lambda message: message.text == "Отправить задание всем")
async def handler_question_all(msg: Message):
    await keyboard.question_keyboard(msg)


@router.message(lambda message: message.text == "Отправить файл")
async def handler_fail_send(msg: Message):
    await msg.answer("Отправьте файл")

@router.message(lambda message: message.text == "Отправить фото")
async def handler_photo_send(msg: Message):
    await msg.answer("Отправьте фото")


@router.message(lambda message: re.match(r'^Ученик \d+\)', message.text))
async def handler_admin_selection(msg: Message, bot: Bot):
    user_chat_id = set()
    selected_user = msg.text
    user_id_match = re.match(r'Ученик (\d+)', selected_user)
    user_id = user_id_match.group(1)

    chat_id = await dataBase.request.get_chat_id(user_id)
    user_chat_id.add(chat_id)

    # Отправляем сообщение пользователю о выборе
    await msg.answer(f"Вы отправили файл: {selected_user}", reply_markup=main_keyboard)


@router.message(content_types=types.ContentType.PHOTO)
async def handler_send_photo(msg: Message, bot: Bot):
