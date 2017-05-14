import math

import numpy as np

np.random.seed(5113)

"""
 Particle class that is used in PSO and is part of the swarm.
 Has its own velocity, position, personal best position and its corresponding velocity
"""


class Particle(object):

    def __init__(self, my_prng, dimensions):
        self.dimensions = dimensions
        self.position = np.random.uniform(-500, 500, dimensions)
        self.velocity = np.random.uniform(-1, 1, dimensions)
        self.pbest = self.position[:]
        self.pbest_val = self.evaluate(self.pbest)
        self.maximum_velocity = 50
        # print("Initial Position {}".format(self.position))
        # print("Initial Velocity {}".format(self.velocity))

    @staticmethod
    def evaluate(x):
        val = 0
        d = len(x)
        for i in range(d):
            val += x[i] * math.sin(math.sqrt(abs(x[i])))
        val = 418.9829 * d - val
        return val

    def update_velocity(self, gbest, ac1, ac2, inertia_weight):
        """
        :param gbest: neighborhood best if topology used else global best
        :param ac1: Acceleration constant for component 1
        :param ac2: Acceleartion constant for component 2
        :param inertia_weight: Inertia weight that is set and passed from Swarm object
        :return: Updates the velocity and the position of the particle
        """
        # Update velocity equation
        new_velocity = inertia_weight * self.velocity + ac1 * np.random.rand() * (
                self.pbest - self.position) + ac2 * np.random.rand() * (gbest - self.position)

        # If the velocity is outside feasible region we replace it with the maximum velocity defined
        mask = (new_velocity > self.maximum_velocity)
        new_velocity[mask] = self.maximum_velocity
        mask = (new_velocity < -self.maximum_velocity)
        new_velocity[mask] = -self.maximum_velocity

        new_position = self.position + new_velocity

        # only allowing feasible solution for the particless
        if np.all((new_position > -500) & (new_position < 500)):
            self.position = new_position
            self.velocity = new_velocity
            if self.evaluate(self.position) < self.pbest_val:
                self.pbest = self.position
                self.pbest_val = self.evaluate(self.position)
        else:
            # Handling infeasibility
            self.position = np.random.uniform(-500, 500, self.dimensions)

            # print("Updated Velocity {}".format(self.velocity))
            # print("Updated Position {}".format(self.position))




