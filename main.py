from parser_files.pddlparser import PDDLParser
from a_star_algorithm import a_star

parser = PDDLParser()
domain = parser.parse('pddl_files/domain.pddl')
problem = parser.parse('pddl_files/problem_easy.pddl')

plan = a_star(domain, problem)
for i, state in enumerate(plan):
    print(f"Step {i}:\n", state)
