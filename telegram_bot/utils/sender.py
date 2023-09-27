import emoji

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.client.bot import Bot

from telegram_bot.custom_types import Questionnaire, AnswerButton
from micro_services.ApiGateWay import bot_client


async def send_question(state: FSMContext, chat_id: int, bot_id: int, bot: Bot) -> None:
    """
    Функция отправляет следующий вопрос пользователю.

    """

    # Получим данные стейта
    data = await state.get_data()
    # Получим модуль из микросервиса БД
    module = await bot_client.get_question(bot_id, data['question_id'])
    keyboard = InlineKeyboardBuilder()

    if len(module.buttons) > 0:
        for element in module.buttons:
            keyboard.button(callback_data=AnswerButton(answer=str(element.answer),
                                                       next_id=element.next_id).pack(),
                            text=str(element.answer))

    # Если уже был пройден хотя бы один вопрос, добавим кнопку "Назад"
    if len(data['prev_questions']) > 0 and await state.get_state() != Questionnaire.on_approval:
        keyboard.button(callback_data='get_back', text=emoji.emojize(":reverse_button: Назад"))

    keyboard.adjust(1)
    message = await bot.send_message(chat_id, module.question, reply_markup=keyboard.as_markup())
    user_status = await state.get_state()
    if user_status != Questionnaire.on_approval:
        # Поставим стейт о прохождении человеком опроса
        await state.set_state(Questionnaire.in_process)
    await state.update_data(question_id=data['question_id'], prev_message_id=message.message_id)
