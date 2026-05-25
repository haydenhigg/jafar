# jafar

- Agent only has 1 choice -- continue rolling or not
- Compared to a dummy agent that always continues if `score < 300` or `score < 500`, it wins handily
- Scores around 555-560 points per turn on average which is pretty strong
- The harder problem is choosing what not to bank to be able to score more
- Could use multiple actions (multinomial) for banking but simpler to reduce it to Bernoulli
- Agent struggled to learn to beat a "bank everything" dummy agent
- Used one-hot encodings for remaining dice and it dramatically changed (was using `num_dice_remaining / game.NUM_DICE`)
- Scores around 590-600 points per turn which is as good as me (~593 per turn)
- Used one-hot encodings for remaining dice in reroll action too
- Scores around 605-610 points per turn which is better than me
- Training runs became more consistent with log reward
- Peak runs were dependent on P1 learning how to exploit going first
    512 ppt | P1 51.7% win | P2 48.3% win
    559 ppt | P1 47.5% win | P2 52.5% win
    571 ppt | P1 44.9% win | P2 55.1% win
    577 ppt | P1 46.3% win | P2 53.7% win
    575 ppt | P1 44.3% win | P2 55.7% win
    581 ppt | P1 44.6% win | P2 55.4% win
    580 ppt | P1 45.3% win | P2 54.7% win
    583 ppt | P1 46.4% win | P2 53.6% win
    <Huge jump when P1 figures out how to win>
    601 ppt | P1 52.0% win | P2 48.0% win
    603 ppt | P1 52.4% win | P2 47.6% win
    601 ppt | P1 51.6% win | P2 48.4% win
    603 ppt | P1 54.1% win | P2 45.9% win
    604 ppt | P1 52.5% win | P2 47.5% win
    605 ppt | P1 53.5% win | P2 46.5% win
    602 ppt | P1 53.3% win | P2 46.7% win
    603 ppt | P1 52.1% win | P2 47.9% win
    607 ppt | P1 54.5% win | P2 45.5% win
    609 ppt | P1 53.1% win | P2 46.9% win
    604 ppt | P1 53.1% win | P2 46.9% win
