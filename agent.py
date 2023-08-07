from car import Car
from network import Network
import numpy as np

class Agent:
    CHECKPOINT_REWARD = 1000
    TIME_REWARD = -1
    COMPLETION_REWARD = 5000
    FAIL_REWARD = -50

    def __init__(self, track_mask, checkpoints, car_x, car_y, car_heading=0):
        self.track_mask = track_mask
        self.checkpoints = checkpoints
        self.checkpoint_index = 0
        self.car = Car(car_x, car_y, heading=car_heading)
        self.network = Network(13, Car.N_ACTIONS)
        self.fitness = 0
        self.failed = False
        self.completed = False

    # called every frame
    def step(self, draw=False, screen=None):
        if not self.completed and not self.failed:
            observation = self.car.sensor(self.track_mask)
            action = self.network.process(observation)
            self.car.take_action(action)
            self.fitness += Agent.TIME_REWARD
            if self.car.collide(self.track_mask):
                self.fitness += Agent.FAIL_REWARD
                self.failed = True
            if self.car.checkpoint_collision(self.checkpoints[self.checkpoint_index]):
                self.fitness += Agent.CHECKPOINT_REWARD
                self.checkpoint_index += 1
                if self.checkpoint_index >= len(self.checkpoints):
                    self.completed = True
                    self.fitness += Agent.COMPLETION_REWARD
        if draw and screen:
            self.car.draw(screen)

    # create new set of agents for the next generation
    def offspring(self, start_x, start_y, start_heading):
        new_agent = Agent(self.track_mask, self.checkpoints, start_x, start_y, start_heading)
        new_weights = np.random.default_rng().normal(self.network.network, 0.1, self.network.network.shape)
        new_agent.network.set_weights(new_weights=new_weights)
        return new_agent

# creates new agents
def create_offspring(agents, start_x, start_y, start_heading):
    weights = []
    for agent in agents:
        weights.append(agent.fitness if agent.fitness >= 0 else 0)
    weight_sum = sum(weights)
    print(weights)

    probs = []
    for weight in weights:
        probs.append(weight / weight_sum)

    samples = np.random.choice(agents, len(agents), replace=True, p=probs)

    offspring = []
    for sample in samples:
        offspring.append(sample.offspring(start_x, start_y, start_heading))

    return offspring
