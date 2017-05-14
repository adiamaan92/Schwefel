from Swarm import Swarm
from random import Random

seed = 5113
my_prng = Random(seed)
dimensions = 2
swarm_size = 100

swarm = Swarm(swarm_size, my_prng, dimensions)
swarm.create_ring()

for i in range(10000):
    print("---- Round {} ----".format(i))
    swarm.roam(i)
    swarm.update_inertia()
    print(swarm.gbest_val)
print("Global best {}".format(swarm.gbest))

