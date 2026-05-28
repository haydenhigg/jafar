# jafar

- A2C RL with simple binary linear models play Farkle superhumanly (615 points-per-turn)
- One-hot encoding of values like dice-remaining is critical
- Peak training runs are dependent on P1 learning how to exploit going first
- Time-discounting is surprisingly crucial to get right as well (TD is somewhat less fickle about gamma)
- Learning rates have to be surprisingly high
- There are proximate/dense rewards that I could apply rather than just the episodic/sparse reward, but I couldn't get better performance with that
