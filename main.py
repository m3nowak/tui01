import sys

import argparse

from common import load_json
from tui_gen.models import parse_raw_course_dict
from tui_gen.gen_alg import genetic_algorithm


def main():
    #parser = argparse.ArgumentParser(description="PWR scheduling using genetic algorithm")
    #parser.add_argument('problem', help="JSON file of problem")

    #args = parser.parse_args()
    input_filepath = './artifacts/art15.json'
    raw_dict = load_json(input_filepath)
    prepared_dict = parse_raw_course_dict(raw_dict)
    alg_gen_report = genetic_algorithm(prepared_dict, 250, 0.7, 0.1, 20, raw_dict.get("scoring", {}))
    print(alg_gen_report.printable_summary())


if __name__ == "__main__":
    main()
