import math
from time import time
import heapq

def planner(problem, heuristic=None, state0=None, goal=None,
            monotone=False, verbose=True):
    """
    Implements A* search to find a plan for the given problem.
    Arguments:
    problem   - a pyddl Problem
    heuristic - a heuristic to use (h(state) = 0 by default)
    state0    - initial state (problem.initial_state by default)
    goal      - tuple containing goal predicates and numerical conditions
                (default is (problem.goals, problem.num_goals))
    monotone  - if True, only applies actions by ignoring delete lists
    verbose   - if True, prints statistics before returning
    """
    if heuristic is None:
        heuristic = null_heuristic
    if state0 is None:
        state0 = problem.initial_state
    if goal is None:
        goal = (problem.goals, problem.num_goals)

    states_explored = 0
    closed = set()
    fringe = [(heuristic(state0), -state0.cost, state0)]
    heapq.heapify(fringe)
    start = time()
    while True:
        if len(fringe) == 0:
            if verbose: print('States Explored: %d' % states_explored)
            return None

        # Get node with minimum evaluation function from heap
        h, _, node = heapq.heappop(fringe)
        states_explored += 1

        # Goal test
        if node.is_true(*goal):
            plan = node.plan()
            dur = time() - start
            if verbose:
                print('States Explored: %d' % states_explored)
                print('Time per state: %.3f ms' % (1000*dur / states_explored))
                print('Plan length: %d' % node.cost)
            return plan

        # Expand node if we haven't seen it before
        if node not in closed:
            closed.add(node)

            # Apply all applicable actions to get successors
            successors = set(node.apply(action, monotone)
                             for action in problem.grounded_actions
                             if node.is_true(action.preconditions,
                                             action.num_preconditions))

            # Compute heuristic and add to fringe
            for successor in successors:
                if successor not in closed:
                    f = successor.cost + heuristic(successor)
                    heapq.heappush(fringe, (f, -successor.cost, successor))


class Heuristics:
    @staticmethod
    def manhattan_heuristic(node, goal):
        """
        Manhattan heuristic function.
        Calculates the Manhattan distance between two nodes as the sum of the absolute differences in their x and y coordinates.
        Assumes nodes have attributes `x` and `y` representing their coordinates.

        Args:
            node (node): Current node for which the heuristic value is calculated.
            goal (node): Goal node for the A* algorithm.

        Returns:
            float: Manhattan heuristic value.
        """
        return abs(node.x - goal.x) + abs(node.y - goal.y)

    @staticmethod
    def euclidean_heuristic(node, goal):
        """
        Euclidean heuristic function.
        Calculates the Euclidean distance between two nodes as the square root of the sum of the squared differences
        in their x, y, and z (if applicable) coordinates.
        Assumes nodes have attributes `x`, `y`, and `z` (if applicable) representing their coordinates.

        Args:
            node (node): Current node for which the heuristic value is calculated.
            goal (node): Goal node for the A* algorithm.

        Returns:
            float: Euclidean heuristic value.
        """
        dx = node.x - goal.x
        dy = node.y - goal.y
        dz = node.z - goal.z if hasattr(node, 'z') and hasattr(goal, 'z') else 0
        return math.sqrt(dx**2 + dy**2 + dz**2)

    @staticmethod
    def null_heuristic(state):
        """
        Admissible, but trivial heuristic.
        Returns a constant value of 0 as the heuristic value.

        Args:
            state: Current state for which the heuristic value is calculated.

        Returns:
            int: Heuristic value of 0.
        """
        return 0

    @staticmethod
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

    @staticmethod
    def monotone_heuristic(problem):
        """
        Heuristic that finds plans using only add lists of actions.
        Calculates the cost of the plan using the `planner` function with the `monotone` flag set to True.

        Args:
            problem: Problem instance for which the heuristic value is calculated.

        Returns:
            int: Heuristic value.
        """
        def h(state):
            monotone_plan = planner(problem, Heuristics.null_heuristic, state, monotone=True, verbose=False)
            return Heuristics.plan_cost(monotone_plan)
        return h

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
                subgoal_plan = planner(problem, null_heuristic, state, ((g,), ()))
                costs.append(plan_cost(subgoal_plan))
            for g in problem.num_goals:
                subgoal_plan = planner(problem, null_heuristic, state, ((), (g,)))
                costs.append(plan_cost(subgoal_plan))
            return max(costs)
        return h