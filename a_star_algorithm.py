import itertools


def plan_cost(plan):
    """
    Convert a plan to a cost, handling nonexistent plans.
    Returns the length of the plan if it exists, otherwise returns positive infinity.

    Args:
        plan: Plan to convert to a cost.

    Returns:
        int: Length of the plan if it exists, otherwise positive infinity.
    """
    if plan is None:
        return float('inf')
    else:
        return len(plan)


def reconstruct_path(node):
    """ Gives the paths to node """
    path = [node.predicates]
    while node.parent:
        node = node.parent
        path.append(node.predicates)
    return list(reversed(path))


def state_contains_goal(goals, state, constant_predicates):
    """ Tests if the state contains all goals """
    for goal in goals:
        if goal not in state and goal not in constant_predicates:
            return False
    return True


def get_value_predicate(predicate, candidate):
    """ Returns the predicate with arguments replace with candidate's values """
    candidate_predicate = tuple([predicate[0]] + [candidate[i] for i in predicate[1:] if i])
    # if predicate has arity = 0
    if len(candidate_predicate) == 1:
        candidate_predicate = (predicate[0], '')
    return candidate_predicate



class State:
    """ A plannification problem state """
    def __init__(self, predicates: list, cost: int = 0, heuristic: float = 0.0):
        self.predicates = predicates
        self.cost = cost
        self.heuristic = heuristic
        self.parent = None


class AStar:
    def __init__(self, domain, problem) -> None:
        self.domain = domain
        self.problem = problem
        self.constant_predicates = None
        self.objects = problem.initial_state.objects


    def get_initial_predicate_lists(self):
        """ Gives initial state predicates with adjacent predicates put in a separate constant list """
        constant_predicates, initial_predicates = [], []

        for predicate in self.problem.initial_state.predicates:
            if predicate[0] in ["adjacent"]:
                constant_predicates.append(predicate)
            else:
                initial_predicates.append(predicate)
        return initial_predicates, constant_predicates


    def get_actions(self, current_state):
        """ 
        Gives the list of all possible actions applicable from current_state
        Arguments:
        - current_state: the list of current predicates that aren't in constant_predicates
        Returns: a list of actions
        """
        actions = []
        for action in self.domain.actions:
            possible_values = {
                param[0]: self.objects[param[1]] for param in zip(action.arg_names, action.types)
            }
            for candidate in ( (dict(zip(possible_values, x)) for x in itertools.product(*possible_values.values()) )):
                action_is_valid = True
                for precond in action.preconditions.literals:
                    # Negative predicate
                    if precond[0]==-1:
                        neg_precond = precond[1]
                        # Applies candidate's values as arguments for the predicate
                        neg_candidate_precond = get_value_predicate(neg_precond, candidate)
                        if neg_candidate_precond in current_state or neg_candidate_precond in self.constant_predicates:
                            action_is_valid = False
                            break
                    # Positive predicate
                    else:
                        candidate_precond = get_value_predicate(precond, candidate)
                        if candidate_precond not in current_state and candidate_precond not in self.constant_predicates:
                            action_is_valid = False
                            break
                if action_is_valid:
                    actions.append((action, candidate))
        return actions


    def get_neighbors(self, current_state):
        """
        Gives the list of all reachable states from current_state
        Arguments:
        - current_state: the list of current predicates that aren't in constant_predicates

        Returns: the list of all successor states of current_state
        """
        # get all possible actions
        actions = self.get_actions(current_state)

        # compute all successor states
        states = []
        for action in actions:
            state = current_state.copy()
            action_function, candidate = action
            for predicate in action_function.effects.literals:
                if predicate[0]==-1:
                    neg_value_predicate = get_value_predicate(predicate[1], candidate)
                    if neg_value_predicate in state:
                        state.remove(neg_value_predicate)
                        state.append((-1, neg_value_predicate))
                else:
                    value_predicate = get_value_predicate(predicate, candidate)
                    if value_predicate not in state:
                        state.append(value_predicate)
            states.append(state)
        return states


    def a_star_algorithm(self, heuristic_name):
        """ A* algorithm """
        closed_list, open_list = [], []
        initial_predicates, self.constant_predicates = self.get_initial_predicate_lists()

        state = State(predicates=initial_predicates, cost=0, heuristic=0)
        goals = State(predicates=self.problem.goals, cost=0, heuristic=0)

        # print(state.predicates, "\n")
        # print(self.problem.goals, "\n")

        open_list.append(state)

        while len(open_list) > 0:
            u = min(open_list, key=lambda x: x.heuristic)
            open_list.remove(u)

            if state_contains_goal(goals.predicates, u.predicates, self.constant_predicates):
                return reconstruct_path(u)

            for v in self.get_neighbors(u.predicates):
                v = State(predicates=v, cost=0, heuristic=0)
                v.parent = u
                if v not in closed_list and v not in open_list:
                    v.cost = u.cost + 1
                    v.heuristic = v.cost + self.distance(v.predicates, goals.predicates, heuristic_name)
                    open_list.append(v)
            closed_list.append(u)
        raise ValueError("No path found")


    def distance(self, state, goal, heuristic_name):
        """ Heuristic estimation between state and goal """
        if heuristic_name == 'null_heuristic':
            distance = 0

        # if heuristic_name == 'monotone':
        #     monotone_plan = a_star(domain, problem, heuristic_name='null_heuristic', state=state, monotone=True)
        #     distance = plan_cost(monotone_plan)

        if heuristic_name=="hamming_distance":
            distance = sum(s != g for s, g in zip(state, goal))

        if heuristic_name=="predicates_difference":
            distance = abs(len(state) - len(goal))

        if heuristic_name=="sum_of_subgoals":
            subgoals = [g for g in goal if g not in state]
            distance = 0
            while subgoals:
                best_distance = float('inf')
                best_successor = None
                for successor in self.get_neighbors(state):
                    successor_distance = sum(g not in successor for g in subgoals)
                    if successor_distance < best_distance:
                        best_distance = successor_distance
                        best_successor = successor
                distance += 1
                state = best_successor
                subgoals = [g for g in subgoals if g not in state]

        if heuristic_name=="max_proposition":
            max_propositions = 0
            for prop in goal:
                visited = [set()]
                queue = [(state, 0)]
                while queue:
                    current, distance = queue.pop(0)
                    if prop in current:
                        max_propositions = max(max_propositions, distance)
                        break
                    visited.append(current)
                    for successor in self.get_neighbors(current):
                        if successor not in visited:
                            queue.append((successor, distance + 1))
        return distance
