import logging
import sqlite3
import aiosqlite
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command, Text
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def run(TOKEN, BOT_ID) -> None:
    router = Router()

    @router.message(Command(commands=["start"]))
    async def command_start_handler(message: Message) -> None:
        """
        Этот хэндлер принимает команду /start и начинает опрос.

        :param message: Отправленное пользователем сообщение
        :return:
        """
        # Отправим сообщение о начале анкетирования
        await message.answer("Заполните анкету, чтобы зарегистрироваться на мероприятие!")
        async with aiosqlite.connect('./test.db') as connection:
            cursor = await connection.cursor()
            user_id = message.from_user.id

            try:
                sql = (
                    f"INSERT INTO id{BOT_ID}_answers (user_id) "
                    f"VALUES (?)"
                )
                await cursor.execute(sql, [user_id])
            except sqlite3.IntegrityError as error:
                logging.error(error)

            # Зададим id предыдущего вопроса как 0
            sql = (
                f"UPDATE id{BOT_ID}_answers SET prev_id = 0 "
                f"WHERE user_id = {user_id}"
            )
            await cursor.execute(sql)

            # Зададим id текущего вопроса как 1
            sql = (
                f"UPDATE id{BOT_ID}_answers SET now_id = 1 "
                f"WHERE user_id = {user_id}"
            )
            await cursor.execute(sql)

            # Подтвердим изменения
            await cursor.execute("COMMIT;")

            # Отправим первый вопрос в чат
            sql = (
                f"SELECT question_text FROM id{BOT_ID} "
                f"WHERE module_id = 1"
            )
            await cursor.execute(sql)
            question_text = (await cursor.fetchall())[0][0]
            await message.answer(question_text)

    @router.message()
    async def answer_handler(message: Message) -> None:
        """
        Этот хэндлер обрабатывает ответ пользователя на вопрос и
        выводит следующий вопрос.

        :param message: Отправленное пользователем сообщение
        :return:
        """
        async with aiosqlite.connect('./test.db') as connection:
            cursor = await connection.cursor()
            user_id = message.from_user.id
            answer_text = message.text

            # Получим id текущего вопроса
            sql = (
                f"SELECT now_id FROM id{BOT_ID}_answers "
                f"WHERE user_id = {user_id}"
            )
            await cursor.execute(sql)
            now_id = (await cursor.fetchall())[0][0]

            # Если пользователь уже проходил анкетирование
            if now_id is None:
                await message.answer("Вы уже заполнили анкету!")
            else:
                # Запишем ответ пользователя
                sql = (
                    f"UPDATE id{BOT_ID}_answers SET answer{now_id} = '{answer_text}' "
                    f"WHERE user_id = {user_id}"
                )
                await cursor.execute(sql)

                # Запишем в предыдущий id текущий id
                sql = (
                    f"UPDATE id{BOT_ID}_answers SET prev_id = prev_id || '/' || now_id "
                    f"WHERE user_id = {user_id}"
                )
                await cursor.execute(sql)

                # Найдем id следующего вопроса
                sql = (
                    f"SELECT next_ids FROM id{BOT_ID} "
                    f"WHERE module_id = {now_id}"
                )
                await cursor.execute(sql)
                next_ids = (await cursor.fetchall())[0][0]

                # Если следующего вопроса нет
                if next_ids is None:
                    sql = (
                        f"UPDATE id{BOT_ID}_answers SET now_id = NULL "
                        f"WHERE user_id = {user_id}"
                    )
                    await cursor.execute(sql)
                    await message.answer("Ответы записаны!")
                else:
                    next_ids.split("/")
                    next_id = next_ids[0]

                    sql = (
                        f"UPDATE id{BOT_ID}_answers SET now_id = {next_id} "
                        f"WHERE user_id = {user_id}"
                    )
                    await cursor.execute(sql)

                    sql = (
                        f"SELECT question_text FROM id{BOT_ID} "
                        f"WHERE module_id = {next_id}"
                    )
                    await cursor.execute(sql)
                    question_text = (await cursor.fetchall())[0][0]
                    await message.answer(question_text)

                await cursor.execute("COMMIT;")

    @router.callback_query(Text(startswith="answer_"))
    async def keyboard_handler(callback: CallbackQuery):
        pass

    async def main() -> None:
        dp = Dispatcher()
        dp.include_router(router)

        # Инициализация бота по переданному токену
        bot = Bot(token=TOKEN, parse_mode="HTML")
        await dp.start_polling(bot)

    async with aiosqlite.connect('./test.db') as connection:
        cursor = await connection.cursor()

        sql = (
            f"CREATE TABLE IF NOT EXISTS id{BOT_ID}_answers ("
            f"user_id INTEGER PRIMARY KEY,"
            f"prev_id INTEGER,"
            f"now_id INTEGER)"
        )
        await cursor.execute(sql)

        sql = (
            f"SELECT module_id FROM id{BOT_ID}"
        )
        await cursor.execute(sql)
        modules_ids = (await cursor.fetchall())

        for id in modules_ids:
            try:
                sql = (
                    f"ALTER TABLE id{BOT_ID}_answers "
                    f"ADD COLUMN answer{id[0]} VARCHAR(256);"
                )
                await cursor.execute(sql)
            except sqlite3.OperationalError as error:
                logging.error(error)

    logging.basicConfig(level=logging.INFO)
    # Запуск бота
    await main()
