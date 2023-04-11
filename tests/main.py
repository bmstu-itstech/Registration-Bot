from constructor import writer
from asker_bot import bot_instance, config
import asyncio

async def test():
    data = {

        1: {
            "links": [2],
            "question": "What is your name?",
            "answers": None
        },

        2: {
            "links": [3, 4],
            "question": "r u gay?",
            "answers": ["yes", "no"]
        },

        3: {
            "links": [5],
            "question": "why r u gay?",
            "answers": None
        },

        4: {
            "links": [5],
            "question": "how do u feel about gays?",
            "answers": None
        },

        5: {
            "links": [],
            "question": "rate us pls",
            "answers": None
        }
    }

    await writer.create_tree(data, 1)
    await bot_instance.run(config.bot_token, 1)


if __name__ == "__main__":
    asyncio.run(test())
