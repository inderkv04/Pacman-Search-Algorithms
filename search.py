# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions
from typing import List

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    state = problem.getStartState()
    stack = util.Stack()
    stack.push(state)
    backtracking_map = {state: []}
    visited = set()

    while not stack.isEmpty():
        node = stack.pop()
        if problem.isGoalState(node):
            return backtracking_map[node]
        
        if node not in visited:
            visited.add(node)
            for i in problem.getSuccessors(node):
                if i[0] not in visited:
                    stack.push(i[0])
                    backtracking_map[i[0]] = backtracking_map[node] + [i[1]]
    return []


def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "* YOUR CODE HERE *"
    state = problem.getStartState()
    queue = util.Queue()
    queue.push(state)
    backtracking_map = {state: []}
    visited = set([state])

    while queue:
        node = queue.pop()
        if problem.isGoalState(node):
            return backtracking_map[node]
        
        for i in problem.getSuccessors(node):
            if i[0] not in visited:
                queue.push(i[0])
                visited.add(i[0])
                backtracking_map[i[0]] = backtracking_map[node] + [i[1]]
    return []

def IDSHelper(problem, maxDepth):
    state = problem.getStartState()
    stack = util.Stack()
    stack.push((state, 0))
    backtracking_map = {state: []}
    visited = set()

    depth = 0
    while not stack.isEmpty() and depth <= maxDepth:
        loc, depth = stack.pop()
        if problem.isGoalState(loc):
            return backtracking_map[loc]
        
        if loc not in visited and depth < maxDepth:
            visited.add(loc)
            for i in problem.getSuccessors(loc):
                if i[0] not in visited:
                    stack.push((i[0], depth + 1))
                    backtracking_map[i[0]] = backtracking_map[loc] + [i[1]]
        
    return None

def iterativeDeepeningSearch(problem):
    """
    Perform DFS with increasingly larger depth. Begin with a depth of 1 and increment depth by 1 at every step.
    """
    "* YOUR CODE HERE *"
    depth = 1
    pathIDS = None
    while not pathIDS:
        pathIDS = IDSHelper(problem, depth)
        depth += 1
    return pathIDS

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "* YOUR CODE HERE *"
    initial_state = problem.getStartState()
    priority_queue = util.PriorityQueue()
    # Push initial state into Priority Queue with priority 0
    priority_queue.push((initial_state, [], 0), 0)
    visited = {}

    while not priority_queue.isEmpty():
        curr_state, path, cost = priority_queue.pop()

        if problem.isGoalState(curr_state):
            return path

        # If the state is already visited with a lower cost before, skip
        if curr_state in visited and visited[curr_state] <= cost:
            continue
        visited[curr_state] = cost

        for next, action, step_cost in problem.getSuccessors(curr_state):
            new_cost = cost + step_cost
            if next not in visited or new_cost < visited[next]:
                new_path = path + [action]
                priority_queue.push((next, new_path, new_cost), new_cost)
        
    return []

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """
    A* Search: Expands nodes with the lowest total estimated cost f = g + h.
    Returns a list of actions to reach the goal from the start state.
    """
    from util import PriorityQueue

    start_state = problem.getStartState()
    pq = PriorityQueue()
    pq.push((start_state, [], 0), heuristic(start_state, problem))

    #tracks the minimum known cost to reach each state
    visited_cost = {start_state: 0}

    while not pq.isEmpty():
        current_state, actions, current_cost = pq.pop()

        #skip if we already found a cheaper path to this state
        if current_cost > visited_cost.get(current_state, float("inf")):
            continue

        if problem.isGoalState(current_state):
            return actions

        #explore neighbors
        for next_state, direction, step_cost in problem.getSuccessors(current_state):
            new_cost = current_cost + step_cost

            #only consider this path if it’s cheaper than any previously found
            if new_cost < visited_cost.get(next_state, float("inf")):
                visited_cost[next_state] = new_cost
                total_estimated_cost = new_cost + heuristic(next_state, problem)
                pq.push((next_state, actions + [direction], new_cost), total_estimated_cost)

    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
ids = iterativeDeepeningSearch
