from operator import attrgetter

from Particle import Particle
import numpy as np

"""
Swarm object that holds the list of particles.
Also sets the acceleration constant 1 and 2 and also the inertia weight
"""

class Swarm(object):
    def __init__(self, n, my_prng, dimensions):
        self.my_prng = my_prng
        self.no_of_particles = n
        self.dimensions = dimensions
        self.particle_list = np.array(self.create_particles())
        self.gbest_val, self.gbest = self.calculate_gbest()
        self.ac1 = 2
        self.ac2 = 2
        self.inertia_weight = 2
        self.nbhood = list()
        self.nbhood_eval = list()

    def create_particles(self):
        """
        :return: Creates a list of particles and returns them
        """
        particle_list = list()
        for i in range(self.no_of_particles):
            particle_list.append(Particle(self.my_prng, self.dimensions))
        return particle_list

    def create_ring(self):
        """
        Creates the Ring Neighborhood. This function just generates the index of
        particles that should be part of the same neighborhood. This is called only once
        """
        self.nbhood.append([0, self.no_of_particles-1, 1])
        i, j, k = 1, 0, 2
        for o in range(self.no_of_particles-2):
            self.nbhood.append([i, j, k])
            i += 1
            j += 1
            k += 1
        self.nbhood.append([self.no_of_particles-1, self.no_of_particles - 2, 0])
        print(self.nbhood)

    def calculate_gbest(self):
        """
        :return: Particle object having the minimum pbest value
        """
        best_particle = min(self.particle_list, key=attrgetter('pbest_val'))
        return best_particle.pbest_val, best_particle.pbest

    def calculate_mod_gbest(self):
        """
        Similar to the calculate_gbest function but only considers the Neighbourhood of a particle
        """
        self.nbhood_eval = list()
        for i in self.nbhood:
            temp_list = list()
            temp_list.extend((self.particle_list[i[0]], self.particle_list[i[1]], self.particle_list[i[2]]))
            temp_particle = min(temp_list, key=attrgetter('pbest_val'))
            self.nbhood_eval.append(temp_particle)

    def roam(self, j):
        """
        Calls update velocity function for all the elements in the particle list
        :return:
        """
        self.calculate_mod_gbest()
        for i, p in enumerate(self.particle_list):
            p.update_velocity(self.gbest, self.ac1, self.ac2, self.inertia_weight)
        self.gbest_val, self.gbest = self.calculate_gbest()

    def update_inertia(self):
        return self.inertia_weight
