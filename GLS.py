import math
from random import Random

import numpy as np

my = Random(4123)
dimensions = 200
penalty = np.zeros(dimensions)
penalty_factor = 5
np.random.seed(5113)
cost = np.ones(dimensions)

a = np.array((range(dimensions)))
feature_vector = np.zeros(dimensions)
x = np.random.uniform(-500, 500, dimensions)


def evaluate(x):
    val = 0
    d = len(x)
    for i in range(d):
        val += x[i] * math.sin(math.sqrt(abs(x[i])))
    val = 418.9829 * d - val
    return val


def indicator_set(x):
    """
    Indicator function that compares x with the feature vector and sets the value to 1 if there is a match
    :param x: The solution to be compared with the feature vector
    :return: A Indicator vector with 1 if there is a match with the feature vector else 0
    """
    global feature_vector
    mask = x == feature_vector
    indicator = np.zeros(dimensions)
    indicator[mask] = 1
    return indicator


def penalty_set(x):
    """
    Penalty set that takes in the feature vector and increments the penalty of a feature if its
    occuring recurringly
    :param x: Local minima
    :return: Update the penalty
    """
    global penalty
    mask = x == feature_vector
    indicator = np.zeros(dimensions)
    indicator[mask] = 1
    for i, v in enumerate(indicator):
        if v == 1:
            penalty[i] += 1
    local_penalty = np.array([penalty])
    local_penalty = local_penalty.T
    return local_penalty


def extended_eval(x):
    """
    Extended evaluation function that adds penalty to the default evaluation function
    :param x: Solution ro calculate the evaluation for
    :return: Value of the extended evaluation function
    """
    return evaluate(x) + penalty_factor * temp(indicator_set(x), penalty_set(x))


def temp(i1, i2):
    c = np.dot(i1, i2)
    return int(c)


def nbhood(x, n, v):
    """
    Return the nbhood list. For random number of bits random number of elements are chosen and a constant value v is
    added and removed from it.
    :param x: Solution for which we need to calculate the nbhood.
    :param v: A constant value to be added
    :return: Returns a list of values
    """
    main_list = list()
    temp_list = list()
    for i in range(n):
        temp_list.append(my.sample(range(dimensions), my.randint(1, dimensions / 2 - 1)))
    for j in temp_list:
        temp = list(x)
        for k in j:
            temp[k] += v
        main_list.append(temp)
        temp = list(x)
        for l in j:
            temp[l] -= v
        main_list.append(temp)
    return main_list


def feature_find(x, split):
    """
    That splits the data and assigns them to their respective bins
    :param x: Input Solution
    :param split: Bin size
    :return: Assigns and return the solution to a bin
    """
    bins = np.array(range(-500, 500, split))
    x = np.array(x)
    return np.digitize(x, bins)


def utility(current, value):
    global feature_vector
    feature_vector = feature_find(current, value)


current = x[:]
best = x[:]
best_sol = evaluate(best)
best_extended_sol = extended_eval(best)

solutions_checked = 0
done = 0
while done == 0:
    s_star = current
    split = 10
    value = 10
    if solutions_checked > 200:
        split = 0.5
        value = 0.5
    Neighborhood = nbhood(current, 2000, split)
    for i in Neighborhood:
        i = np.array(i)
        if extended_eval(i) < best_extended_sol:
            s_star = i[:]
            best_extended_sol = extended_eval(s_star)
    if extended_eval(s_star) < extended_eval(current):
        current = s_star
        if evaluate(current) < evaluate(best):
            best = current
    else:
        utility(current, value)
    solutions_checked += 1
    print(evaluate(best))

    if solutions_checked == 100000:
        done = 1

    if solutions_checked % 100 == 0:
        print("Solutions checked {} ".format(solutions_checked))
