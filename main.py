from time import time

from parser_files.pddlparser import PDDLParser
from a_star_algorithm import a_star

parser = PDDLParser()
domain = parser.parse('pddl_files/groupe1/domain.pddl')
problem = parser.parse('pddl_files/groupe1/problem0.pddl')

start = time()
plan = a_star(domain, problem)
end = time()

print(f"\nComputed in {round(end - start, 2)}s\n")
print("-- Plan --")
for i, state in enumerate(plan):
    for pred in state:
        if pred[0]=="at":
            print(f"Step {i}:\n", pred)
