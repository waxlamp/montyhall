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

    def react(self, result):
        pass


class Bob(object):
    def choose_door(self):
        return 0

    def choose_again(self, revealed):
        return (doors - ({0} | {revealed})).pop()

    def react(self, result):
        pass


class Carol(object):
    def __init__(self, seed):
        self.random = Random(seed)

    def choose_door(self):
        return self.random.choice(list(doors))

    def choose_again(self, revealed):
        return self.random.choice(list(doors - {revealed}))

    def react(self, result):
        pass


class Dave(object):
    def __init__(self, seed):
        self.random = Random(seed)

    def choose_door(self):
        self.choice = self.random.choice(list(doors))
        return self.choice

    def choose_again(self, revealed):
        return self.choice

    def react(self, result):
        pass


class Erin(object):
    def __init__(self, seed):
        self.random = Random(seed)

    def choose_door(self):
        self.choice = self.random.choice(list(doors))
        return self.choice

    def choose_again(self, revealed):
        return (doors - ({revealed} | {self.choice})).pop()

    def react(self, result):
        pass


class Frank(object):
    def choose_door(self):
        return 0

    def choose_again(self, revealed):
        return 1 if revealed != 1 else 0

    def react(self, result):
        pass


class Gina(object):
    def __init__(self):
        self.alice = Alice()
        self.bob = Bob()
        self.me = self.alice

    def switch(self):
        if self.me is self.alice:
            self.me = self.bob
        else:
            self.me = self.alice

    def react(self, result):
        if not result:
            self.switch()

    def choose_door(self):
        return self.me.choose_door()

    def choose_again(self, revealed):
        return self.me.choose_again(revealed)


def game_show(m, c):
    # Step 1
    m.hide_prize()

    # Step 2
    choice = c.choose_door()

    # Step 3
    revealed = m.reveal_empty_door(choice)

    # Step 4
    choice = c.choose_again(revealed)

    # Step 4.5
    c.react(choice == m.prize)

    # Step 5
    return choice == m.prize



if __name__ == "__main__":
    m = Monty(0)
    a = Alice()
    b = Bob()
    c = Carol(1)
    d = Dave(2)
    e = Erin(3)
    f = Frank()
    g = Gina()

    results = {
        "alice": 0,
        "bob": 0,
        "carol": 0,
        "dave": 0,
        "erin": 0,
        "frank": 0,
        "gina": 0,
    }

    contestants = [
        (a, "alice"),
        (b, "bob"),
        (c, "carol"),
        (d, "dave"),
        (e, "erin"),
        (f, "frank"),
        (g, "gina"),
    ]

    for c, name in contestants:
        for _ in range(10000):
            results[name] += game_show(m, c)

    for k in results:
        results[k] /= 10000.0

    pprint.pprint(results)
