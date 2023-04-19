from time import time

from parser_files.pddlparser import PDDLParser
from a_star_algorithm import AStar


###########################################################
DOMAIN = 'pddl_files/groupe2/domain.pddl'
PROBLEM = 'pddl_files/groupe2/problem0.pddl'
HEURISTIC_NAME = "monotone"
# Among: "null_heuristic", "sum_of_subgoals", "hamming_distance", "max_proposition", "monotone"
###########################################################

parser = PDDLParser()
domain = parser.parse(DOMAIN)
problem = parser.parse(PROBLEM)

a_star = AStar(domain=domain, problem=problem)

start = time()
# A* algorithm
plan = a_star.a_star_algorithm(heuristic_name=HEURISTIC_NAME)
end = time()
total_time = round(end - start, 2)

minutes = total_time // 60
seconds = total_time % 60

# print("-- Plan --")
# for i, state in enumerate(plan):
#     for pred in state:
#         if pred[0]=="at":
#             print(f"Step {i}:\n", pred)

print(f"\nComputed in {int(minutes)} min {round(seconds, 3)}s\n")
print(f"Plan length: {len(plan)}\n")
