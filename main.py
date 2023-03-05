from constructor import writer


def test():
    data = [
        [
            1,
            [2],
            "What is your name?",
            None
        ],
        [
            2,
            [3, 4],
            "r u gay?",
            ["yes", "no"]
        ],
        [
            3,
            [5],
            "why r u gay?",
            None
        ],
        [
            4,
            [5],
            "how do u feel about gays?",
            None
        ],
        [
            5,
            [],
            "rate us pls",
            None
        ]
    ]

    writer.create_tree(data, 23178)
    writer.read_tree(23178)


if __name__ == "__main__":
    test()
