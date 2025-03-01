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

In this example, we use PyLLMut to generate
mutants for `equilateral.py`, shown in Figure 2.

```Python linenums="1" title="Figure 2: equilateral.py"
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
created in the previous step (if you created it):

    ```bash
    source env/bin/activate
    ```

6. Install PyLLMut by following the instructions in the
[Installation Guide](install.md).

### How to Use PyLLMut

PyLLMut is a Python library that can be used by importing it
into a Python program and calling its API. Figure 3 shows
an example of using PyLLMut through its API.

```python linenums="1" title="Figure 3: pyllmut_triangle_area.py"
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
```

You can also find this code in the
[examples/pyllmut_triangle_area.py
](https://github.com/mohrez86/pyllmut/blob/main/examples/pyllmut_triangle_area.py)
file and run it using the following steps:

1. Navigate to the `examples` directory, created in the previous steps:

    ```bash
    cd ~/pyllmut_examples
    ```

2. Activate the virtual environment
created in the previous step (if you created it):

    ```bash
    source env/bin/activate
    ```
   
3. Run `pyllmut_triangle_area.py` using the following command:

    ```bash
    python pyllmut_triangle_area.py
    ```

#### Details of `pyllmut_triangle_area.py`

In `pyllmut_triangle_area.py` shown in Figure 3:

- Line 6 imports the [MutantGenerator](../api/generator.md) class.
- Lines 14-18 instantiate a `MutantGenerator`
  object by passing three parameters:
      1. *Parameter 1:* The content of the module to be mutated. 
         The variable `module_content`
         is a string containing the code of `equilateral.py` in Figure 2.
      2. *Parameter 2:* An optional list of lines for which to generate mutants.
        The default value for this parameter is `None`, 
        in which case PyLLMut generates mutants for
        every code line in the given module.
        The variable `lines_to_mutate` is a list of three numbers: 
         7, 10, and 11, meaning we want to generate mutants for
        these three lines in Figure 2.
      3. *Parameter 3:* An optional number indicating the number of 
        mutants to generate for each line. The
        default value for this parameter is 1.
        The variable `mutants_per_line` is set to 3, meaning
        we want PyLLMut to generate three mutants per line.
- Line 19 calls the `generate()` method of `MutantGenerator`,
which returns a [MutationReport](../api/mutation_report.md) object.
- Line 20 retrieves a list of valid mutants generated
by PyLLMut by calling the `get_valid_mutant_list` method
form `MutationReport`. Each mutant is a [MutantInfo](../api/mutant_info.md) object.
- Lines 24-29 print some information from one of the valid mutants
generated. Specifically, it prints the line number, the mutant as a diff,
and the mutated code.

To learn more about the PyLLMut API, refer 
to the [API Reference](../api/generator.md) page.

Figure 4 shows the result of running `pyllmut_triangle_area.py`,
as demonstrated in Figure 3. Lines 1-6 in Figure 4 shows some logging information,
which can be turned off by removing lines 3-4 in Figure 3.

```bash linenums="1" title="Figure 4: Result of running pyllmut_triangle_area.py"
INFO:pyllmut.generator:LLM is generating 3 mutant(s) for line 7.
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
INFO:pyllmut.generator:LLM is generating 3 mutant(s) for line 10.
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
INFO:pyllmut.generator:LLM is generating 3 mutant(s) for line 11.
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
Number of valid mutants: 9
Line number: 7
---------
--- original
+++ modified
@@ -4,7 +4,7 @@
 def equilateral_area(a):
     const = math.sqrt(3) / 4
 
-    if a == 1:
+    if a != 1:
         return const
 
     term = math.pow(a, 2)
---------
import math


def equilateral_area(a):
    const = math.sqrt(3) / 4

    if a != 1:
        return const

    term = math.pow(a, 2)
    area = const * term
    return area
```
