import emoji

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.bot import Bot
from aiogram.fsm.context import FSMContext

from typing import Optional

from ..custom_types import Questionnaire, QuestionButton
from micro_services.ApiGateWay import bot_client


async def finish_questionnaire(state: FSMContext, chat_id: int, bot_id: int, bot: Bot,
                               next_question_id: Optional[int] = None) -> None:
    user_status = await state.get_state()

    if user_status == Questionnaire.on_approval:
        # Get state data
        data = await state.get_data()
        # Get temp and new answers
        temp_answers = data['on_approval']
        new_answers = data['answers']
        answers = dict()

        for temp_id in temp_answers.keys():
            if temp_id == list(new_answers.keys())[0]:
                break
            answers[temp_id] = temp_answers[temp_id]

        for answer_id in new_answers.keys():
            answers[answer_id] = new_answers[answer_id]

        if next_question_id is not None:
            for temp_id in temp_answers.keys():
                if int(temp_id) >= next_question_id:
                    answers[temp_id] = temp_answers[temp_id]

        await state.update_data(answers=answers, on_approval=None)

    await state.set_state(Questionnaire.on_approval)

    # Build a keyboard
    keyboard = InlineKeyboardBuilder()
    keyboard.button(callback_data='questionnaire_over',
                    text=emoji.emojize('Отправить :check_mark_button:'))

    data = await state.get_data()
    # Get answers dict from the state data
    new_answers = data['answers']
    message = 'Ваши ответы:\n\n'

    for answer_id in new_answers.keys():
        message += emoji.emojize(':small_blue_diamond:')
        module = await bot_client.get_question(bot_id, int(answer_id))
        answer_text = new_answers[answer_id]
        message += f' {module.question}: {answer_text}\n'
        keyboard.button(callback_data=QuestionButton(question_id=answer_id).pack(),
                        text=module.question)
    message += '\nЕсли вы хотите что-то исправить - нажмите кнопку с нужным вопросом.\n' \
               'Если всё в порядке - нажмите кнопку "Отправить".'
    keyboard.adjust(1)
    await bot.send_message(chat_id, message, reply_markup=keyboard.as_markup())
