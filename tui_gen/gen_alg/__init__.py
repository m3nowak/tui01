from random import choice as rand_choice

def create_random_chromosome(problem_dict):
    return {
        course_name: rand_choice(group_list) for course_name, group_list in problem_dict.items()
    }