# Installation

## Prerequisites

Ensure you have met the following requirements before you begin:

- Python 3.6 or higher.
- `pip` for Python package management.

## Installing PyLLMut Library

Run the following command to install PyLLMut from 
[PyPI](https://pypi.org/project/PyLLMut/):

```bash
pip install pyllmut
```

To install the latest development version, install it directly from GitHub:

```bash
pip install git+https://github.com/mohrez86/pyllmut
```

Running this second command installs the latest version
of PyLLMut available on the main branch of
[its GitHub repository](https://github.com/mohrez86/pyllmut).

## Setting Up Your LLM API Key

PyLLMut needs an OpenAI API key to use LLMs. 
Follow these steps to create and add a key to your environment:

1. Visit the [OpenAI website](https://openai.com) 
   and sign up 
   for an account (you can use your 
   Google account for this step).

2. Once signed up, follow the 
   [Developer quickstart](https://platform.openai.com/docs/quickstart/step-2-setup-your-api-key.eot) 
   instructions to create an API key and export it to 
   an environment variable `OPENAI_API_KEY`.
   For instance, on Linux-based machines, you can use the
   following command to export the 
   key (replace `<your_api_key_here>` 
   with your actual API key):

```bash
export OPENAI_API_KEY=<your_api_key_here>
```

PyLLMut assumes this environment variable exists 
and contains your API key.
