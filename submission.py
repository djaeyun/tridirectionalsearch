# coding=utf-8
"""
This file is your main submission that will be graded against. Only copy-paste
code on the relevant classes included here. Do not add any classes or functions
to this file that are not part of the classes that we want.
"""

import heapq
import os
import pickle
import math


class PriorityQueue(object):
    """
    A queue structure where each element is served in order of priority.

    Elements in the queue are popped based on the priority with higher priority
    elements being served before lower priority elements.  If two elements have
    the same priority, they will be served in the order they were added to the
    queue.

    Traditionally priority queues are implemented with heaps, but there are any
    number of implementation options.

    (Hint: take a look at the module heapq)

    Attributes:
        queue (list): Nodes added to the priority queue.
    """

    def __init__(self):
        """Initialize a new Priority Queue."""

        self.queue = []

    def pop(self):
        """
        Pop top priority node from queue.

        Returns:
            The node with the highest priority.
        """
        node_pre = heapq.heappop(self.queue)
        if len(node_pre) == 5:
            node = (node_pre[0], node_pre[1], node_pre[2], node_pre[4])
        elif len(node_pre) == 3:
            node = (node_pre[0], node_pre[2])
        elif len(node_pre) == 2:
            node = node_pre[1]
        else:
            node = node_pre
        return node

    def remove(self, node):
        """
        Remove a node from the queue.

        Hint: You might require this in ucs. However, you may
        choose not to use it or to define your own method.

        Args:
            node (tuple): The node to remove from the queue.
        """

        self.queue.remove(node)
        return self.queue

    def __iter__(self):
        """Queue iterator."""

        return iter(sorted(self.queue))

    def __str__(self):
        """Priority Queue to string."""

        return 'PQ:%s' % self.queue

    def append(self, node):
        """
        Append a node to the queue.

        Args:
            node: Comparable Object to be added to the priority queue.
        """

        # Below 
        if type(node) == tuple:
            if len(node) == 2:
                index = len(self.queue) + 1
                heapq.heappush(self.queue, (node[0], index, node[1]))
            if len(node) == 3:
                index = len(self.queue) + 1
                heapq.heappush(self.queue, (node[0], node[1], index, node[2]))  
            if len(node) == 4:
                index = len(self.queue) +1
                heapq.heappush(self.queue, (node[0], node[1], node[2], index, node[3]))              
        elif type(node) == str:
            heapq.heappush(self.queue, node)
        else:
            heapq.heappush(self.queue, node)
        return self.queue
        
    def __contains__(self, key):
        """
        Containment Check operator for 'in'

        Args:
            key: The key to check for in the queue.

        Returns:
            True if key is found in queue, False otherwise.
        """

        return key in [n[-1] for n in self.queue]

    def __eq__(self, other):
        """
        Compare this Priority Queue with another Priority Queue.

        Args:
            other (PriorityQueue): Priority Queue to compare against.

        Returns:
            True if the two priority queues are equivalent.
        """

        return self.queue == other.queue

    def size(self):
        """
        Get the current size of the queue.

        Returns:
            Integer of number of items in queue.
        """

        return len(self.queue)

    def clear(self):
        """Reset queue to empty (no nodes)."""

        self.queue = []

    def next(self, i):

        return self.queue[i]

    def top(self):
        """
        Get the top item in the queue.

        Returns:
            The first item stored in the queue.
        """

        return self.queue[0]

def breadth_first_search(graph, start, goal):
    """
    Warm-up exercise: Implement breadth-first-search.
    See README.md for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        start (str): Key for the start node.
        goal (str): Key for the end node.

    Returns:
        The best path as a list from the start and goal nodes (including both).
    """
    frontier = PriorityQueue()
    explored = []
    solution = []

    # Ensure start and goal state are not the same, else return empty list
    if start == goal:
        return explored

    # Run loop until frontier is empty
    else:
        # Initialize frontier with starting node and depth counter to 1 (start state)
        frontier.append((0, start))
        parent_child = {}
        d = 1

        while frontier.size() != 0:

            # Remove node in frontier then move it to explored
            node = frontier.pop()[1]
            explored.append(node)

            if node == goal:
                break
            else:
                neighbors = [n for n in graph.neighbors(node)]
                neighbors = sorted(neighbors)
                i = 1
                frontier_size = frontier.size()
                for neighbor in neighbors:

                    # Only append node if the neighbor is not already explored or in the frontier
                    if neighbor not in explored and not (any(neighbor in x for x in frontier)):
                        parent_child[(node, i)] = (neighbor, d)     
                        if neighbor == goal:
                            solution = bfs_solution(graph, start, goal, parent_child)
                            return solution
                        frontier.append((d, neighbor)) 
                        i+=1
                
                if frontier.size() > frontier_size:
                    d+=1
            #print('frontier: ', frontier)
            #print('explored: ', explored)
            #print('dict: ', parent_child)
        
        solution = bfs_solution(graph, start, goal, parent_child)
        return solution
    raise NotImplementedError

def bfs_solution(graph, start, goal, parent_child):
    solution = []
    solution.append(goal)
    val = goal
    while val != start:
        for key in parent_child:
            if val == parent_child[key][0]:
                solution.append(key[0])
                val = key[0]
                d = parent_child[key][1] - 1
    return solution[::-1]

def ucs_solution(graph, start, goal, parent_child):
    solution = []
    solution.append(goal)
    val = goal
    cost = float("inf")
    for key in parent_child:
        if parent_child[key][0] == goal and parent_child[key][1] < cost:
            cost = parent_child[key][1]

    while val != start:
        for key in parent_child:
            if val == parent_child[key][0] and cost == parent_child[key][1]:
                sub_weight = graph.get_edge_weight(val, key[0])
                cost = cost - sub_weight
                solution.append(key[0])
                val = key[0]
    return solution[::-1]

def astar_solution(graph, start, goal, parent_child, heuristic):
    solution = []
    solution.append(goal)
    val = goal
    dist = float("inf")
    for key in parent_child:
        if parent_child[key][0] == goal and parent_child[key][1] < dist:
            dist = parent_child[key][1]

    while val != start:
        for key in parent_child:
            if val == parent_child[key][0] and abs(dist - parent_child[key][1]) < 0.01:
                f = graph.get_edge_weight(key[0], parent_child[key][0])
                g_next = heuristic(graph, parent_child[key][0], goal)
                g_prior = heuristic(graph, key[0], goal)
                dist = dist - (f + g_next) + g_prior
                solution.append(key[0])
                val = key[0]
    return solution[::-1]

def bi_ucs_solution(graph, start, goal, intersection, s_dict, g_dict):
    solution = []
    val = None
    mu = float("inf")

    # Find shortest path in the intersection
    for state in intersection:
        s_val_temp = float("inf")
        g_val_temp = float("inf")
        for key in s_dict:
            if s_dict[key][0] == state and s_dict[key][1] < s_val_temp:
                s_val_temp = s_dict[key][1]
        for key in g_dict:
            if g_dict[key][0] == state and g_dict[key][1] < g_val_temp:
                g_val_temp = g_dict[key][1]
        if s_val_temp == float("inf"):
            s_val_temp = 0
        if g_val_temp == float("inf"):
            g_val_temp = 0
        if s_val_temp + g_val_temp < mu:
            val = state
            mu = s_val_temp + g_val_temp
            s_val = s_val_temp
            g_val = g_val_temp

    # Stitch forward path
    f_val = val
    f_mu = s_val
    if f_val == start or f_mu == 0:
        solution.append(start)
    else:
        while f_val != start:
            for key in s_dict:
                if f_val == s_dict[key][0] and f_mu == s_dict[key][1]:
                    sub_weight = graph.get_edge_weight(f_val, key[0])
                    f_mu = f_mu - sub_weight
                    solution.append(key[0])
                    f_val = key[0]
    solution = solution[::-1]
    if solution[-1] != val:
        solution.append(val)

    # Stitch backward path
    b_val = val
    b_mu = g_val
    if (b_val == goal or b_mu == 0) and solution[-1] != val:
        solution.append(goal)
    else:
        while b_val != goal:
            for key in g_dict:
                if b_val == g_dict[key][0] and b_mu == g_dict[key][1]:
                    sub_weight = graph.get_edge_weight(b_val, key[0])
                    b_mu = b_mu - sub_weight
                    solution.append(key[0])
                    b_val = key[0] 
    return solution

def tri_ucs_solution(graph, start, goal, intersection, s_dict, g_dict):
    solution = []
    val = None
    mu = float("inf")

    # Find shortest path in the intersection
    s_states = {}
    g_states = {}
    for state in intersection:
        s_val = float("inf")
        g_val = float("inf")
        if state == start:
            s_states[state] = 0
        else:
            for key in s_dict:
                if s_dict[key][0] == state and s_dict[key][1] < s_val:
                    s_val = s_dict[key][1]
                    s_states[state] = s_val
        if state == goal:
            g_states[state] = 0
        else:
            for key in g_dict:
                if g_dict[key][0] == state and g_dict[key][1] < g_val:
                    g_val = g_dict[key][1]
                    g_states[state] = g_val
        if s_states[state] + g_states[state] < mu:
            val = state
            mu = s_states[state] + g_states[state]
    
    # Stitch forward path
    f_val = val
    f_mu = s_states[val]
    if f_val == start or f_mu == 0:
        solution.append(start)
    else:
        while f_val != start:
            for key in s_dict:
                if f_val == s_dict[key][0] and abs(f_mu - s_dict[key][1]) < 0.01:
                    f = graph.get_edge_weight(key[0], s_dict[key][0])
                    f_mu = f_mu - f
                    f_val = key[0]
                    solution.append(key[0])
    solution = solution[::-1]
    if solution[-1] != val:
        solution.append(val)

    # Stitch backward path
    b_val = val
    b_mu = g_states[val]
    if (b_val == goal or b_mu == 0) and solution[-1] != val:
        solution.append(goal)
    else:
        while b_val != goal:
            for key in g_dict:
                if b_val == g_dict[key][0] and abs(b_mu - g_dict[key][1]) < 0.01:
                    f = graph.get_edge_weight(key[0], g_dict[key][0])
                    b_mu = b_mu - f
                    b_val = key[0]
                    solution.append(key[0])
    cost = s_states[val] + g_states[val]    
    return (solution, cost)

def tri_a_star_solution(graph, start, goal, intersection, s_dict, g_dict, heuristic):
    solution = []
    val = None
    mu = float("inf")

    # neighbor, dist 1, dist 2, cost
    # Find shortest path in the intersection
    s_states = {}
    g_states = {}
    print('intersection: ', intersection)
    for state in intersection:
        s_cost = float("inf")
        g_cost = float("inf")
        if state == start:
            s_states[state] = (0, 0)
        else:
            for key in s_dict:
                if s_dict[key][0] == state and s_dict[key][3] < s_cost:
                    s_dist_1 = s_dict[key][1]
                    #s_dist_2 = s_dict[key][2]
                    s_cost = s_dict[key][3]
                    s_states[state] = (s_dist_1, s_cost)
        if state == goal:
            g_states[state] = (0, 0)
        else:
            for key in g_dict:
                if g_dict[key][0] == state and g_dict[key][3] < g_cost:
                    #g_dist_1 = g_dict[key][1]
                    g_dist_2 = g_dict[key][2]
                    g_cost = g_dict[key][3]
                    g_states[state] = (g_dist_2, g_cost)
        if s_states[state][1] + g_states[state][1] < mu:
            val = state
            mu = s_states[state][1] + g_states[state][1]
    print('s_states: ', s_states)
    print('g_states: ', g_states)
    # Stitch forward path
    f_val = val
    f_mu = s_states[val][0]
    print('f: ', f_val, f_mu)
    if f_val == start or f_mu == 0:
        solution.append(start)
    else:
        while f_val != start:
            for key in s_dict:
                if f_val == s_dict[key][0] and abs(f_mu - s_dict[key][1]) < 0.01:
                    f = graph.get_edge_weight(key[0], s_dict[key][0])
                    g_next = heuristic(graph, s_dict[key][0], goal)
                    g_prior = heuristic(graph, key[0], goal)
                    f_mu = f_mu - (f + g_next) + g_prior
                    f_val = key[0]
                    solution.append(key[0])
    solution = solution[::-1]
    if solution[-1] != val:
        solution.append(val)

    # Stitch backward path
    b_val = val
    b_mu = g_states[val][0]
    print('b: ', b_val, b_mu)
    if (b_val == goal or b_mu == 0) and solution[-1] != val:
        solution.append(goal)
    else:
        while b_val != goal:
            for key in g_dict:
                if b_val == g_dict[key][0] and abs(b_mu - g_dict[key][2]) < 0.01:
                    f = graph.get_edge_weight(key[0], g_dict[key][0])
                    g_next = heuristic(graph, g_dict[key][0], start)
                    g_prior = heuristic(graph, key[0], start)
                    b_mu = b_mu - (f + g_next) + g_prior
                    b_val = key[0]
                    solution.append(key[0])
                    print(b_val, b_mu)
    cost = s_states[val][1] + g_states[val][1]
    return (solution, cost)

def tri_ucs_final(goals, solution_12, solution_23, solution_31):
    solutions = [solution_12[0], solution_23[0], solution_31[0]]
    for sol in solutions:
        if set(goals).issubset(sol):
            return sol
    
    # Find minimum cost combination
    cost_min = float("inf")
    combo = None
    #print('12 + 23: ', solution_12[1] + solution_23[1])
    #print('23 + 31: ', solution_23[1] + solution_31[1])
    #print('31 + 12: ', solution_31[1] + solution_12[1])
    if solution_12[1] + solution_23[1] < cost_min:
        cost_min = solution_12[1] + solution_23[1]
        combo = (solution_12[0], solution_23[0])
    if solution_23[1] + solution_31[1] < cost_min:
        cost_min = solution_23[1] + solution_31[1]
        combo = (solution_23[0], solution_31[0])
    if solution_31[1] + solution_12[1] < cost_min:
        cost_min = solution_31[1] + solution_12[1]
        combo = (solution_31[0], solution_12[0])

    # Stitch best combo together
    if combo[0][-1] == combo[1][0]:
        solution = combo[0] + combo[1][1:]
    else:
        solution = combo[0] + combo[1]
    return solution

def tri_a_star_final(goals, solution_12, solution_23, solution_31):
    solutions = [solution_12, solution_23, solution_31]
    
    cost_min = float("inf")
    combo = None
    for sol in solutions:
        if set(goals).issubset(sol[0]) and sol[1] < cost_min:
            cost_min = sol[1]
            solution = sol[0]
    
    # Find minimum cost combination
    print('12 + 23: ', solution_12[1] + solution_23[1])
    print('23 + 31: ', solution_23[1] + solution_31[1])
    print('31 + 12: ', solution_31[1] + solution_12[1])
    if solution_12[1] + solution_23[1] < cost_min:
        cost_min = solution_12[1] + solution_23[1]
        combo = (solution_12[0], solution_23[0])
    if solution_23[1] + solution_31[1] < cost_min:
        cost_min = solution_23[1] + solution_31[1]
        combo = (solution_23[0], solution_31[0])
    if solution_31[1] + solution_12[1] < cost_min:
        cost_min = solution_31[1] + solution_12[1]
        combo = (solution_31[0], solution_12[0])

    # Stitch best combo together
    if combo is None:
        return solution
    if combo[0][-1] == combo[1][0]:
        solution = combo[0] + combo[1][1:]
    else:
        solution = combo[0] + combo[1]
    return solution

def bi_astar_solution(graph, start, goal, intersection, s_dict, g_dict, heuristic):
    solution = []
    val = None
    mu = float("inf")

    # Find shortest path in the intersection
    # neighbor, dist, f
    #print('intersection: ', intersection)
    s_states = {}
    g_states = {}
    for state in intersection:
        s_val_temp = float("inf")
        g_val_temp = float("inf")
        if state == start:
            s_states[state] = (0, 0)
        else:
            for key in s_dict:
                if s_dict[key][0] == state and s_dict[key][2] < s_val_temp:
                    s_val_temp = s_dict[key][2]
                    s_val = s_dict[key][1]
                    s_states[state] = (s_val, s_val_temp)
        if state == goal:
            g_states[state] = (0, 0)
        else:
            for key in g_dict:
                if g_dict[key][0] == state and g_dict[key][2] < g_val_temp:
                    g_val_temp = g_dict[key][2]
                    g_val = g_dict[key][1]
                    g_states[state] = (g_val, g_val_temp)
        if s_states[state][1] + g_states[state][1] < mu:
            val = state
            mu = s_states[state][1] + g_states[state][1]
    #print(s_states, g_states)
    # Stitch forward path
    f_val = val
    f_mu = s_states[val][0]
    #print('f: ', f_val, f_mu)
    if f_val == start or f_mu == 0:
        solution.append(start)
    else:
        while f_val != start:
            for key in s_dict:
                if f_val == s_dict[key][0] and abs(f_mu - s_dict[key][1]) < 0.01:
                    f = graph.get_edge_weight(key[0], s_dict[key][0])
                    g_next = heuristic(graph, s_dict[key][0], goal)
                    g_prior = heuristic(graph, key[0], goal)
                    f_mu = f_mu - (f + g_next) + g_prior
                    solution.append(key[0])
                    f_val = key[0]
    solution = solution[::-1]
    if solution[-1] != val:
        solution.append(val)

    # Stitch backward path
    b_val = val
    b_mu = g_states[val][0]
    #print('g: ', b_val, b_mu)
    if (b_val == goal or b_mu == 0) and solution[-1] != val:
        solution.append(goal)
    else:
        while b_val != goal:
            for key in g_dict:
                #if b_val == g_dict[key][0]:
                    #print(b_val, g_dict[key][1])
                if b_val == g_dict[key][0] and abs(b_mu - g_dict[key][1]) < 0.01:
                    f = graph.get_edge_weight(key[0], g_dict[key][0])
                    g_next = heuristic(graph, g_dict[key][0], start)
                    g_prior = heuristic(graph, key[0], start)
                    b_mu = b_mu - (f + g_next) + g_prior
                    solution.append(key[0])
                    b_val = key[0]
    return solution

def uniform_cost_search(graph, start, goal):
    """
    Warm-up exercise: Implement uniform_cost_search.

    See README.md for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        start (str): Key for the start node.
        goal (str): Key for the end node.

    Returns:
        The best path as a list from the start and goal nodes (including both).
    """
    
    frontier = PriorityQueue()
    explored = []
    solution = []

    # Ensure start and goal state are not the same, else return empty list
    if start == goal:
        return explored
    else:
        # Initialize frontier with starting node with distance 0
        frontier.append((0, start))
        parent_child = {}

        while frontier.size() != 0:
            node = frontier.pop()

            if node[1] == goal:
                solution = ucs_solution(graph, start, goal, parent_child)
                return solution

            explored.append(node[1])
            neighbors = [n for n in graph.neighbors(node[1])]
            frontier_size = frontier.size()
            i = 1
            for neighbor in neighbors:
                prior_weight = node[0]
                next_weight = graph.get_edge_weight(node[1], neighbor)
                weight = prior_weight + next_weight

                # Append node if the neighbor is not already explored or in the frontier
                if neighbor not in explored and not (any(neighbor in x for x in frontier)):
                    frontier.append((weight, neighbor)) 
                    parent_child[(node[1], i)] = (neighbor, weight)
                    i+=1

                # Append node if it's in frontier but has lower cost
                else:
                    for f_node in frontier:
                        if neighbor == f_node[2] and weight < f_node[0]:
                            frontier.remove(f_node)
                            frontier.append((weight, neighbor))
                            parent_child[(node[1], i)] = (neighbor, weight)
                            i+=1
            #print('frontier: ', frontier)
            #print('explored: ', explored)
            #print('dict: ', parent_child)
        solution = ucs_solution(graph, start, goal, parent_child)
        return solution
    raise NotImplementedError

def null_heuristic(graph, v, goal):
    """
    Null heuristic used as a base line.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        v (str): Key for the node to calculate from.
        goal (str): Key for the end node to calculate to.

    Returns:
        0
    """

    return 0

def euclidean_dist_heuristic(graph, v, goal):
    """
    Warm-up exercise: Implement the euclidean distance heuristic.

    See README.md for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        v (str): Key for the node to calculate from.
        goal (str): Key for the end node to calculate to.

    Returns:
        Euclidean distance between `v` node and `goal` node
    """

    v_coor = graph.nodes[v]['pos']
    g_coor = graph.nodes[goal]['pos']
    dist = ((v_coor[0] - g_coor[0]) ** 2 + (v_coor[1] - g_coor[1]) ** 2) ** (0.5)
    return dist

def get_location(queue):
    locations = []
    for i in range(queue.size()):
        node = queue.next(i)
        size = len(node)
        locations.append(node[size-1])
    return locations

def a_star(graph, start, goal, heuristic=euclidean_dist_heuristic):
    """
    Warm-up exercise: Implement A* algorithm.

    See README.md for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        start (str): Key for the start node.
        goal (str): Key for the end node.
        heuristic: Function to determine distance heuristic.
            Default: euclidean_dist_heuristic.

    Returns:
        The best path as a list from the start and goal nodes (including both).
    """
    frontier = PriorityQueue()
    explored = []
    solution = []

    # Ensure start and goal state are not the same, else return empty list
    if start == goal:
        return explored
    else:
        # Initialize frontier with starting node
        init_dist = heuristic(graph, start, goal)
        frontier.append((init_dist, 0, start))
        parent_child = {}

        while frontier.size() != 0:
            node = frontier.pop()

            if node[3] == goal:
                solution = astar_solution(graph, start, goal, parent_child, heuristic)
                return solution

            explored.append(node[3])
            neighbors = [n for n in graph.neighbors(node[3])]
            frontier_size = frontier.size()
            i = 1
            for neighbor in neighbors:
                f = graph.get_edge_weight(node[3], neighbor) + node[1]
                g = heuristic(graph, neighbor, goal)
                dist = f + g

                # Append node if the neighbor is not already explored or in the frontier
                if neighbor not in explored and not (any(neighbor in x for x in frontier)):
                    frontier.append((dist, f, neighbor)) 
                    parent_child[(node[3], i)] = (neighbor, dist, f)
                    i+=1

                # Append node if it's in frontier but has lower cost
                else:
                    for f_node in frontier:
                        if neighbor == f_node[3] and dist < f_node[0]:
                            frontier.remove(f_node)
                            frontier.append((dist, f, neighbor))
                            parent_child[(node[3], i)] = (neighbor, dist, f)
                            i+=1
            #print('frontier: ', frontier)
            #print('explored: ', explored)
            #print('dict: ', parent_child)
        solution = astar_solution(graph, start, goal, parent_child, heuristic)
        return solution
    raise NotImplementedError

def bidirectional_ucs(graph, start, goal):
    """
    Exercise 1: Bidirectional Search.

    See README.md for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        start (str): Key for the start node.
        goal (str): Key for the end node.

    Returns:
        The best path as a list from the start and goal nodes (including both).
    """
    s_frontier = PriorityQueue()
    g_frontier = PriorityQueue()
    s_explored = []
    g_explored = []
    solution = []

    # Ensure start and goal state are not the same, else return empty list
    if start == goal:
        return []
    else:
        # Initialize frontier with starting node with distance 0
        s_frontier.append((0, start))
        g_frontier.append((0, goal))
        s_parent_child = {}
        g_parent_child = {}

        while s_frontier.size() != 0 or g_frontier.size() != 0:
            if s_frontier.size() <= g_frontier.size():
                # Forward Expansion
                s_node = s_frontier.pop()
                #print('s popped: ', s_node)

                # Return solution if forward expansion is found in goal explored state
                if s_node[1] in g_explored or s_node[1] == goal:
                    g_frontier_locations = get_location(g_frontier)
                    g_union = list(set().union(g_frontier_locations, g_explored))
                    intersection = list(set(g_union) & set(s_explored))
                    intersection.append(s_node[1])
                    solution = bi_ucs_solution(graph, start, goal, intersection, s_parent_child, g_parent_child)
                    return solution
                
                s_explored.append(s_node[1])
                neighbors = [n for n in graph.neighbors(s_node[1])]

                i = 1
                if goal in neighbors:
                    prior_weight = s_node[0]
                    next_weight = graph.get_edge_weight(s_node[1], goal)
                    weight = prior_weight + next_weight
                    s_frontier.append((weight, goal))
                    s_parent_child[(s_node[1], i)] = (goal, weight)
                else: 
                    frontier_size = s_frontier.size()
                    for neighbor in neighbors:
                        prior_weight = s_node[0]
                        next_weight = graph.get_edge_weight(s_node[1], neighbor)
                        weight = prior_weight + next_weight

                        # Append node if the neighbor is not already explored or in the frontier
                        if neighbor not in s_explored and not (any(neighbor in x for x in s_frontier)):
                            s_frontier.append((weight, neighbor)) 
                            s_parent_child[(s_node[1], i)] = (neighbor, weight)
                            i+=1

                        # Append node if it's in frontier but has lower cost
                        else:
                            for f_node in s_frontier:
                                if neighbor == f_node[2] and weight < f_node[0]:
                                    s_frontier.remove(f_node)
                                    s_frontier.append((weight, neighbor))
                                    s_parent_child[(s_node[1], i)] = (neighbor, weight)
                                    i+=1
                #print('s_frontier:', s_frontier)
                #print('s_explored:', s_explored)
                #print('s_dict: ', s_parent_child)
            else:
                # Backward Expansion
                g_node = g_frontier.pop()
                #print('g popped: ', g_node)

                # Return solution if forward expansion is found in goal explored state
                if g_node[1] in s_explored or g_node[1] == start:
                    s_frontier_locations = get_location(s_frontier)
                    s_union = list(set().union(s_frontier_locations, s_explored))
                    intersection = list(set(s_union) & set(g_explored))
                    intersection.append(g_node[1])
                    solution = bi_ucs_solution(graph, start, goal, intersection, s_parent_child, g_parent_child)
                    return solution

                g_explored.append(g_node[1])
                neighbors = [n for n in graph.neighbors(g_node[1])]

                i = 1
                if start in neighbors:
                    prior_weight = g_node[0]
                    next_weight = graph.get_edge_weight(g_node[1], start)
                    weight = prior_weight + next_weight
                    g_frontier.append((weight, start))
                    g_parent_child[(g_node[1], i)] = (start, weight)
                else:
                    frontier_size = g_frontier.size()
                    for neighbor in neighbors:
                        prior_weight = g_node[0]
                        next_weight = graph.get_edge_weight(g_node[1], neighbor)
                        weight = prior_weight + next_weight

                        # Append node if the neighbor is not already explored or in the frontier
                        if neighbor not in g_explored and not (any(neighbor in x for x in g_frontier)):
                            g_frontier.append((weight, neighbor)) 
                            g_parent_child[(g_node[1], i)] = (neighbor, weight)
                            i+=1

                        # Append node if it's in frontier but has lower cost
                        else:
                            for f_node in g_frontier:
                                if neighbor == f_node[2] and weight < f_node[0]:
                                    g_frontier.remove(f_node)
                                    g_frontier.append((weight, neighbor))
                                    g_parent_child[(g_node[1], i)] = (neighbor, weight)
                                i+=1               
                #print('g_frontier:', g_frontier)
                #print('g_explored:', g_explored)
                #print('g_dict: ', g_parent_child)
    raise NotImplementedError

def bidirectional_a_star(graph, start, goal,
                         heuristic=euclidean_dist_heuristic):
    """
    Exercise 2: Bidirectional A*.

    See README.md for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        start (str): Key for the start node.
        goal (str): Key for the end node.
        heuristic: Function to determine distance heuristic.
            Default: euclidean_dist_heuristic.

    Returns:
        The best path as a list from the start and goal nodes (including both).
    """
    s_frontier = PriorityQueue()
    g_frontier = PriorityQueue()
    s_explored = []
    g_explored = []
    solution = []

    # Ensure start and goal state are not the same, else return empty list
    if start == goal:
        return []
    else:
        # Initialize frontier with starting node with distance 0
        init_dist = heuristic(graph, start, goal)
        s_frontier.append((init_dist, 0, start))
        g_frontier.append((init_dist, 0, goal))
        s_parent_child = {}
        g_parent_child = {}

        while s_frontier.size() != 0 or g_frontier.size() != 0:
            if s_frontier.size() <= g_frontier.size():
                # Forward Expansion
                s_node = s_frontier.pop()
                s_explored.append(s_node[3])
                #print('s popped: ', s_node)

                # Return solution if forward expansion is found in goal explored state
                if s_node[3] in g_explored or s_node[3] == goal:
                    g_frontier_locations = get_location(g_frontier)
                    g_union = list(set().union(g_frontier_locations, g_explored))
                    intersection = list(set(g_union) & set(s_explored))
                    #intersection.append(s_node[3])
                    solution = bi_astar_solution(graph, start, goal, intersection, s_parent_child, g_parent_child, heuristic)
                    return solution
                
                neighbors = [n for n in graph.neighbors(s_node[3])]
                frontier_size = s_frontier.size()
                i = 1
                if goal in neighbors:
                    f = graph.get_edge_weight(s_node[3], goal) + s_node[1]
                    dist = f
                    s_frontier.append((dist, f, goal)) 
                    s_parent_child[(s_node[3], i)] = (goal, dist, f)
                else:
                    for neighbor in neighbors:
                        f = graph.get_edge_weight(s_node[3], neighbor) + s_node[1]
                        g = heuristic(graph, neighbor, goal)
                        dist = f + g

                        # Append node if the neighbor is not already explored or in the frontier
                        if neighbor not in s_explored and not (any(neighbor in x for x in s_frontier)):
                            s_frontier.append((dist, f, neighbor)) 
                            s_parent_child[(s_node[3], i)] = (neighbor, dist, f)
                            i+=1

                        # Append node if it's in frontier but has lower cost
                        else:
                            for f_node in s_frontier:
                                if neighbor == f_node[3] and dist < f_node[0]:
                                    s_frontier.remove(f_node)
                                    s_frontier.append((dist, f, neighbor))
                                    s_parent_child[(s_node[3], i)] = (neighbor, dist, f)
                                    i+=1
                #print('s_frontier:', s_frontier)
                #print('s_explored:', s_explored)
                #print('s_dict: ', s_parent_child)
            else:
                # Backward Expansion
                g_node = g_frontier.pop()
                g_explored.append(g_node[3])
                #print('g popped: ', g_node)

                # Return solution if forward expansion is found in goal explored state
                if g_node[3] in s_explored or g_node[3] == start:
                    s_frontier_locations = get_location(s_frontier)
                    s_union = list(set().union(s_frontier_locations, s_explored))
                    intersection = list(set(s_union) & set(g_explored))
                    #intersection.append(g_node[3])
                    solution = bi_astar_solution(graph, start, goal, intersection, s_parent_child, g_parent_child, heuristic)
                    return solution

                neighbors = [n for n in graph.neighbors(g_node[3])]
                frontier_size = g_frontier.size()
                i = 1
                if start in neighbors:
                    f = graph.get_edge_weight(g_node[3], start) + g_node[1]
                    dist = f
                    g_frontier.append((dist, f, start)) 
                    g_parent_child[(g_node[3], i)] = (start, dist, f)
                else:
                    for neighbor in neighbors:
                        f = graph.get_edge_weight(g_node[3], neighbor) + g_node[1]
                        g = heuristic(graph, neighbor, start)
                        dist = f + g

                        # Append node if the neighbor is not already explored or in the frontier
                        if neighbor not in g_explored and not (any(neighbor in x for x in g_frontier)):
                            g_frontier.append((dist, f, neighbor)) 
                            g_parent_child[(g_node[3], i)] = (neighbor, dist, f)
                            i+=1

                        # Append node if it's in frontier but has lower cost
                        else:
                            for f_node in g_frontier:
                                if neighbor == f_node[3] and dist < f_node[0]:
                                    g_frontier.remove(f_node)
                                    g_frontier.append((dist, f, neighbor))
                                    g_parent_child[(g_node[3], i)] = (neighbor, dist, f)
                                    i+=1               
                #print('g_frontier:', g_frontier)
                #print('g_explored:', g_explored)
                #print('g_dict: ', g_parent_child)
    raise NotImplementedError

def tridirectional_search(graph, goals):
    """
    Exercise 3: Tridirectional UCS Search

    See README.MD for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        goals (list): Key values for the 3 goals

    Returns:
        The best path as a list from one of the goal nodes (including both of
        the other goal nodes).
    """
    # Initialize all frontiers
    g1_frontier = PriorityQueue()
    g2_frontier = PriorityQueue()
    g3_frontier = PriorityQueue()
    g1_explored = []
    g2_explored = []
    g3_explored = []
    g1_frontier.append((0, goals[0]))
    g2_frontier.append((0, goals[1]))
    g3_frontier.append((0, goals[2]))
    g1_dict = {}
    g2_dict = {}
    g3_dict = {}
    solution_12 = None
    solution_23 = None
    solution_31 = None
    g1_frontier_size = g1_frontier.size()
    g2_frontier_size = g2_frontier.size()
    g3_frontier_size = g3_frontier.size()

    if goals[0] == goals[1] and goals[1] == goals[2]:
        return []

    while solution_12 is None or solution_23 is None or solution_31 is None:
        # G1 to G2
        if min(g1_frontier_size, g2_frontier_size, g3_frontier_size) == g1_frontier_size and solution_12 is None:
            node = g1_frontier.pop()
            g1_explored.append(node[1])
            #print('g1 pop: ', node)

            if node[1] in g2_explored or node[1] == goals[1]:
                frontier_locations = get_location(g2_frontier)
                union = list(set().union(frontier_locations, g2_explored))
                intersection = list(set(union) & set(g1_explored))
                if node[1] not in intersection:
                    intersection.append(node[1])
                solution_12 = tri_ucs_solution(graph, goals[0], goals[1], intersection, g1_dict, g2_dict)
                g1_frontier_size = float("inf")

            elif node[1] in g3_explored or node[1] == goals[2]:
                frontier_locations = get_location(g3_frontier)
                union = list(set().union(frontier_locations, g3_explored))
                intersection = list(set(union) & set(g1_explored))
                if node[1] not in intersection:
                    intersection.append(node[1])
                solution_31 = tri_ucs_solution(graph, goals[2], goals[0], intersection, g3_dict, g1_dict)
                g3_frontier_size = float("inf")

            if g1_frontier_size != float("inf"):
                neighbors = [n for n in graph.neighbors(node[1])]
                i = 1
                for neighbor in neighbors:
                    prior_weight = node[0]
                    next_weight = graph.get_edge_weight(node[1], neighbor)
                    weight = prior_weight + next_weight

                    if neighbor not in g1_explored and not (any(neighbor in x for x in g1_frontier)):
                        g1_frontier.append((weight, neighbor))
                        g1_dict[(node[1], i)] = (neighbor, weight)
                        i+=1
                    
                    else:
                        for f_node in g1_frontier:
                            if neighbor == f_node[2] and weight < f_node[0]:
                                g1_frontier.remove(f_node)
                                g1_frontier.append((weight, neighbor))
                                g1_dict[(node[1], i)] = (neighbor, weight)
                                i+=1
                if g1_frontier_size != float("inf"):
                    g1_frontier_size = g1_frontier.size()
            #print('g1 frontier: ', g1_frontier)
            #print('g1_explored: ', g1_explored)
            #print('g1_dict: ', g1_dict)

        # G2 to G3
        if min(g2_frontier_size, g3_frontier_size) == g2_frontier_size and solution_23 is None:
            node = g2_frontier.pop()
            g2_explored.append(node[1])
            #print('g2 pop: ', node)

            if node[1] in g3_explored or node[1] == goals[2]:
                frontier_locations = get_location(g3_frontier)
                union = list(set().union(frontier_locations, g3_explored))
                intersection = list(set(union) & set(g2_explored))
                if node[1] not in intersection:
                    intersection.append(node[1])
                solution_23 = tri_ucs_solution(graph, goals[1], goals[2], intersection, g2_dict, g3_dict)
                g2_frontier_size = float("inf")

            elif node[1] in g1_explored or node[1] == goals[0]:
                frontier_locations = get_location(g1_frontier)
                union = list(set().union(frontier_locations, g1_explored))
                intersection = list(set(union) & set(g2_explored))
                if node[1] not in intersection:
                    intersection.append(node[1])
                solution_12 = tri_ucs_solution(graph, goals[0], goals[1], intersection, g1_dict, g2_dict)
                g1_frontier_size = float("inf")                               

            if g2_frontier_size != float("inf"):
                neighbors = [n for n in graph.neighbors(node[1])]
                i = 1
                for neighbor in neighbors:
                    prior_weight = node[0]
                    next_weight = graph.get_edge_weight(node[1], neighbor)
                    weight = prior_weight + next_weight

                    if neighbor not in g2_explored and not (any(neighbor in x for x in g2_frontier)):
                        g2_frontier.append((weight, neighbor))
                        g2_dict[(node[1], i)] = (neighbor, weight)
                        i+=1
                    
                    else:
                        for f_node in g2_frontier:
                            if neighbor == f_node[2] and weight < f_node[0]:
                                g2_frontier.remove(f_node)
                                g2_frontier.append((weight, neighbor))
                                g2_dict[(node[1], i)] = (neighbor, weight)
                                i+=1
                if g2_frontier_size != float("inf"):
                    g2_frontier_size = g2_frontier.size()
            #print('g2 frontier: ', g2_frontier)
            #print('g2 explored: ', g2_explored)
            #print('g2 dict: ', g2_dict)

        # G3 to G1
        if solution_31 is None:
            node = g3_frontier.pop()
            g3_explored.append(node[1])
            #print('g3 pop: ', node)

            if node[1] in g1_explored or node[1] == goals[0]:
                frontier_locations = get_location(g1_frontier)
                union = list(set().union(frontier_locations, g1_explored))
                intersection = list(set(union) & set(g3_explored))
                if node[1] not in intersection:
                    intersection.append(node[1])
                solution_31 = tri_ucs_solution(graph, goals[2], goals[0], intersection, g3_dict, g1_dict)
                g3_frontier_size = float("inf")

            elif node[1] in g2_explored or node[1] == goals[1]:
                frontier_locations = get_location(g2_frontier)
                union = list(set().union(frontier_locations, g2_explored))
                intersection = list(set(union) & set(g3_explored))
                if node[1] not in intersection:
                    intersection.append(node[1])
                solution_23 = tri_ucs_solution(graph, goals[1], goals[2], intersection, g2_dict, g3_dict)
                g2_frontier_size = float("inf")

            if g3_frontier_size != float("inf"):
                neighbors = [n for n in graph.neighbors(node[1])]
                i = 1
                for neighbor in neighbors:
                    prior_weight = node[0]
                    next_weight = graph.get_edge_weight(node[1], neighbor)
                    weight = prior_weight + next_weight

                    if neighbor not in g3_explored and not (any(neighbor in x for x in g3_frontier)):
                        g3_frontier.append((weight, neighbor))
                        g3_dict[(node[1], i)] = (neighbor, weight)
                        i+=1
                    
                    else:
                        for f_node in g3_frontier:
                            if neighbor == f_node[2] and weight < f_node[0]:
                                g3_frontier.remove(f_node)
                                g3_frontier.append((weight, neighbor))
                                g3_dict[(node[1], i)] = (neighbor, weight)
                                i+=1
                if g3_frontier_size != float("inf"):
                    g3_frontier_size = g3_frontier.size()
            #print('g3 frontier: ', g3_frontier)
            #print('g3 explored: ', g3_explored)
            #print('g3 dict: ', g3_dict)

    #print('separate paths: ', solution_12, solution_23, solution_31)
    solution = tri_ucs_final(goals, solution_12, solution_23, solution_31)
    print('path: ', solution)
    return solution

def tridirectional_upgraded(graph, goals, heuristic=euclidean_dist_heuristic):
    """
    Exercise 4: Upgraded Tridirectional Search

    See README.MD for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        goals (list): Key values for the 3 goals
        heuristic: Function to determine distance heuristic.
            Default: euclidean_dist_heuristic.

    Returns:
        The best path as a list from one of the goal nodes (including both of
        the other goal nodes).
    """
    # Initialize all frontiers
    print('start: ', goals[0], goals[1], goals[2])
    g1_frontier = PriorityQueue()
    g2_frontier = PriorityQueue()
    g3_frontier = PriorityQueue()
    g1_explored = []
    g2_explored = []
    g3_explored = []

    if goals[0] == goals[1] and goals[1] == goals[2]:
        return []
    else:
        # G1 = 1 to 2, 1 to 3 / G2 = 2 to 3, 2 to 1 / G3 = 3 to 1, 3 to 2
        g1_frontier.append((heuristic(graph, goals[0], goals[1]), heuristic(graph, goals[0], goals[2]), 0, goals[0]))
        g2_frontier.append((heuristic(graph, goals[1], goals[2]), heuristic(graph, goals[1], goals[0]), 0, goals[1]))
        g3_frontier.append((heuristic(graph, goals[2], goals[0]), heuristic(graph, goals[2], goals[1]), 0, goals[2]))
        g1_dict = {}
        g2_dict = {}
        g3_dict = {}
        solution_12 = None
        solution_23 = None
        solution_31 = None
        g1_frontier_size = g1_frontier.size()
        g2_frontier_size = g2_frontier.size()
        g3_frontier_size = g3_frontier.size()

    while solution_12 is None or solution_23 is None or solution_31 is None:
        #print(solution_12, solution_23, solution_31)
        # G1 to G2
        if min(g1_frontier_size, g2_frontier_size, g3_frontier_size) == g1_frontier_size:
            node = g1_frontier.pop()
            g1_explored.append(node[3])
            print('g1 pop: ', node)

            if (node[3] in g2_explored or node[3] == goals[1]) and solution_12 is None:
                frontier_locations = get_location(g2_frontier)
                union = list(set().union(frontier_locations, g2_explored))
                intersection = list(set(union) & set(g1_explored))
                if node[3] not in intersection:
                    intersection.append(node[3])
                solution_12 = tri_a_star_solution(graph, goals[0], goals[1], intersection, g1_dict, g2_dict, heuristic)
                print('term_12: ', solution_12)
                g1_frontier_size = float("inf")

            elif (node[3] in g3_explored or node[3] == goals[2]) and solution_31 is None:
                frontier_locations = get_location(g3_frontier)
                union = list(set().union(frontier_locations, g3_explored))
                intersection = list(set(union) & set(g1_explored))
                if node[3] not in intersection:
                    intersection.append(node[3])
                solution_31 = tri_a_star_solution(graph, goals[2], goals[0], intersection, g3_dict, g1_dict, heuristic)
                print('term_31: ', solution_31)
                g3_frontier_size = float("inf")

            if g1_frontier_size != float("inf"):
                neighbors = [n for n in graph.neighbors(node[3])]
                i = 1
                for neighbor in neighbors:
                    f = graph.get_edge_weight(node[3], neighbor) + node[2]
                    g_12 = heuristic(graph, neighbor, goals[1])
                    g_13 = heuristic(graph, neighbor, goals[2])
                    dist_12 = f + g_12
                    dist_13 = f + g_13

                    if neighbor not in g1_explored and not (any(neighbor in x for x in g1_frontier)):
                        g1_frontier.append((dist_12, dist_13, f, neighbor))
                        g1_dict[(node[3], i)] = (neighbor, dist_12, dist_13, f)
                        i+=1
                    
                    else:
                        for f_node in g1_frontier:
                            if neighbor == f_node[4] and dist_12 < f_node[0]:
                                g1_frontier.remove(f_node)
                                g1_frontier.append((dist_12, dist_13, f, neighbor))
                                g1_dict[(node[3], i)] = (neighbor, dist_12, dist_13, f)
                                i+=1
                            elif neighbor == f_node[4] and dist_13 < f_node[1]:
                                g1_frontier.remove(f_node)
                                g1_frontier.append((dist_12, dist_13, f, neighbor))
                                g1_dict[(node[3], i)] = (neighbor, dist_12, dist_13, f)
                                i+=1
                g1_frontier_size = g1_frontier.size()
            print('g1 frontier: ', g1_frontier)
            print('g1_explored: ', g1_explored)
            print('g1_dict: ', g1_dict)

        # G2 to G3
        elif min(g2_frontier_size, g3_frontier_size) == g2_frontier_size:
            node = g2_frontier.pop()
            g2_explored.append(node[3])
            print('g2 pop: ', node)

            if (node[3] in g3_explored or node[3] == goals[2]) and solution_23 is None:
                frontier_locations = get_location(g3_frontier)
                union = list(set().union(frontier_locations, g3_explored))
                intersection = list(set(union) & set(g2_explored))
                if node[3] not in intersection:
                    intersection.append(node[3])
                print('direction 23')
                solution_23 = tri_a_star_solution(graph, goals[1], goals[2], intersection, g2_dict, g3_dict, heuristic)
                print('term_23: ', solution_23)
                g2_frontier_size = float("inf")

            elif (node[3] in g1_explored or node[3] == goals[0]) and solution_12 is None:
                frontier_locations = get_location(g1_frontier)
                union = list(set().union(frontier_locations, g1_explored))
                intersection = list(set(union) & set(g2_explored))
                if node[3] not in intersection:
                    intersection.append(node[1])
                print('direction 12')
                solution_12 = tri_a_star_solution(graph, goals[0], goals[1], intersection, g1_dict, g2_dict, heuristic)
                print('term_12: ', solution_12)
                g1_frontier_size = float("inf")                               

            if g2_frontier_size != float("inf"):
                neighbors = [n for n in graph.neighbors(node[3])]
                i = 1
                for neighbor in neighbors:
                    f = graph.get_edge_weight(node[3], neighbor) + node[2]
                    g_23 = heuristic(graph, neighbor, goals[2])
                    g_12 = heuristic(graph, neighbor, goals[0])
                    dist_23 = f + g_23
                    dist_12 = f + g_12

                    if neighbor not in g2_explored and not (any(neighbor in x for x in g2_frontier)):
                        g2_frontier.append((dist_23, dist_12, f, neighbor))
                        g2_dict[(node[3], i)] = (neighbor, dist_23, dist_12, f)
                        i+=1
                    
                    else:
                        for f_node in g2_frontier:
                            if neighbor == f_node[4] and dist_23 < f_node[0]:
                                g2_frontier.remove(f_node)
                                g2_frontier.append((dist_23, dist_12, f, neighbor))
                                g2_dict[(node[3], i)] = (neighbor, dist_23, dist_12, f)
                                i+=1
                            elif neighbor == f_node[4] and dist_12 < f_node[0]:
                                g2_frontier.remove(f_node)
                                g2_frontier.append((dist_23, dist_12, f, neighbor))
                                g2_dict[(node[3], i)] = (neighbor, dist_23, dist_12, f)
                                i+=1
                g2_frontier_size = g2_frontier.size()
            print('g2 frontier: ', g2_frontier)
            print('g2 explored: ', g2_explored)
            print('g2 dict: ', g2_dict)

        # G3 to G1
        else:
            node = g3_frontier.pop()
            g3_explored.append(node[3])
            print('g3 pop: ', node)

            if (node[3] in g1_explored or node[3] == goals[0]) and solution_31 is None:
                frontier_locations = get_location(g1_frontier)
                union = list(set().union(frontier_locations, g1_explored))
                intersection = list(set(union) & set(g3_explored))
                if node[3] not in intersection:
                    intersection.append(node[3])
                solution_31 = tri_a_star_solution(graph, goals[2], goals[0], intersection, g3_dict, g1_dict, heuristic)
                print('term_31: ', solution_31)
                g3_frontier_size = float("inf")

            elif (node[3] in g2_explored or node[3] == goals[1]) and solution_23 is None:
                frontier_locations = get_location(g2_frontier)
                union = list(set().union(frontier_locations, g2_explored))
                intersection = list(set(union) & set(g3_explored))
                if node[3] not in intersection:
                    intersection.append(node[3])
                solution_23 = tri_a_star_solution(graph, goals[1], goals[2], intersection, g2_dict, g3_dict, heuristic)
                print('term_23: ', solution_23)
                g2_frontier_size = float("inf")

            if g3_frontier_size != float("inf"):
                neighbors = [n for n in graph.neighbors(node[3])]
                i = 1
                for neighbor in neighbors:
                    f = graph.get_edge_weight(node[3], neighbor) + node[2]
                    g_31 = heuristic(graph, neighbor, goals[0])
                    g_23 = heuristic(graph, neighbor, goals[1])
                    dist_31 = f + g_31
                    dist_23 = f + g_23                    

                    if neighbor not in g3_explored and not (any(neighbor in x for x in g3_frontier)):
                        g3_frontier.append((dist_31, dist_23, f, neighbor))
                        g3_dict[(node[3], i)] = (neighbor, dist_31, dist_23, f)
                        i+=1
                    
                    else:
                        for f_node in g3_frontier:
                            if neighbor == f_node[4] and dist_31 < f_node[0]:
                                g3_frontier.remove(f_node)
                                g3_frontier.append((dist_31, dist_23, f, neighbor))
                                g3_dict[(node[3], i)] = (neighbor, dist_31, dist_23, f)
                                i+=1
                            elif neighbor == f_node[4] and dist_23 < f_node[0]:
                                g3_frontier.remove(f_node)
                                g3_frontier.append((dist_31, dist_23, f, neighbor))
                                g3_dict[(node[3], i)] = (neighbor, dist_31, dist_23, f)
                                i+=1
                g3_frontier_size = g3_frontier.size()
            print('g3 frontier: ', g3_frontier)
            print('g3 explored: ', g3_explored)
            print('g3 dict: ', g3_dict)

    print('separate paths: ', solution_12, solution_23, solution_31)
    solution = tri_a_star_final(goals, solution_12, solution_23, solution_31)
    print('start, path: ', goals, solution)
    return solution

def return_your_name():
    """Return your name from this function"""
    name = 'David Jaeyun Kim'
    return name

def custom_heuristic(graph, v, goal):
    """
       Feel free to use this method to try and work with different heuristics and come up with a better search algorithm.
       Args:
           graph (ExplorableGraph): Undirected graph to search.
           v (str): Key for the node to calculate from.
           goal (str): Key for the end node to calculate to.
       Returns:
           Custom heuristic distance between `v` node and `goal` node
       """

pass


# Extra Credit: Your best search method for the race
def custom_search(graph, start, goal, data=None):
    """
    Race!: Implement your best search algorithm here to compete against the
    other student agents.

    If you implement this function and submit your code to Gradescope, you'll be
    registered for the Race!

    See README.md for exercise description.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        start (str): Key for the start node.
        goal (str): Key for the end node.
        data :  Data used in the custom search.
            Will be passed your data from load_data(graph).
            Default: None.

    Returns:
        The best path as a list from the start and goal nodes (including both).
    """

    # TODO: finish this function!
    raise NotImplementedError


def load_data(graph, time_left):
    """
    Feel free to implement this method. We'll call it only once 
    at the beginning of the Race, and we'll pass the output to your custom_search function.
    graph: a networkx graph
    time_left: function you can call to keep track of your remaining time.
        usage: time_left() returns the time left in milliseconds.
        the max time will be 10 minutes.

    * To get a list of nodes, use graph.nodes()
    * To get node neighbors, use graph.neighbors(node)
    * To get edge weight, use graph.get_edge_weight(node1, node2)
    """

    # nodes = graph.nodes()
    return None
 
 
def haversine_dist_heuristic(graph, v, goal):
    """
    Note: This provided heuristic is for the Atlanta race.

    Args:
        graph (ExplorableGraph): Undirected graph to search.
        v (str): Key for the node to calculate from.
        goal (str): Key for the end node to calculate to.

    Returns:
        Haversine distance between `v` node and `goal` node
    """

    #Load latitude and longitude coordinates in radians:
    vLatLong = (math.radians(graph.nodes[v]["pos"][0]), math.radians(graph.nodes[v]["pos"][1]))
    goalLatLong = (math.radians(graph.nodes[goal]["pos"][0]), math.radians(graph.nodes[goal]["pos"][1]))

    #Now we want to execute portions of the formula:
    constOutFront = 2*6371 #Radius of Earth is 6,371 kilometers
    term1InSqrt = (math.sin((goalLatLong[0]-vLatLong[0])/2))**2 #First term inside sqrt
    term2InSqrt = math.cos(vLatLong[0])*math.cos(goalLatLong[0])*((math.sin((goalLatLong[1]-vLatLong[1])/2))**2) #Second term
    return constOutFront*math.asin(math.sqrt(term1InSqrt+term2InSqrt)) #Straight application of formula
