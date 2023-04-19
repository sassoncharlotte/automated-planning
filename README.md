# 🤖 Automatic Planning Project (PO)

Automated planning, also known as AI planning or automated plan generation, is a subfield of artificial intelligence that focuses on developing algorithms and techniques for generating plans or sequences of actions to achieve specific goals or objectives. The goal of automated planning is to build systems that can reason about complex tasks, generate plans to achieve them, and execute those plans in a real-world environment.

In this project, we focus on deterministic automatic planning, where the effects of actions are known with certainty. We implement a general purpose $A^{*}$ algorithm, built to adapt to any automatic planning problem and domain.

The problems and domains must be defined in the PDDL format. Examples of such files are given in the ```pddl_files``` folder.
We defined several heuristic functions that can be used interchangeably as inputs to the algorithm.

## 🏁 Getting started

Create a Python environment and activate it. After that, you need to use the following command to install all the required packages and dependencies:

```
pip install -r requirements.txt
```

Then, run the ```main.py``` file with the arguments of your choice.

## 🗂️ Structure of the repository

- ```parser_files``` folder: contain the Python parser used in the code
- ```pddl_files``` folder: contains PDDL files for domain and problems
- ```.gitignore```: used for Git to ignore some files
- ```a_star_algorithm.py```: implementation of the A* algorithm along with other functions
- ```main.py```: file to run the code
- ```README.md```
- ```requirements.txt```: contains the packages and dependencies requirements
