import pprint
from random import Random

doors = {0, 1, 2}


class Monty(object):
    def __init__(self, seed):
        self.random = Random(seed)
        self.prize = None

    def hide_prize(self):
        self.prize = self.random.choice(list(doors))

    def reveal_empty_door(self, chosen):
        return self.random.choice(list(doors - ({chosen} | {self.prize})))


class Alice(object):
    def choose_door(self):
        return 0

    def choose_again(self, revealed):
        return 0


class Bob(object):
    def choose_door(self):
        return 0

    def choose_again(self, revealed):
        return (doors - ({0} | {revealed})).pop()


def game_show(m, c):
    # Step 1
    m.hide_prize()

    # Step 2
    choice = c.choose_door()

    # Step 3
    revealed = m.reveal_empty_door(choice)

    # Step 4
    choice = c.choose_again(revealed)

    # Step 5
    return choice == m.prize


if __name__ == "__main__":
    m = Monty(0)
    a = Alice()
    b = Bob()

    results = {
        "alice": 0,
        "bob": 0,
    }

    for c, slot in [(a, "alice"), (b, "bob")]:
        for _ in range(1000):
            results[slot] += game_show(m, c)

    for k in results:
        results[k] /= 1000.0

    pprint.pprint(results)
