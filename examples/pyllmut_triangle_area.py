import logging
from pathlib import Path

from pyllmut import MutantGenerator, ModelType

logging.basicConfig(level=logging.INFO)

module_path = "./triangle_area/code/equilateral.py"

module_content = Path(module_path).read_text()
lines_to_mutate = [7, 10, 11]
mutants_per_line = 3
timeout_per_line = 15
model_type = ModelType.GPT4o

generator = MutantGenerator(
    module_content, lines_to_mutate, mutants_per_line, timeout_per_line, model_type
)
mutation_report = generator.generate()
valid_mutants = mutation_report.get_valid_mutant_list()

print(f"\n**Number of valid mutants**: {len(valid_mutants)}")

if valid_mutants:
    first_mutant = valid_mutants[0]

    print("\nFirst Valid Mutant")
    print("=" * 20)
    print(f"**Line number**: {first_mutant.get_line_number()}")
    print("-" * 20)
    print("**Diff Content**:\n", first_mutant.get_diff_content())
    print("-" * 20)
    print("**Mutated Module Content**:\n", first_mutant.get_mutated_module_content())
    print("=" * 20)
