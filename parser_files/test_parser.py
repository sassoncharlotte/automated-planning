import pddlparser

domain_file = '../groupe2/domain.pddl'
problem_file = '../groupe2/problem0.pddl'

domain = pddlparser.PDDLParser.parse(domain_file)
problem = pddlparser.PDDLParser.parse(problem_file)

print(domain.actions, problem.initial_state.predicates)
