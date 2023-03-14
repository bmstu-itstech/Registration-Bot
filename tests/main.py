from constructor import writer


def test():
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
            "asnwers": None
        }
    }

    writer.create_tree(data, 23178)
    writer.read_tree(23178)


if __name__ == "__main__":
    test()
