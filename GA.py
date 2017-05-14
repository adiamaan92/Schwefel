import math
from random import Random
import numpy as np

seed = 5113
my_prng = Random(seed)

dimensions = 200
lowerBound = -500
upperBound = 500

population_size = 1000
Generations = 10000

crossover_rate = 0.8
mutation_rate = 0.15
elitism_rate = 0.20


def create_chromosome(d, l_bound, u_bound):
    """
    :param d: Number of chromosomes
    :param l_bound: Lower bound -500
    :param u_bound: Upper bound +500
    :return: returns a randomly initiated chromosome
    """
    x = []
    for i in range(d):
        x.append(my_prng.uniform(l_bound, u_bound))
    return x


# function to evaluate the Schwefel Function for d dimensions
def evaluate(x):
    val = 0
    d = len(x)
    for i in range(d):
        val += x[i] * math.sin(math.sqrt(abs(x[i])))
    val = 418.9829 * d - val
    return val


def initialize_population():
    """
    Creates a list of randomly initiated chromosomes. Returns a list containing the solutions and the
    Evaluation of these solution sorted based on the evaluation value
    :return: A list of list containing chromosomes and its evaluations
    """
    population = []
    population_fitness = []
    for i in range(population_size):
        population.append(create_chromosome(dimensions, lowerBound, upperBound))
        population_fitness.append(evaluate(population[i]))
    temp_zip = zip(population, population_fitness)
    pop_vals = sorted(temp_zip, key=lambda temp_zip: temp_zip[1])
    return pop_vals


def crossover(x1, x2):
    """
    A random cross over point is selected and a cross over is done by combining the data before and after this
    Cross over point for the two parents
    :param x1: Parent 1
    :param x2: Parent 2
    :return: Offsprings obtained by doing a crossover on the parents
    """
    d = len(x1)
    cross_over_pt = my_prng.randint(1, d - 1)
    beta = 0.05
    new1 = list(np.array(x1) - beta * (np.array(x1) - np.array(x2)))
    new2 = list(np.array(x2) + beta * (np.array(x1) - np.array(x2)))
    if cross_over_pt > d / 2:
        offspring1 = x1[0:cross_over_pt] + new2[cross_over_pt:d]  # note the "+" operator concatenates lists
        offspring2 = x2[0:cross_over_pt] + new1[cross_over_pt:d]
    else:
        offspring1 = new2[0:cross_over_pt] + x1[cross_over_pt:d]
        offspring2 = new1[0:cross_over_pt] + x2[cross_over_pt:d]
    return offspring1, offspring2


def rank_order(any_list):
    """
    :param any_list: The list to be scaled
    :return: Return the scales list
    """
    rank_ordered = [0] * len(any_list)
    for i, x in enumerate(sorted(range(len(any_list)), key=lambda y: any_list[y])):
        rank_ordered[x] = i
    return rank_ordered


def tournament_selection(pop, k):
    """
    :param pop: Population from which k elements need to be selected
    :param k: K is the number of elements to be selected
    :return: mating pool
    """
    mating_pool = []
    while len(mating_pool) < population_size:
        ids = [my_prng.randint(0, population_size - 1) for i in range(k)]
        competing_individuals = [pop[i][1] for i in ids]
        best_id = ids[competing_individuals.index(min(competing_individuals))]
        mating_pool.append(pop[best_id][0])
    return mating_pool


# TODO do some kind of mutation on the children
def mutate(x):
    """
    Randomnly pick a element and replace it with a random value
    :param x: the chromosome to be mutated
    :return: the mutated chromosome
    """
    if my_prng.random() < mutation_rate:
        #no_transactions, 0, -1
        for i in range(1):
            temp = my_prng.randint(0, len(x)-1)
            x[temp] = my_prng.uniform(-500, 500)
    return x


def breeding(mating_pool):
    """
    Takes in the mating pool perform crossover and calculates its fitness and returns the sorted list
    :param mating_pool: Mating pool for breeding
    :return: Sorted population
    """
    children = []
    children_fitness = []
    for i in range(0, population_size - 1, 2):
        child1, child2 = crossover(mating_pool[i], mating_pool[i + 1])
        child1 = mutate(child1)
        child2 = mutate(child2)
        children.append(child1)
        children.append(child2)
        children_fitness.append(evaluate(child1))
        children_fitness.append(evaluate(child2))
    temp_zip = zip(children, children_fitness)
    pop_vals = sorted(temp_zip, key=lambda temp_zip: temp_zip[1])
    return pop_vals


# insertion step
def insert(pop, kids):
    """
    :param pop: Population from the previous generation sorted
    :param kids: Current Generation best solutions sorted
    :return: Elite population
    """
    elite = int(elitism_rate*population_size)
    elite_sol = pop[0:elite+1]
    return elite_sol + kids[0:population_size-elite+1]


def summary_fitness(pop):
    """
    Summary function of the population
    :param pop: Population
    :return: Min, mean and variance of the population
    """
    a = np.array(list(zip(*pop))[1])
    return np.min(a), np.mean(a), np.var(a)


# the best solution should always be the first element... if I coded everything correctly...
def best_solution(pop):
    print(pop[0])


with open('out.txt', 'w') as f:
    Population = initialize_population()
    for j in range(Generations):
        mates = tournament_selection(Population, 3)
        Offspring = breeding(mates)
        Population = insert(Population, Offspring)
        min_val, mean_val, var_val = summary_fitness(Population)
        f.write(str(min_val) + " " + str(mean_val) + " " + str(var_val) + "\n")
        print("Breeded {} generation".format(j))
        print("Min value {}".format(min_val))


print(summary_fitness(Population))
best_solution(Population)
