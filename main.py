import sys

from common import load_json
from tui_gen.models import parse_raw_course_dict
from tui_gen.gen_alg.rating import rate_chromosome
from tui_gen import gen_alg

def main():
    input_filepath = sys.argv[1]
    raw_dict = load_json(input_filepath)
    prepared_dict = parse_raw_course_dict(raw_dict)
    chromosome = gen_alg.create_random_chromosome(prepared_dict)
    rate_chromosome(chromosome, raw_dict.get("scoring", {}))


if __name__ == "__main__":
    main()
