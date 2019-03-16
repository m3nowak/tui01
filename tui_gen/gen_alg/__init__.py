"""
Module containing genetic algorithm logic.
"""
from random import choice as rand_choice

def create_random_chromosome(problem_dict):
    """
    Create random chomosome.
    :param dict problem_dict: problem dictionary
    :param dict chromosome: randomly created chomosome
    """
    return {
        course_name: rand_choice(group_list) for course_name, group_list in problem_dict.items()
    }
