# CS 6601: Artificial Intelligence - Assignment 2 - Search

## Setup

Clone this repository:

`git clone https://github.gatech.edu/omscs6601/assignment_2.git`

Activate the environment you had created during Assignment 0:

`conda activate ai_env`

In case you used a different environment name, to list of all environments you have on your machine you can run `conda env list`.

## Overview

Search is an integral part of AI. It helps in problem solving across a wide variety of domains where a solution isn’t immediately clear.  You will implement several graph search algorithms with the goal of solving bi-directional and tri-directional search.

### Submission

Submit the `submission.py` file to Gradescope for grading.

You are allowed **two submissions every thirty minutes**.

The deliverable for the assignment is a 'submission.py' file with all the functions/methods completed.

**In your Gradescope submission history, you can mark a certain submission as 'Active'.**

### The Files

While you'll only have to edit and submit **__submission.py__**, there are a number of notable files:

1. **__submission.py__**: Where you will implement your _PriorityQueue_, _Breadth First Search_, _Uniform Cost Search_, _A* Search_, _Bi-directional Search_, Tri-directional Search_
2. **_search_submission_tests.py_**: Sample tests to validate your searches locally.
3. **_search_unit_tests.py_**: More detailed tests that run searches from all possible pairs of nodes in the graph
4. **_search_submission_tests_grid.py_**: Tests searches on uniform grid and highlights path and explored nodes.
5. **_romania_graph.pickle_**: Serialized graph files for Romania.
6. **_atlanta_osm.pickle_**: Serialized graph files for Atlanta (optional for robust testing for Race!).
7. **_explorable_graph.py_**: A wrapper around `networkx` that tracks explored nodes. **FOR DEBUGGING ONLY**
9. **_visualize_graph.py_**: Module to visualize search results. See below on how to use it.
10. **_osm2networkx.py_**: Module used by visualize graph to read OSM networks.

### Notes
#### A note on using the graph and grading

Points for each section are awarded based on finding the correct path and by evaluating the number of nodes explored. To track the number of times a node is explored during the search, the ExplorableGraph wrapper is used on the networkx Graph class. Every time you process a node, by calling graph[node] or graph.neighbors(node), the count for that node increases by one. You will need to use one of these methods to add a node's neighbors to the search queue, just be careful not to call it unnecessarily throughout your code. We have created the graph.get_edge_weight(u, v) method to be used to access edge weights between two nodes, u and v. All other normal networkx Graph operations can be performed.  


#### A note on visualizing results for the Atlanta graph:

The Atlanta graph is too big to display within a Python window like Romania. As a result, when you run the bidirectional tests in **_search_submission_tests.py_**, it generates a JSON file in the GeoJSON format. To see the graph, you can upload it to a private GitHub Gist or use [this](http://geojson.io/) site.
If you want to see how **_visualize_graph.py_** is used, take a look at the class TestBidirectionalSearch in **_search_submission_tests.py_**

## Resources

* Canvas, [Lesson 2: Search](https://gatech.instructure.com/courses/151546/pages/2-search?module_item_id=806500)
* R&N slides on [Uninformed Search](https://www.cc.gatech.edu/~thad/6601-gradAI-fall2015/chapter03-clean.pdf)
* [Informed Search](https://www.cc.gatech.edu/~thad/6601-gradAI-fall2015/chapter04a.pdf)
* [Comparing BFS and DFS](https://cs.stanford.edu/people/abisee/tutorial/bfsdfs.html)
* [A* Search](https://cs.stanford.edu/people/abisee/tutorial/astar.html)

Links from Udacity, below the videos:
* [Finding Optimal Solutions to Rubik's Cube Using Pattern Databases](https://www.cs.princeton.edu/courses/archive/fall06/cos402/papers/korfrubik.pdf)
* [God's Number is 26 in the Quarter-Turn Metric](http://www.cube20.org/qtm/)
* [Reach for A∗: An Efficient Point-to-Point Shortest Path Algorithm](http://www.cc.gatech.edu/~thad/6601-gradAI-fall2015/02-search-01-Astart-ALT-Reach.pdf)
* [Computing the Shortest Path: A∗ Search Meets Graph Theory](http://www.cc.gatech.edu/~thad/6601-gradAI-fall2015/02-search-Goldberg03tr.pdf)
* [Reach-based Routing: A New Approach to Shortest Path Algorithms Optimized for Road Networks](http://www.cc.gatech.edu/~thad/6601-gradAI-fall2015/02-search-Gutman04siam.pdf)

**_Please refrain from referring code/psuedocode from any other resource that is not provided here._**

## The Assignment

Your task is to implement several informed search algorithms that will calculate a driving route between two points in Romania with a minimal time and space cost.
There is a `search_submission_tests.py` file to help you along the way. Your searches should be executed with minimal runtime and memory overhead.

We will be using an undirected network representing a map of Romania (and an optional Atlanta graph used for the Race!).

**Frequently Asked Questions Along with Issues and Solutions**<br />
Also, as an extra note, there are some things that are among our most common questions:

* Remember that if start and goal are the same, you should return []. This keeps your results consistent with ours and avoids some headache.
* When nodes in the priority queue have the same priority value, break ties according to FIFO. Hint: A counter can be used to track when nodes enter the priority queue.
* Your priority queue implementation should allow for duplicate nodes to enter the queue.
* There is a little more to this when you get to tridirectional, so read those Notes especially carefully as well
* **Do not** use graph.explored_nodes for anything that you submit to Gradescope. This can be used for debugging, but you should not be calling this in your code. **Additionally, please make sure you read the "Notes" section above.**
* If you are stuck, check out the resources! We recognize this is a hard assignment and tri-directional search is a more research-oriented topic than the other search algorithms. Many previous students have found it useful to go through the resources in this README if they are having difficulty understanding the algorithms. Hopefully they are of some use to you all as well! :)
* We have included the "Haversine" heuristic in the `search_submission_tests.py` file. All of the local tests on the Atlanta map use this method. For the race, you can use whatever you choose, but know that the Atlanta map positions are (latitude, longitude). If you would like to learn more about this formula, here is a link: https://en.wikipedia.org/wiki/Haversine_formula
* Make sure you clean up any changes/modifications/additions you make to the networkx graph structure before you exit the search function. Depending on your changes, the auto grader might face difficulties while testing. The best alternative is to create your own data structure(s).
* If you're having problems (exploring too many nodes) with your Breadth first search implementation, one thing many students have found useful is to re-watch the Udacity videos for an optimization trick mentioned.
* Most 'NoneType object ...' errors are because the path you return is not completely connected (a pair of successive nodes in the path are not connected). Or because the path variable itself is empty.
* Adding unit tests to your code may cause your submission to fail. It is best to comment them out when you submit.
* Individual tests can be run using the following:
```python
import search_submission_tests as tests
tests.TestPriorityQueue().test_append_and_pop()
```
* For running the search tests, use this:
``` python
import search_submission_tests as tests
testclass = tests.TestBasicSearch()
testclass.setUp()
testclass.test_bfs()
```

### Warmups
We'll start by implementing some simpler optimization and search algorithms before the real exercises.

#### Warmup 1: Priority queue

_[5 points]_

In all searches that involve calculating path cost or heuristic (e.g. uniform-cost), we have to order our search frontier. It turns out the way that we do this can impact our overall search runtime.

To show this, you'll implement a priority queue which will help you in understanding its performance benefits. For large graphs, sorting all input to a priority queue is impractical. As such, the data structure you implement should have an amortized O(1) insertion and O(lg n) removal time. It should do better than the naive implementation in our tests (InsertionSortQueue), which sorts the entire list after every insertion.

In this implementation of priority queue, if two elements have the same priority, they should be served according to the order in which they were enqueued (see Hint 3).  

> **Notes**:
> **While the idea of amortization is quite an interesting one that you may want to think about, please note that this is not the focus
> of this assignment. The heapq library should be enough for this assignment. If you want to optimize further, you can always come back to
> this section.**

> **Hint:**
> **The heapq module has been imported for you. Feel free to use it.**

> **Hint 2:**
> **The local tests provided are used to test the correctness of your implementation of the Priority Queue. To verify that your implementation consistently beats the naive implementation, you might want to test it with a large number of elements.**

> **Hint 3:**
> **If you choose to use the heapq library, keep in mind that the queue will sort entries as a whole upon being enqueued, not just on the first element. This means you need to figure out a way to keep elements with the same priority in FIFO order.**

> **Hint 4:**
> **You may enqueue nodes however you like, but when your Priority Queue is tested, we feed node in the form (priority, value).**

#### Warmup 2: BFS

_[5 pts]_

To get you started with handling graphs, implement and test breadth-first search over the test network.

You'll complete this by writing the `breadth_first_search()` method. This returns a path of nodes from a given start node to a given end node, as a list.

For this part, it is optional to use the PriorityQueue as your frontier. You will require it from the next question onwards. You can use it here too if you want to be consistent.

> **Notes**:
> 1. You need to include start and goal in the path.
> 2. **If your start and goal are the same then just return [].**
> 3. The above are just to keep your results consistent with our test cases.
> 4. You can access all the neighbors of a given node by calling `graph[node]`, or `graph.neighbors(node)` ONLY. 
> 5. You are not allowed to maintain a cache of the neighbors for any node. You need to use the above mentioned methods to get the neighbors.
> 6. To measure your search performance, the `explorable_graph.py` provided keeps track of which nodes you have accessed in this way (this is referred to as the set of 'Explored' nodes). To retrieve the set of nodes you've explored in this way, call `graph.explored_nodes`. If you wish to perform multiple searches on the same graph instance, call `graph.reset_search()` to clear out the current set of 'Explored' nodes. **WARNING**, these functions are intended for debugging purposes only. Calls to these functions will fail on Gradescope.
> 7. In BFS, because we are using unit edge weight, make sure you process the neighbors in alphabetical order. Because networkx uses dictionaries, the order that it returns the neighbors is not fixed. This can cause differences in the number of explored nodes from run to run. If you sort the neighbors alphabetically before processing them, you should return the same number of explored nodes each time.

#### Warmup 3: Uniform-cost search

_[10 points]_

Implement uniform-cost search, using PriorityQueue as your frontier. From now on, PriorityQueue should be your default frontier.

`uniform_cost_search()` should return the same arguments as breadth-first search: the path to the goal node (as a list of nodes).

> **Notes**:
> 1. You need to include start and goal in the path.
> 2. **If your start and goal are the same then just return [].**
> 3. The above are just to keep your results consistent with our test cases.
> 4. You can access all the neighbors of a given node by calling `graph[node]`, or `graph.neighbors(node)` ONLY. 
> 5. You can access the weight of an edge using: `graph.get_edge_weight(node_1, node_2)`. Not using this method will result in your explored nodes count being higher than it should be.
> 6. You are not allowed to maintain a cache of the neighbors for any node. You need to use the above mentioned methods to get the neighbors and corresponding weights.
> 7. We will provide some margin of error in grading the size of your 'Explored' set, but it should be close to the results provided by our reference implementation.

#### Warmup 4: A* search

_[10 points]_

Implement A* search using Euclidean distance as your heuristic. You'll need to implement `euclidean_dist_heuristic()` then pass that function to `a_star()` as the heuristic parameter. We provide `null_heuristic()` as a baseline heuristic to test against when calling a_star tests.

> **Hint**:
> You can find a node's position by calling the following to check if the key is available: `graph.nodes[n]['pos']`

> **Notes**:
> 1. You need to include start and goal in the path.
> 2. **If your start and goal are the same then just return [].**
> 3. The above are just to keep your results consistent with our test cases.
> 4. You can access all the neighbors of a given node by calling `graph[node]`, or `graph.neighbors(node)` ONLY. 
> 5. You can access the weight of an edge using: `graph.get_edge_weight(node_1, node_2)`. Not using this method will result in your explored nodes count being higher than it should be.
> 6. You are not allowed to maintain a cache of the neighbors for any node. You need to use the above mentioned methods to get the neighbors and corresponding weights.
> 7. You can access the (x, y) position of a node using: `graph.nodes[n]['pos']`. You will need this for calculating the heuristic distance.
> 8. We will provide some margin of error in grading the size of your 'Explored' set, but it should be close to the results provided by our reference implementation.

---
### Exercises
The following exercises will require you to implement several kinds of bidirectional searches. The benefits of these algorithms over uninformed or unidirectional search are more clearly seen on larger graphs. As such, during grading, we will evaluate your performance on the map of Romania included in this assignment.

For these exercises, we recommend you take a look at the following resources.

1. [A Star meets Graph Theory](https://github.gatech.edu/omscs6601/assignment_2_online/raw/master/resources/A%20Star%20meets%20Graph%20Theory.pdf)
2. [Bi Directional A Star - Slides](https://github.gatech.edu/omscs6601/assignment_2_online/raw/master/resources/Bi%20Directional%20A%20Star%20-%20Slides.pdf)
3. [Bi Directional A Star with Additive Approx Bounds](https://github.gatech.edu/omscs6601/assignment_2_online/raw/master/resources/Bi%20Directional%20A%20Star%20with%20Additive%20Approx%20Bounds.pdf)
4. [Bi Directional A Star](https://github.gatech.edu/omscs6601/assignment_2_online/raw/master/resources/Bi%20Directional%20A%20Star.pdf)
5. [Search Algorithms Slide Deck](https://github.gatech.edu/omscs6601/assignment_2_online/raw/master/resources/Search%20Algorithms%20Slide%20Deck.pdf)
6. [Bi-directional Search, Piazza Spring ‘17](https://docs.google.com/document/d/14Wr2SeRKDXFGdD-qNrBpXjW8INCGIfiAoJ0UkZaLWto/pub)

#### Exercise 1: Bidirectional uniform-cost search

_[15 points]_

Implement bidirectional uniform-cost search. Remember that this requires starting your search at both the start and end states.

`bidirectional_ucs()` should return the path from the start node to the goal node (as a list of nodes).

> **Notes**:
> 1. You need to include start and goal in the path. Make sure the path returned is from start to goal and not in the reverse order.
> 2. **If your start and goal are the same then just return [].**
> 3. The above are just to keep your results consistent with our test cases.
> 4. You can access all the neighbors of a given node by calling `graph[node]`, or `graph.neighbors(node)` ONLY. 
> 5. You can access the weight of an edge using: `graph.get_edge_weight(node_1, node_2)`. Not using this method will result in your explored nodes count being higher than it should be.
> 6. You are not allowed to maintain a cache of the neighbors for any node. You need to use the above mentioned methods to get the neighbors and corresponding weights.
> 7. We will provide some margin of error in grading the size of your 'Explored' set, but it should be close to the results provided by our reference implementation.

#### Exercise 2: Bidirectional A* search

_[20 points]_

Implement bidirectional A* search. Remember that you need to calculate a heuristic for both the start-to-goal search and the goal-to-start search.

To test this function, as well as using the provided tests, you can compare the path computed by bidirectional A* to bidirectional UCS search above.
`bidirectional_a_star()` should return the path from the start node to the goal node, as a list of nodes.

> **Notes**:
> 1. You need to include start and goal in the path.
> 2. **If your start and goal are the same then just return [].**
> 3. The above are just to keep your results consistent with our test cases.
> 4. You can access all the neighbors of a given node by calling `graph[node]`, or `graph.neighbors(node)` ONLY. 
> 5. You can access the weight of an edge using: `graph.get_edge_weight(node_1, node_2)`. Not using this method will result in your explored nodes count being higher than it should be.
> 6. You are not allowed to maintain a cache of the neighbors for any node. You need to use the above mentioned methods to get the neighbors and corresponding weights.
> 7. You can access the (x, y) position of a node using: `graph.nodes[n]['pos']`. You will need this for calculating the heuristic distance.
> 8. We will provide some margin of error in grading the size of your 'Explored' set, but it should be close to the results provided by our reference implementation.

#### Exercise 3: Tridirectional UCS search

_[19 points]_

Implement tridirectional search in the naive way: starting from each goal node, perform a uniform-cost search and keep
expanding until two of the three searches meet. This should be one continuous path that connects all three nodes.

For example, suppose we have goal nodes [a,b,c]. Then what we want you to do is to start at node a and expand like in a normal search. However, notice that you will be searching for both nodes b and c during this search and a similar search will start from nodes b and c. Finally, please note that this is a problem that can be accomplished without using 6 frontiers, which is why we stress that **this is not the same as 3 bi-directional searches.**

`tridirectional_search()` should return a path between all three nodes. You can return the path in any order. Eg.
(1->2->3 == 3->2->1). You may also want to look at the [Tri-city search challenge question on Canvas](https://gatech.instructure.com/courses/151546/pages/45-challenge-question-revisited?module_item_id=806646).

> **Notes**:
> 1. You need to include start and goal in the path.
> 2. **If all three nodes are the same then just return [].**
> 3. **If there are 2 identical goals (i.e. a,b,b) then return the path [a...b] (i.e. just the path from a to b).**
> 4. The above are just to keep your results consistent with our test cases.
> 5. You can access all the neighbors of a given node by calling `graph[node]`, or `graph.neighbors(node)` ONLY. 
> 6. You can access the weight of an edge using: `graph.get_edge_weight(node_1, node_2)`. Not using this method will result in your explored nodes count being higher than it should be.
> 7. You are not allowed to maintain a cache of the neighbors for any node. You need to use the above mentioned methods to get the neighbors and corresponding weights.
> 8. We will provide some margin of error in grading the size of your 'Explored' set, but it should be close to the results provided by our reference implementation.

#### Exercise 4: Upgraded Tridirectional search

_[15 points]_

This is the heart of the assignment. Implement tridirectional search in such a way as to consistently improve on the
performance of your previous implementation. This means consistently exploring fewer nodes during your search in order
to reduce runtime. Keep in mind, we are not performing 3 bidirectional A* searches. We are searching from each of the goals towards the other two goals, in the direction that seems most promising.

The specifics are up to you, but we have a few suggestions:
 * Tridirectional A*
 * choosing landmarks and pre-computing reach values
 * ATL (A\*, landmarks, and triangle-inequality)
 * shortcuts (skipping nodes with low reach values)

`tridirectional_upgraded()` should return a path between all three nodes.

> **Notes**:
> 1. You need to include start and goal in the path.
> 2. **If all three nodes are the same then just return [].**
> 3. **If there are 2 identical goals (i.e. a,b,b) then return the path [a...b] (i.e. just the path from a to b).**
> 4. The above are just to keep your results consistent with our test cases.
> 5. You can access all the neighbors of a given node by calling `graph[node]`, or `graph.neighbors(node)` ONLY. 
> 6. You can access the weight of an edge using: `graph.get_edge_weight(node_1, node_2)`. Not using this method will result in your explored nodes count being higher than it should be.
> 7. You are not allowed to maintain a cache of the neighbors for any node. You need to use the above mentioned methods to get the neighbors and corresponding weights.
> 8. You can access the (x, y) position of a node using: `graph.nodes[n]['pos']`. You will need this for calculating the heuristic distance.
> 9. We will provide some margin of error in grading the size of your 'Explored' set, but it should be close to the results provided by our reference implementation.
     
     
#### Final Task: Return your name
_[1 point]_

A simple task to wind down the assignment. Return your name from the function aptly called `return_your_name()`.


### The Race!

Here's your chance to show us your best stuff. This part is mandatory if you want to compete in the race for extra credit. Implement `custom_search()` using whatever strategy you like.
**More details will be posted soon on Piazza.**

**Bonus points are added to the grade for this assignment, not to your overall grade.**

The Race! will be based on Atlanta Pickle data.

## References

Here are some notes you might find useful.
1. [Gradescope: Error Messages](https://docs.google.com/document/d/1hykYneVoV_JbwBjVz9ayFTA6Yr3pgw6JBvzrCgM0vyY/pub)
2. [Bi-directional Search](https://docs.google.com/document/d/14Wr2SeRKDXFGdD-qNrBpXjW8INCGIfiAoJ0UkZaLWto/pub)
3. [Using Landmarks](https://docs.google.com/document/d/1YEptGbSYUtu180MfvmrmA4B6X9ImdI4oOmLaaMRHiCA/pub)
