from random import randint

def count(xs: list[int]) -> dict[int, int]:
    counts = {}

    for x in xs:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1

    return counts

def repeat(x: int, times: int) -> list[int]:
    return [x] * times

class Farkle:
    NUM_DICE = 6
    WIN_SCORE = 10_000

    def roll(n: int) -> list[int]:
        return [randint(1, 6) for _ in range(n)]

    def score(dice: list[int]) -> list[tuple[int, int]]:
        counts = count(dice)
        items = sorted(counts.items(), key=lambda item: item[1], reverse=True)

        if len(dice) == 6:
            if items[0][1] == 6:
                return [(3000, repeat(*items[0]))]
            elif len(items) >= 2 and items[0][1] == 3 and items[1][1] == 3:
                return [(2500, repeat(*items[0]) + repeat(*items[1]))]
            elif len(items) >= 2 and items[0][1] == 4 and items[1][1] == 2:
                return [(1500, repeat(*items[0]) + repeat(*items[1]))]
            elif len(items) >= 3 and items[0][1] == 2 and items[1][1] == 2 and items[2][1] == 2:
                return [(1500, repeat(*items[0]) + repeat(*items[1]) + repeat(*items[2]))]
            elif len(items) == 6 and all(item[1] == 1 for item in items):
                return [(1500, list(counts.keys()))]

        scorers = []
        offset = 1

        if items[0][1] == 5:
            score = 4000 if items[0][0] == 1 else 2000
            scorers.append((score, repeat(*items[0])))
        elif items[0][1] == 4:
            score = 2000 if items[0][0] == 1 else 1000
            scorers.append((score, repeat(*items[0])))
        elif items[0][1] == 3:
            score = 1000 if items[0][0] == 1 else items[0][0] * 100
            scorers.append((score, repeat(*items[0])))
        else:
            offset = 0

        for item in items[offset:]:
            if item[0] == 1:
                for _ in range(item[1]):
                    scorers.append((100, [item[0]]))
            elif item[0] == 5:
                for _ in range(item[1]):
                    scorers.append((50, [item[0]]))

        return sorted(scorers, key=lambda scorer: scorer[0] - len(scorer[1]), reverse=True)

    def __init__(self):
        self.scores = [0, 0]
        self.turn = 0

        self.last_turn = False
        self.winner = None

    @property
    def my_score(self) -> int:
        return self.scores[self.turn]

    @property
    def their_score(self) -> int:
        return self.scores[(self.turn + 1) % 2]

    def finish_turn(self, turn_score: int):
        self.scores[self.turn] += turn_score

        if self.last_turn:
            if self.scores[0] == self.scores[1]:
                self.last_turn = False
            else:
                self.winner = int(self.scores[0] < self.scores[1])
        elif self.scores[self.turn] >= Farkle.WIN_SCORE:
            self.last_turn = True

        self.turn = (self.turn + 1) % 2
