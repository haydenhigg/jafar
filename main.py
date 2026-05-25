from jafar import Jafar
from farkle import Farkle
from statistics import mean
from json import load, dump

NUM_EPOCHS = 100_000
MAX_TURNS = 100

# without one-hot in `reroll`: 605 ppt | P1 54.7% win | P2 45.3% win
# with one-hot in `reroll`:    613 ppt | P1 52.5% win | P2 47.5% win
# with A2C:                    617 ppt | P1 52.6% win | P2 47.4% win
score_to_beat = 610
players = [
    {
        'reroll': Jafar(9, lr=6e-2),
        'bank': Jafar(15, lr=6e-2)
    },
    {
        'reroll': Jafar(9, lr=6e-2),
        'bank': Jafar(15, lr=6e-2)
    }
]

pts_per_game = []
winners = []

for epoch in range(NUM_EPOCHS):
    game = Farkle()
    num_turns = 0

    while game.winner is None and num_turns < MAX_TURNS:
        if epoch == 99_999:
            print(f'Player 1: {game.scores[0]} points | Player 2: {game.scores[1]} points')

        turn_score = 0
        num_dice_remaining = game.NUM_DICE

        while turn_score == 0 or players[game.turn]['reroll'].act([
            (game.my_score - game.their_score) / game.WIN_SCORE,
            game.my_score / game.WIN_SCORE,
            game.their_score / game.WIN_SCORE,
            turn_score / game.WIN_SCORE,
            int(num_dice_remaining == 1),
            int(num_dice_remaining == 2),
            int(num_dice_remaining == 3),
            int(num_dice_remaining == 4),
            int(num_dice_remaining == 5)
        ]):
            scorers = Farkle.score(Farkle.roll(num_dice_remaining))
            if len(scorers) == 0:
                turn_score = 0
                break

            turn_score += scorers[0][0]
            num_dice_remaining -= len(scorers[0][1])

            if len(scorers) >= 2:
                for score, scored_dice in scorers[1:]:
                    num_scored_dice = len(scored_dice)
                    if players[game.turn]['bank'].act([
                        (game.my_score - game.their_score) / game.WIN_SCORE,
                        game.my_score / game.WIN_SCORE,
                        game.their_score / game.WIN_SCORE,
                        turn_score / game.WIN_SCORE,
                        score / num_scored_dice / game.WIN_SCORE,
                        int(num_scored_dice == 1),
                        int(num_scored_dice == 2),
                        int(num_scored_dice == 3),
                        int(num_scored_dice == 4),
                        int(num_scored_dice == 5),
                        int(num_dice_remaining == 1),
                        int(num_dice_remaining == 2),
                        int(num_dice_remaining == 3),
                        int(num_dice_remaining == 4),
                        int(num_dice_remaining == 5)
                    ]):
                        turn_score += score
                        num_dice_remaining -= len(scored_dice)
                    else:
                        if epoch == 99_999:
                            print(f'Player {game.turn + 1} refused to bank {scored_dice}')

            if num_dice_remaining == 0:
                num_dice_remaining = game.NUM_DICE

        game.finish_turn(turn_score)
        num_turns += 1

    rewards = [-1, -1]
    score_sum = sum(game.scores)
    if score_sum > 0:
        rewards[0] = (game.scores[0] - game.scores[1]) / score_sum
        rewards[1] = (game.scores[1] - game.scores[0]) / score_sum

    for i, r in enumerate(rewards):
        players[i]['reroll'].reward(r - epoch / NUM_EPOCHS)
        players[i]['bank'].reward(r - epoch / NUM_EPOCHS)

    winners.append(game.winner)
    pts_per_game.append(score_sum / num_turns)

    if epoch % 5000 == 0:
        print(f'{mean(pts_per_game[-5000:]):.0f} ppt | P1 {100 * (1 - mean(winners[-5000:])):.1f}% win | P2 {100 * mean(winners[-5000:]):.1f}% win')

score = mean(pts_per_game[-5000:])
if score > score_to_beat:
    print('\nNew score to beat:', score)
    with open('models.json', 'w') as f:
        dump(players, f, indent=4, default=lambda o: o.__dict__)
