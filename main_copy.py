from time import time

from parser_files.pddlparser import PDDLParser
from a_star_algorithm import a_star, plan_cost

parser = PDDLParser()
domain = parser.parse('pddl_files/groupe2/domain.pddl')
problem = parser.parse('pddl_files/groupe2/problem_easy.pddl')

start = time()
plan = a_star(domain, problem, heuristic='null_heuristic')
end = time()

print(plan_cost(plan))

print(f"\nComputed in {round(end - start, 2)}s\n")
print("-- Plan --")
for i, state in enumerate(plan):
    # for pred in state:
    #     if pred[0]=="at":
    #         print(f"Step {i}:\n", pred)
    print(i, state)