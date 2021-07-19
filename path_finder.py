''' 
    Name: Matthew Chevannes
    ID: 620106393
'''
class PriorityQueue:
    
    def __init__(self):
        self.queue = []
    
    def prioritize(self):
        l = len(self.queue)
        for index in range(0, l):
            for i in range(0, l-index-1):
                if (self.queue[i] > self.queue[i + 1]):
                    d = self.queue[i]
                    self.queue[i] = self.queue[i +1]
                    self.queue[i +1]= d

    def astarprioritize(self):
        l = len(self.queue)
        for index in range(0, l):
            for i in range(0, l-index-1):
                if (self.queue[i].compare(self.queue[i + 1])):
                    d = self.queue[i]
                    self.queue[i] = self.queue[i +1]
                    self.queue[i +1]= d

    def dequeue(self):
        self.prioritize()
        return self.queue.pop(0)        


    def astardequeue(self):
        self.astarprioritize()
        return self.queue.pop(0)   
        
    def enqueue(self, el):
        self.queue.append(el)

    def isempty(self):
        return len(self.queue) == 0




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

    def compare(self,node):
        return self.g > node.g

    def setHeuristic(self,x):
        self.h = x  

    def parentnode(self):
        return self.parent

    def getLabel(self):
        return  self.label

    def calculateCost(self, value):
        self.f = self.parent.f + value   

    def setScore(self):
        self.g = self.h + self.f


# Returns the children/negihbours of a node in the graph including path cost
# e.g. [('A', 20), ('B', 30), ('D', 50)]
# graph - dictionary of nodes and edges
# node - label of node
def get_children(graph, node):
    children = []
    if node in graph.keys():
        children = list(graph[node].items())
    return children

def heuristic(heurdict, label):
        if label in heurdict.keys():
            value = heurdict[label]
        return value


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
    path = []
    #Uniform Cost Search
    if search_type == 'UCS':
        while not fringe.isempty():
            current = fringe.dequeue()
            if current.getLabel() == goal:
                path.append(goal)
                while not current.parentnode() == None:
                    plabel = current.parentnode().getLabel()
                    path.insert(0, plabel)
                    current = current.parentnode()
    
                return path
            if current.getLabel() not in visited:
                branch = get_children(path_graph, current.getLabel())
                for route in branch:
                    child = Node(route[0], current)
                    child.calculateCost(route[1])
                    if child.getLabel() not in visited:
                        fringe.enqueue(child)
                visited.append(current.getLabel())

    # expanding the neighbours into nodes and traversing based on the function f(n)= g(n)
            if current.getLabel() not in visited:
                branch = get_children(path_graph, current.getLabel())
                for route in branch:
                    child = Node(route[0], current)
                    child.calculateCost(route[1])
                    if child.getLabel() not in visited:
                        fringe.enqueue(child)
                visited.append(current.getLabel())

    # Greedy (best first search)
    elif search_type == 'Greedy':

        path.append(start)
        while not goal in path:
            node = path[-1]
            branch = get_children(path_graph, node)
            heurvalues = []
            for route in branch:
                if route[0] not in visited:
                    hv = heuristic(heurist_dist, route[0])
                    heurvalues.append([route[0], hv])
            visited.append(node)
            heurvalues = sorted(heurvalues, key = lambda x: x[1])
            path.append(heurvalues[0][0])
        return path

    # A-Star Search
    elif search_type == 'A-Star':
        while not fringe.isempty():
            current = fringe.astardequeue()
            if current.getLabel() == goal:
                path.append(goal)
                while not current.parentnode() == None:
                    plabel = current.parentnode().getLabel()
                    path.insert(0, plabel)
                    current = current.parentnode()
    
                return path
            if current.getLabel() not in visited:
                branch = get_children(path_graph, current.getLabel())
                for route in branch:
                    child = Node(route[0], current)
                    child.calculateCost(route[1])
                    child.setHeuristic(heuristic(heurist_dist, route[0]))
                    child.setScore()
                    if child.getLabel() not in visited:
                        fringe.enqueue(child)
                visited.append(current.getLabel())
