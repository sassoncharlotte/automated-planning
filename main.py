from time import time

from parser_files.pddlparser import PDDLParser
from a_star_algorithm import AStar


###########################################################
DOMAIN = 'pddl_files/groupe2/domain.pddl'
PROBLEM = 'pddl_files/groupe2/problem_easy.pddl'
###########################################################

parser = PDDLParser()
domain = parser.parse(DOMAIN)
problem = parser.parse(PROBLEM)

a_star = AStar(domain=domain, problem=problem)

start = time()
# A* algorithm
plan = a_star.a_star_algorithm(heuristic_name="null_heuristic")
end = time()
total_time = round(end - start, 2)

minutes = total_time // 60
seconds = total_time % 60

print(f"\nComputed in {int(minutes)} min {seconds}s\n")
print("-- Plan --")
for i, state in enumerate(plan):
    for pred in state:
        if pred[0]=="at":
            print(f"Step {i}:\n", pred)


## Groupe 2 ##

# Problem 1 224.8s
# 
# -- Plan --
# Step 0:
#  ('at', 'pos82')
# Step 1:
#  ('at', 'pos81')
# Step 2:
#  ('at', 'pos71')
# Step 3:
#  ('at', 'pos61')
# Step 4:
#  ('at', 'pos61')
# Step 5:
#  ('at', 'pos51')
# Step 6:
#  ('at', 'pos41')
# Step 7:
#  ('at', 'pos31')
# Step 8:
#  ('at', 'pos21')
# Step 9:
#  ('at', 'pos11')


