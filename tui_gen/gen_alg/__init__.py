"""
Module containing genetic algorithm logic.
"""
from copy import copy
import math
from random import choice as rand_choice, randrange, random, choices as rand_choices, sample
from datetime import datetime

import numpy as np

from tui_gen.gen_alg.rating import rate_population
from tui_gen.gen_alg.genetic_algorithm_report import GeneticAlgorithmReport


def tournament_selection(population, population_rating, tour_size=3):
    """
    Perform tournament selection.
    :param list population: population to perform selection on
    :param list population_rating: rating of population members
    """
    survived_population = []
    population_rating_np = np.array(population_rating)
    for _ in population:
        chosen_indicies = sample(range(len(population)), k=tour_size)
        index_of_chosen_indicies = np.argmax(population_rating_np[chosen_indicies])
        pop_index_chosen = chosen_indicies[index_of_chosen_indicies]
        survived_population.append(population[pop_index_chosen])
    return survived_population


def logistic(population_rating):
    """
    Calculate sigmoid for population ratings.
    :param list population_rating: rating of population members
    :returns list: rayings with sigmoid applied
    """
    np_population_rating = np.array(population_rating)
    np_population_rating_softplus = np.log(1/(1 + np.exp(np_population_rating*-1)))
    scores_softplus = np_population_rating_softplus.tolist()
    return scores_softplus


def softplus(population_rating):
    """
    Calculate softplus for population ratings.
    :param list population_rating: rating of population members
    :returns list: rayings with softlus applied
    """
    np_population_rating = np.array(population_rating)
    np_population_rating_softplus = np.log(1 + np.exp(np_population_rating))
    scores_softplus = np_population_rating_softplus.tolist()
    return scores_softplus


def roulette_selection(population, population_rating, activation_func=softplus):
    """
    Perform roulette selection.
    :param list population: population to perform selection on
    :param list population_rating: rating of population members
    :param function activation_func: activation function
    :returns list: selected chromosomes
    """
    return rand_choices(population, weights=activation_func(population_rating), k=len(population))


def chromosome_mutation(chromo, problem_dict):
    """
    Perform mutation on chromosome.
    :param dict chromo: chromosome to perform mutation on
    :return dict: mutated chromosome
    """
    key_list = list(problem_dict.keys())
    selected_key = rand_choice(key_list)
    mutated_chromo = copy(chromo)
    mutated_chromo[selected_key] = rand_choice(problem_dict[selected_key])
    return mutated_chromo


def population_mutation(population, problem_dict, probability):
    """
    Perform mutation on population.
    :param list population: population to perform mutation on
    :param dict problem_dict: problem dictionary
    :param int probability: mutation probability
    :return list: population after mutation
    """
    mutated_population = []
    for chromo in population:
        if random() <= probability:
            chromo = chromosome_mutation(chromo, problem_dict)
        mutated_population.append(chromo)
    return mutated_population


def chromosomes_crossover(chromo_0, chromo_1):
    """
    Perform crossover on two chromosomes.
    :param dict chromo_0: first chromosome to perform crossover on
    :param dict chromo_1: second chromosome to perform crossover on
    :return tuple: crossed chromosome pair
    """
    crossd_chromo_0 = {}
    crossd_chromo_1 = {}

    for key in chromo_0.keys():
        if randrange(2):
            crossd_chromo_0[key] = chromo_0[key]
            crossd_chromo_1[key] = chromo_1[key]
        else:
            crossd_chromo_0[key] = chromo_1[key]
            crossd_chromo_1[key] = chromo_0[key]
    return crossd_chromo_0, crossd_chromo_1


def population_crossover(population, probability):
    """
    Perform crossover on population.
    :param list population: population to perform crossover on
    :param int probability: crosspover probability
    :return list: population after crossover
    """
    og_population = copy(population)
    crossoverd_population = []
    while len(og_population) >= 2:
        chromo_0 = og_population.pop(randrange(len(og_population)))
        chromo_1 = og_population.pop(randrange(len(og_population)))
        if random() <= probability:
            chromo_0, chromo_1 = chromosomes_crossover(chromo_0, chromo_1)
        crossoverd_population.append(chromo_0)
        crossoverd_population.append(chromo_1)
    if og_population:
        crossoverd_population.append(og_population[0])
    return crossoverd_population


def create_random_chromosome(problem_dict):
    """
    Create random chomosome.
    :param dict problem_dict: problem dictionary
    :returns dict: randomly created chomosome
    """
    return {
        course_name: rand_choice(group_list) for course_name, group_list in problem_dict.items()
    }


def create_population(problem_dict, size):
    """
    Create random population.
    :param dict problem_dict: problem dictionary
    :param int size: population size
    :returns list: randomly created chomosomes
    """
    return [create_random_chromosome(problem_dict) for _ in range(size)]


def genetic_algorithm(problem_dict, pop_size, crossover_prob,
                      mutation_prob, stale_limit, scoring_values, verbose=True):
    """
    Run genetic algorithm.
    :param dict problem_dict: problem dictionary
    :param int pop_size: population size
    :param float crossover_prob: crossover probability
    :param float mutation_prob: mutation probability
    :param int stale_limit: max number of stale generations (termination condition)
    :param dict scoring_values: dictionary of scoring values
    :param bool verbose: whether print info during execution
    :returns GeneticAlgorithmReport: final report
    """
    population = create_population(problem_dict, pop_size)
    best_score = - math.inf
    best_score_stale_for = 0  # for how many gens. best score is the same
    best_chromo = population[0]
    generation_count = 0
    time_start = datetime.now()
    while best_score_stale_for < stale_limit:
        generation_count += 1

        population = population_crossover(population, crossover_prob)
        population = population_mutation(population, problem_dict, mutation_prob)
        population_rating = rate_population(population, scoring_values)
        gen_best_index = np.argmax(population_rating)
        gen_best_score = population_rating[gen_best_index]

        if gen_best_score > best_score:
            best_score_stale_for = 0
            best_score = gen_best_score
            best_chromo = population[gen_best_index]
        else:
            best_score_stale_for += 1
        if verbose:
            print("Best score for generation {}: {}".format(generation_count, gen_best_score))
        #population = roulette_selection(population, population_rating, logistic)
        population = tournament_selection(population, population_rating)
    time_end = datetime.now()
    return GeneticAlgorithmReport(best_chromo, best_score, generation_count, time_end-time_start)
