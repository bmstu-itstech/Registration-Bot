from .connector import connect_or_create

async def get_question(question_id: int, bot_id: int):
        conn = await connect_or_create('postgres', f'id{bot_id}')
        # Get module text from database
        module = await conn.fetchrow('SELECT * FROM modules WHERE id = $1',
                                     question_id)
        rows = await conn.fetch('SELECT (answer, next_id) FROM buttons '
                                'WHERE current_id = $1',
                                question_id)
        buttons = [row[0] for row in rows]
        await conn.close()
        return module, buttons
