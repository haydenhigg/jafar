from random import gauss, random
from math import exp

class LinearModel:
    def __init__(self, n: int = 1, learning_rate: float = 1e-3):
        self.n = n
        self.learning_rate = learning_rate

        self.weights = [self.__random() for _ in range(self.n)]
        self.bias = self.__random()

    def __random(self) -> float:
        return gauss(0, 1 / self.n)

    def feed(self, xs: list[float]) -> float:
        if len(xs) != self.n:
            raise ValueError('wrong number of inputs')

        return sum(w * x for w, x in zip(self.weights, xs)) + self.bias

    def step(self, factor: float, xs: list[float]):
        for i, x in enumerate(xs):
            self.weights[i] += self.learning_rate * factor * x

        self.bias += self.learning_rate * factor

# Encapsulates a logistic (Bernoulli) RL policy
class Jafar:
    def __init__(self, n: int = 1, lr: float = 1e-3, critic_lr: float = 1e-4):
        self.n = n

        self.actor = LinearModel(self.n, lr)
        self.critic = LinearModel(self.n, critic_lr)

        self.trajectory = []

    def __sigmoid(self, z: float) -> float:
        try:
            return 1 / (1 + exp(-z))
        except OverflowError:
            return 0 if z < 0 else 1

    def act(self, inputs: list[float]) -> bool:
        p = self.__sigmoid(self.actor.feed(inputs))
        action = int(random() < p)

        self.trajectory.append((inputs, action - p))

        return action

    def reward(self, r: float):
        for xs, error in self.trajectory:
            advantage = r - self.critic.feed(xs)

            self.actor.step(advantage * error, xs)
            self.critic.step(advantage, xs)

        self.trajectory = []
