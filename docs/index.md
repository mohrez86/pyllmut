# PyLLMut Documentation

[![PyPI version](https://badge.fury.io/py/pyllmut.svg)](https://badge.fury.io/py/pyllmut)
[![PyPI Downloads](https://static.pepy.tech/badge/pyllmut)](https://pepy.tech/projects/pyllmut)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/mohrez86/pyllmut/blob/main/LICENSE.txt)
![Status](https://img.shields.io/badge/Status-Experimental-orange)
![Research](https://img.shields.io/badge/Research-Driven-lightgrey)
[![Open Source](https://img.shields.io/badge/Open%20Source-Yes-brightgreen)](https://github.com/mohrez86/pyllmut)
[![Tests](https://github.com/mohrez86/pyllmut/actions/workflows/tests-conda.yml/badge.svg)](https://github.com/mohrez86/pyllmut/actions/workflows/tests-conda.yml)

## Introduction

PyLLMut—pronounced "Pill Moot" (/pɪl muːt/)—is 
a research-based LLM-driven mutant generator library 
for Python. It uses Large Language Models (LLMs) to 
generate mutants for a given Python module.
The current version of PyLLMut 
supports `gpt-4o-mini` through its API. 
We plan to add support for more models, 
such as *DeepSeek-R1*.

!!! tip "PyLLMut has been integrated into [FauxPy](https://fauxpy.readthedocs.io) 🚀"
    [FauxPy](https://fauxpy.readthedocs.io) 
    now supports **LLM-driven mutation-based fault 
    localization** using *GPT-4o mini*!  
    This functionality is the result of 
    integrating PyLLMut into [FauxPy](https://fauxpy.readthedocs.io).

!!! note
    PyLLMut is **not** a full-fledged 
    mutation analysis framework such as 
    [Cosmic Ray](https://cosmic-ray.readthedocs.io/)
    that generates mutants for the whole project, 
    runs tests to kill them, and reports mutation scores. 
    PyLLMut is a library that generates mutants for 
    Python modules. In fact, any 
    mutation analysis frameworks (e.g., Cosmic Ray) 
    can leverage PyLLMut in 
    their mutant generation phase to 
    enhance their results.

### Why `gpt-4o-mini`?

We picked `gpt-4o-mini` for now since 
it is a cheaper model compared to other 
OpenAI models, as we are conducting several tests.
Given the modular structure of PyLLMut, adding 
support for more models later will not be a problem.

Also, according to a recent study 
[On the Use of Large Language Models 
in Mutation Testing](https://arxiv.org/abs/2406.09843), 
`gpt-4o-mini` performs fairly well considering 
its lower price.

### Local Models vs. API

Our first attempt was to use local models, but
running large language models on a regular 
machine is extremely slow.
We want PyLLMut to be usable on regular laptops.  So, for now, we decided to 
start with using LLMs through their API.
Supporting local models later will not be a problem,
considering the modular nature of PyLLMut.

## Key Features

- Uses LLMs to generate mutants for Python code.
- Currently supports `gpt-4o-mini` via API.
- Future plans: support for more models such as *DeepSeek-R1*.

## Motivation

Although traditional—heuristic-based—mutation operators
have been effectively used for decades in different domains,
such as mutation testing and fault localization,
they have a key limitation: they cannot always generate mutants
for certain program statements.

Recent studies on fault localization, including
[An Empirical Study of Fault Localization in Python 
Programs](https://link.springer.com/article/10.1007/s10664-024-10475-3),
indicate that Mutation-Based Fault Localization (MBFL) techniques
are not always effective due to this limitation.
Traditional mutation operators fail to generate mutants for
some buggy statements, which reduces the overall effectiveness
of MBFL techniques.

However, our preliminary experimental results show that
LLMs can generate effective mutants for these buggy statements
where traditional mutation operators fail.
This motivated the development of PyLLMut, aiming to
enhance mutant generation by leveraging the capabilities of LLMs.

## Use Cases

PyLLMut can be used anywhere mutant generation 
is needed. For instance, mutants are widely 
used in mutation testing, fault localization, automated program repair, 
and many other domains. 
PyLLMut can be used for any of these activities.

## Background & Research

PyLLMut is a research-based project, inspired by the study 
[On the Use of Large Language Models in 
Mutation Testing](https://arxiv.org/abs/2406.09843), which was 
originally for Java.
During the development of PyLLMut, we faced and continue to 
face several research questions—some of which you may find 
here and there inside the PyLLMut source code as comments 
or in this documentation.

During development, we tried (and keep trying) 
to find solutions for as many of these 
questions as we could. When further 
research is required, we develop PyLLMut in a way that it performs 
as soundly and robustly as possible without crashing.
As we continue our research in this area, we 
improve PyLLMut by finding research-based answers for such questions. 
If you find anything interesting, have any features 
in mind, or encounter bugs, feel free to share 
them with us.

## Navigation to Other Sections
- **[User Guide](user/install.md)** → How to install and use PyLLMut.
- **[API Reference](api/generator.md)** → Detailed documentation of available functions and parameters.
