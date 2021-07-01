''' 
    Name: Matthew Chevannes
    ID: 620106393
'''
class PriorityQueue:
    
    def __init__(self):

        self.queue = []

    # ** FINISH THIS FUNCTION **
    # Should add element to priority queue
    def enqueue(self, el):
        self.queue.append(el)

   # for checking if the queue is empty
    def isempty(self):
        return len(self.queue) == 0   
 
    def heapify(self):
        self.queue = self.queue.sort(key=lambda x:x.f)


    # ** FINISH THIS FUNCTION **
    # Should take minmum element from priority queue and return element 
    def dequeue(self):
        if self.queue is not self.isempty():
            self.queue.pop(0)     


    def __str__(self):
        return ' '.join([str(i) for i in self.queue])
   

                




# ** ONLY DO THIS IF YOU WANT BONUS MARKS**
# MinHeap allows you to extract elements in O(logn) time
# Feel free to add more helper functions
class MinHeap:
    
    
    def __init__(self):
        self.heap = []
    
    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    # ** FINISH THIS FUNCTION **
    # Adds element to heap

    def enqueue(self, el):
        self.heap.append(el)
    
    
    
    # ** FINISH THIS FUNCTION **
    # Should take minmum element from heap and return element

    def dequeue(self):
        if not self.isempty():
            return self.heap.pop(0)

    def heapify(self):
        try: 

   


class Node:
    
    def __init__(self, label, parent):
        self.label = label
        self.parent = parent # parent node
        self.g = 0 # total path cost from start node
        self.f = 0 # final cost
        self.h = 0 # heuristic distance
    
    # allows you to compare two nodes using <
    def __lt__(self, other):
         return self.f < other.f
        
    def __str__(self):
        return str((self.label, self.f))

# Returns the children/negihbours of a node in the graph including path cost
# e.g. [('A', 20), ('B', 30), ('D', 50)]
# graph - dictionary of nodes and edges
# node - label of node
def get_children(graph, node):
    children = []
    if node in graph.keys():
        children = list(graph[node].items())
    return children

def expandnodes(node, lst):
    children_nodes = []
    for node in len(range(lst)):
        child = Node(lst[node][0],node)
        child.g = lst[node][1]
        children_nodes.append(child)
        
def reconstruct(initial_state, goal_state):
    current_state = goal_state
    path = []
    while (not current_state.label ==  initial_state.label):
        path.append(current_state.label)
        current_state = current_state.parent
    path.append(initial_state.label)
    return list(reversed(path))

# ** FINISH THIS FUNCTION **
# Should return a list representing the path from start to goal
# e.g ['A', 'B', 'G'] would be a possible solution starting from start node A to goal node G
# If there is no path from start to goal, the function should return empty list
# path_graph - dictionary of nodes and edges
# heurist_dist - dictionary of heuristic distance to goal
# start - label for start node e.g. 'A'
# goal - label for goal node e.g. 'G'
# search_type - can be one of UCS, Greedy, A-Start
# fringe_type - data structure used for fring can be one of p_queue, heap
def path_find(path_graph, heurist_dist, start, goal, 
				search_type='UCS', fringe_type='p_queue'):
    
    if fringe_type == 'p_queue':
        fringe = PriorityQueue()
    else:
        fringe = MinHeap()
    
    start_node = Node(start, None)
    goal_node = Node(goal, None)
    
    visited = []
   
    goal_found = False
    fringe.enqueue(start_node) # add the start node to fringe
    if fringe.isempty():
        return 0
    current_node = fringe.dequeue()
    if current_node.label == goal_node.label:
        goal_found = True
        return reconstruct(current_node, goal_node)
    else:
        if search_type == 'UCS':
            children = get_children(path_graph, current_node)
            children_nodes = expandnodes(current_node ,children)
            fringe.append(children_nodes)
            fringe.heapify()
            visited.append(current_node.label)           
            next_node = fringe.dequeue()
            next_node.f += next_node.g
            if fringe_type == 'p_queue':
                return path_find(path_graph,heurist_dist,next_node.label,goal_node.label,search_type='UCS', fringe_type='p_queue')
            return path_find(path_graph,heurist_dist,next_node.label,goal_node.label,search_type='UCS', fringe_type='heap')
        elif search_type == 'Greedy':
            children = get_children(path_graph, current_node)
            children_nodes = expandnodes(current_node ,children)
            fringe.append(children_nodes)            
            for node in len(range(children_nodes)):
                if node.label in heurist_dist:
                    node.h = heurist_dist[node][1]
                    node.f = node.h
            fringe.heapify()
            visited.append(current_node.label)
            next_node = fringe.dequeue()
            if fringe_type == 'p_queue':
                return path_find(path_graph,heurist_dist,next_node.label,goal_node.label,search_type='Greedy', fringe_type='p_queue')
            return path_find(path_graph,heurist_dist,next_node.label,goal_node.label,search_type='Greedy', fringe_type='heap')
        elif search_type == 'A-Star':
            children = get_children(path_graph, current_node)
            children_nodes = expandnodes(current_node ,children)
            fringe.append(children_nodes)
            for node in len(range(children_nodes)):
                if node.label in heurist_dist:
                    node.h = heurist_dist[node][1]
                    node.f = node.h + node.g
            fringe.heapify()
            visited.append(current_node.label)
            next_node = fringe.dequeue()
            if fringe_type == 'p_queue':
                return path_find(path_graph,heurist_dist,next_node.label,goal_node.label,search_type='A-Star', fringe_type='p_queue')
            return path_find(path_graph,heurist_dist,next_node.label,goal_node.label,search_type='A-Star', fringe_type='heap')
