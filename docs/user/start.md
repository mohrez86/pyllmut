# Quick Start

The [examples](https://github.com/mohrez86/pyllmut/tree/main/examples)
directory includes a simple example of using
PyLLMut. This page provides step-by-step instructions for
running this example.

## Example: Triangle Area

As shown in Figure 1,
*Triangle Area*, in the
[examples/triangle_area](https://github.com/mohrez86/pyllmut/tree/main/examples/triangle_area)
directory, is a simple project with two packages:
`code` and `tests`.
The `code` package contains the project’s source code,
which consists of two Python modules:
`equilateral.py` and `isosceles.py`,
which compute the area of equilateral and
isosceles triangles, respectively.
The `tests` package contains the project’s test suite,
including two test modules:
`test_equilateral.py` and `test_isosceles.py`,
which test the `equilateral.py` and `isosceles.py` modules,
respectively.

In this example, we use PyLLMut to generate
mutants for `equilateral.py`, shown in Figure 2.

``` title="Figure 1: Project structure of Triangle Area."
triangle_area/
├── code/
│   ├── __init__.py
│   ├── equilateral.py
│   └── isosceles.py
└── tests/
    ├── __init__.py
    ├── test_equilateral.py
    └── test_isosceles.py
```

```Python linenums="1" title="Figure 2: Implementation of 'equilateral.py', a function that computes the area of an equilateral triangle."
import math


def equilateral_area(a):
    const = math.sqrt(3) / 4

    if a == 1:
        return const

    term = math.pow(a, 2)
    area = const * term
    return area
```

### Setup Instructions

To start using PyLLMut with this example, we first need
to set up the required environment by following these steps:

1. Clone the PyLLMut repository:

    ```bash
    git clone git@github.com:mohrez86/pyllmut.git
    ```
   
2. Copy the `examples` directory to a location of
your choice (e.g., your home directory):

    ```bash
    cp -r pyllmut/examples ~/pyllmut_examples
    ```

3. Navigate to the `examples` directory:

    ```bash
    cd ~/pyllmut_examples
    ```
   
4. Create a Python virtual environment using the following command.
   On some machines (e.g., MacBooks), you may need to use `python3` instead of `python`.
   Note that creating a Python virtual environment is optional in this example,
   but it is recommended to set up a dedicated Python environment for each project.

    ```bash
    python -m venv env
    ```

5. Activate the virtual environment
created in the previous step (if created):

    ```bash
    source env/bin/activate
    ```

6. Install PyLLMut by following the instructions in the
[Installation Guide](install.md).

### How to Use PyLLMut

PyLLMut is a Python library.
You can use it by importing it
into a Python program and calling its API.
The example in Figure 3 demonstrates 
how to use PyLLMut to generate mutants for a given Python module.

```python linenums="1" title="Figure 3: 'pyllmut_triangle_area.py', a script demonstrating how to use PyLLMut to generate mutants for 'equilateral.py'."
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
```

You can also find this code in the
[examples/pyllmut_triangle_area.py
](https://github.com/mohrez86/pyllmut/blob/main/examples/pyllmut_triangle_area.py)
file and run it using the following steps:

#### Running the Example

1. Navigate to the `examples` directory:

    ```bash
    cd ~/pyllmut_examples
    ```

2. Activate the virtual environment (if created):

    ```bash
    source env/bin/activate
    ```
   
3. Run `pyllmut_triangle_area.py`:

    ```bash
    python pyllmut_triangle_area.py
    ```

#### Explanation of `pyllmut_triangle_area.py`

The script in Figure 3 follows these steps:

##### Imports

- **Line 1** imports `logging` for debugging and status updates (lines 1 and 6 are optional).
- **Line 2** imports `Path` from `pathlib` for reading the module file.
- **Line 4** imports `MutantGenerator` and `ModelType` from PyLLMut.

##### Setup and Configuration

- **Lines 8 and 10** define `module_path` and read its content.
- **Lines 11-14** specify:
    - `lines_to_mutate`: A list of line numbers where mutants should be generated (7, 10, and 11).
    - `mutants_per_line`: The number of mutants to generate for each line (3).
    - `timeout_per_line`: The mutant generation timeout for each line (15 seconds).
    - `model_type`: The LLM model used (GPT-4o).

##### Mutation Generation

- **Lines 16-18** initialize a `MutantGenerator` object.
- **Line 19** calls the `generate()` method, which generates the mutants and returns a `MutationReport` object.
- **Line 20** retrieves a list of valid mutants using `get_valid_mutant_list()`.

##### Output Processing

- **Line 22** prints the total number of valid mutants PyLLMut generated.
- **Lines 24-34** print details of the first valid mutant, including:
    - The mutated line number.
    - A diff representation of the mutation.
    - The modified module content.

For more details about PyLLMut’s API, refer to the [API Reference](../api/generator.md) page.

##### Sample Output

Figure 4 shows an example of running `pyllmut_triangle_area.py`.
Lines 1-9 display logging messages, which can be disabled by removing 
`logging.basicConfig(...)` in Figure 3.

```bash linenums="1" title="Figure 4: Sample output of running 'pyllmut_triangle_area.py', displaying logging messages and the first valid mutant generated."
INFO:pyllmut.generator:LLM is generating 3 mutant(s) for line 7.
INFO:pyllmut.generator:PyLLMut is using model gpt-4o.
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
INFO:pyllmut.generator:LLM is generating 3 mutant(s) for line 10.
INFO:pyllmut.generator:PyLLMut is using model gpt-4o.
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
INFO:pyllmut.generator:LLM is generating 3 mutant(s) for line 11.
INFO:pyllmut.generator:PyLLMut is using model gpt-4o.
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"

**Number of valid mutants**: 9

First Valid Mutant
====================
**Line number**: 7
--------------------
**Diff Content**:
 --- original
+++ modified
@@ -4,7 +4,7 @@
 def equilateral_area(a):
     const = math.sqrt(3) / 4
 
-    if a == 1:
+    if a == 0:
         return const
 
     term = math.pow(a, 2)
--------------------
**Mutated Module Content**:
 import math


def equilateral_area(a):
    const = math.sqrt(3) / 4

    if a == 0:
        return const

    term = math.pow(a, 2)
    area = const * term
    return area
====================
```
