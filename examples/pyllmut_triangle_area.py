from pathlib import Path

import logging
logging.basicConfig(level=logging.INFO)

from pyllmut import MutantGenerator

module_path = "./triangle_area/code/equilateral.py"

module_content = Path(module_path).read_text()
lines_to_mutate = [7, 10, 11]
mutants_per_line = 3

generator = MutantGenerator(
    module_content,
    lines_to_mutate,
    mutants_per_line
)
mutation_report = generator.generate()
valid_mutants = mutation_report.get_valid_mutant_list()

print("Number of valid mutants:", len(valid_mutants))

if len(valid_mutants) > 0:
    print("Line number:", valid_mutants[0].get_line_number())
    print("---------")
    print(valid_mutants[0].get_diff_content())
    print("---------")
    print(valid_mutants[0].get_mutated_module_content())
