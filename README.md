#  Planification

Automated planning, also known as AI planning or automated plan generation, is a subfield of artificial intelligence that focuses on developing algorithms and techniques for generating plans or sequences of actions to achieve specific goals or objectives. The goal of automated planning is to build systems that can reason about complex tasks, generate plans to achieve them, and execute those plans in a real-world environment.

In this project we focus in deterministic automatic planning - the effects of actions are known with certainty. We implement an $$ A^{*} $$ algorithm that is build to adapt to any planification problem and domain.

The problems and domains must be defined in PDDL format. Example of files are given in the pddl_files folder.
We defined several heuristic functions that can be used interchangeably as inputs to the algorithm.


## 🏁 Getting started

Create a Python environment and activate it. After that, you need to use the command:
```
pip install -r requirements.txt
```

Then, run the file main.py with the arguments of your choice.

## Structure of the repository

- folder parser_files: contain the Python parser used in the code
- folder pddl_files: contains PDDL files for domain and problems
- .gitignore: used for Git to ignore some files
- a_star_algorithm.py: implementation of the A* algorithm along with other functions
- main.py: file to run the code
- README.md
- requirements.txt: contains the package requirements
