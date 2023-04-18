import itertools
# import math

class State:
    """ A planning problem state """
    def __init__(self, predicates: list, cost: int = 0, heuristic: float = 0.0):
        self.predicates = predicates
        self.cost = cost
        self.heuristic = heuristic
        self.parent = None


def get_initial_predicate_lists(problem):
    """ Gives initial state predicates with adjacent predicates put in a separate constant list """
    constant_predicates, initial_predicates = [], []

    for predicate in problem.initial_state.predicates:
        if predicate[0] in ["adjacent"]:
            constant_predicates.append(predicate)
        else:
            initial_predicates.append(predicate)
    return initial_predicates, constant_predicates

def state_contains_goal(goals, state, constant_predicates):
    """ Tests if the state contains all goals """
    for goal in goals:
        if goal not in state and goal not in constant_predicates:
            return False
    return True

def a_star(domain, problem, heuristic='null_heuristic', state=None, monotone=False):
    """ A* algorithm """
    closed_list, open_list = [], []
    objects = problem.initial_state.objects
    initial_predicates, constant_predicates = get_initial_predicate_lists(problem)
    if not state:
        state = State(predicates=initial_predicates, cost=0, heuristic=0)
    goals = State(predicates=problem.goals, cost=0, heuristic=0)
    open_list.append(state)

    while len(open_list) > 0:
        u = min(open_list, key=lambda x: x.heuristic)
        open_list.remove(u)

        if state_contains_goal(goals.predicates, u.predicates, constant_predicates):
            return reconstruct_path(u)

        for v in get_neighbors(u.predicates, constant_predicates, domain.actions, objects, monotone):
            v = State(predicates=v, cost=0, heuristic=0)
            v.parent = u
            if v not in closed_list and v not in open_list:
                v.cost = u.cost + 1
                v.heuristic = v.cost + distance(v, goals, domain, problem, heuristic)
                open_list.append(v)
        closed_list.append(u)
    raise ValueError("No path found")

def reconstruct_path(node):
    """ Gives the paths to node """
    path = [node.predicates]
    while node.parent:
        node = node.parent
        path.append(node.predicates)
    return list(reversed(path))

def distance(state, goal, domain, problem, heuristic):
    """ Heuristic estimation between state and goal """
    # state_pred = state.predicates
    # goal_pred = goal.predicates

    distance_dict = {'null_heuristic': Heuristics.null_heuristic(),   #(state, goal, domain, problem)  #####
                     'monotone_heuristic': Heuristics.monotone_heuristic(state, goal, domain, problem)} #,
                     # 'subgoal_heuristic': Heuristics.subgoal_heuristic()}
    
    # return distance_dict[heuristic]
    return Heuristics.null_heuristic()

def get_value_predicate(predicate, candidate):
    """ Returns the predicate with arguments replace with candidate's values """
    candidate_predicate = tuple([predicate[0]] + [candidate[i] for i in predicate[1:] if i])
    # if predicate has arity = 0
    if len(candidate_predicate) == 1:
        candidate_predicate = (predicate[0], '')
    return candidate_predicate

def get_actions(current_state, constant_predicates, all_actions, objects):
    """ 
    Gives the list of all possible actions applicable from current_state
    Arguments:
    - current_state: the list of current predicates that aren't in constant_predicates
    - constant_predicates: the list of constant predicates (True all the time)
    - all_actions: list of all domain actions
    - objects: list of all problem objects
    Returns: a list of actions
    """
    actions = []
    for action in all_actions:
        possible_values = {
            param[0]: objects[param[1]] for param in zip(action.arg_names, action.types)
        }
        for candidate in ( (dict(zip(possible_values, x)) for x in itertools.product(*possible_values.values()) )):
            action_is_valid = True
            for precond in action.preconditions.literals:
                # Negative predicate
                if precond[0]==-1:
                    neg_precond = precond[1]
                    # Applies candidate's values as arguments for the predicate
                    neg_candidate_precond = get_value_predicate(neg_precond, candidate)
                    if neg_candidate_precond in current_state or neg_candidate_precond in constant_predicates:
                        action_is_valid = False
                        break
                # Positive predicate
                else:
                    candidate_precond = get_value_predicate(precond, candidate)
                    if candidate_precond not in current_state and candidate_precond not in constant_predicates:
                        action_is_valid = False
                        break
            if action_is_valid:
                actions.append((action, candidate))
    return actions

def get_neighbors(current_state, constant_predicates, all_actions, objects, monotone=False):
    """
    Gives the list of all reachable states from current_state
    Arguments:
    - current_state: the list of current predicates that aren't in constant_predicates
    - constant_predicates: the list of constant predicates (True all the time)
    - all_actions: list of all domain actions
    - objects: list of all problem objects
    - monotone: a boolean flag indicating whether to ignore delete lists (default: False)
    Returns: the list of all successor states of current_state
    """
    # get all possible actions
    actions = get_actions(current_state, constant_predicates, all_actions, objects)

    # compute all successor states
    states = []
    for action in actions:
        state = current_state.copy()
        action_function, candidate = action
        for predicate in action_function.effects.literals:
            if not monotone:
                if predicate[0]==-1:
                    neg_value_predicate = get_value_predicate(predicate[1], candidate)
                    if neg_value_predicate in state:
                        state.remove(neg_value_predicate)
                        state.append((-1, neg_value_predicate))
                else:
                    value_predicate = get_value_predicate(predicate, candidate)
                    if value_predicate not in state:
                        state.append(value_predicate)
            else:
                if not predicate[0]==-1:
                    value_predicate = get_value_predicate(predicate, candidate)
                    if value_predicate not in state:
                        state.append(value_predicate)
        states.append(state)
    return states

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

# Heuristics

class Heuristics:
    # @staticmethod
    # def manhattan_heuristic(node, goal):
    #     """
    #     Manhattan heuristic function.
    #     Calculates the Manhattan distance between two nodes as the sum of the absolute differences in their x and y coordinates.
    #     Assumes nodes have attributes `x` and `y` representing their coordinates.

    #     Args:
    #         node (node): Current node for which the heuristic value is calculated.
    #         goal (node): Goal node for the A* algorithm.

    #     Returns:
    #         float: Manhattan heuristic value.
    #     """
    #     return abs(node.x - goal.x) + abs(node.y - goal.y)

    # @staticmethod
    # def euclidean_heuristic(node, goal):
    #     """
    #     Euclidean heuristic function.
    #     Calculates the Euclidean distance between two nodes as the square root of the sum of the squared differences
    #     in their x, y, and z (if applicable) coordinates.
    #     Assumes nodes have attributes `x`, `y`, and `z` (if applicable) representing their coordinates.

    #     Args:
    #         node (node): Current node for which the heuristic value is calculated.
    #         goal (node): Goal node for the A* algorithm.

    #     Returns:
    #         float: Euclidean heuristic value.
    #     """
    #     dx = node.x - goal.x
    #     dy = node.y - goal.y
    #     dz = node.z - goal.z if hasattr(node, 'z') and hasattr(goal, 'z') else 0
    #     return math.sqrt(dx**2 + dy**2 + dz**2)

    @staticmethod
    def null_heuristic():
        """
        Admissible, but trivial heuristic.
        Returns a constant value of 0 as the heuristic value.

        Returns:
            int: Heuristic value of 0.
        """
        return 0

    @staticmethod
    def monotone_heuristic(state, goal, domain, problem):
        """
        Heuristic that finds plans using only add lists of actions.
        Calculates the cost of the plan using the `a_star` function with the `monotone` flag set to True. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        Args:
            problem: Problem instance for which the heuristic value is calculated.

        Returns:
            int: Heuristic value.
        """
        # def h(state):
        monotone_plan = a_star(domain, problem, heuristic='null_heuristic', state=state, monotone=True)  #, Heuristics.null_heuristic, state, monotone=True, verbose=False)
        return plan_cost(monotone_plan)
        # return h

    @staticmethod
    def subgoal_heuristic(problem):
        """
        Heuristic that computes the max cost of plans across all subgoals.
        Calculates the cost of the plan using the `planner` function for each subgoal, and returns the maximum cost.

        Args:
            problem: Problem instance for which the heuristic value is calculated.

        Returns:
            int: Heuristic value.
        """
        def h(state):
            costs = []
            for g in problem.goals:
                subgoal_plan = a_star(problem, Heuristics.null_heuristic, state, ((g,), ()))
                costs.append(plan_cost(subgoal_plan))
            # for g in problem.num_goals:
            #     subgoal_plan = a_star(problem, Heuristics.null_heuristic, state, ((), (g,)))
            #     costs.append(plan_cost(subgoal_plan))
            return max(costs)
        return h
