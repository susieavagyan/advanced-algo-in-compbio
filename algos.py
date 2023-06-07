import math

#####Needlman-Wunsch#######
def needwunsch(s, t):
    m, n = len(s), len(t)
    if m*n==0:
        return m+n
    DP = [[0 for x in range(n + 1)] for x in range(m + 1)]
    for i in range(m+1):
        DP[i][0] = i
    for j in range(n+1):
        DP[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            left = DP[i-1][j] + 1
            down = DP[i][j-1] + 1
            left_down = DP[i-1][j-1]
            if s[i-1] != t[j-1]:
                left_down += 1
            DP[i][j] = min(left, down, left_down)
    edit_distance = DP[m][n]
    return edit_distance, DP
#############################




###Banding DP######
def banding(s,t,m,n, b): # set b to start from the difference in length of two strings so that it initially contains the last cell of regular DP matrix
    if b < 0: 
        ValueError
    if b == 0:
        b = 1
    DP = {}
    for i in range(b+1): # fill in the first row and column of the band
        DP[i,0] = i
        DP[0,i] = i
   

    # Fill in the DP matrix
    for i in range(1, m+1): # iterate i until the length of s
        for j in range(1, n+1): # iterate i until the length of t
            left = math.inf
            up = math.inf
            if j >= i - b and i >= j-b: # check to not get out of band's borders
                diag = DP[i-1, j-1] + (0 if s[i-1] == t[j-1] else 1)
                if i != j - b: # if i equals j-b then we are in the top border, so no value is accessible vertically
                    up = DP[i-1, j] + 1
                if j != i - b: # if j equals i-b then we are in the bottom border, so no value is accessible horizontally
                    left = DP[i, j-1] + 1
                DP[i, j] = min(diag, up, left)
        
    # Check if the last cell of DP matrix is greater than (or equal to?) b
    # if all(v >= b for v in DP.values()): # check of DP contaims any values less than b
    if (DP[m,n] > b):
        return banding(s,t,m,n,2*b) # call the function with 2*b

    edit_distance = DP[m,n]

    # return edit_distance, DP, b
    return edit_distance, DP
    
##########################


####Djiksta####
# class PriorityQueue:
#     def __init__(self):
#         self.heap = []

#     def insert(self, key, value):
#         for i, (k, v) in enumerate(self.heap):
#             if k == key:
#                 if value < v:
#                     self.heap[i] = (key, value)
#                     self._bubble_up(i)
#                 return
#         self.heap.append((key, value))
#         self._bubble_up(len(self.heap) - 1)

#     def pop(self):
#         if not self.heap:
#             raise IndexError("Priority queue is empty")
#         self._swap(0, len(self.heap) - 1)
#         min_key, min_value = self.heap.pop()
#         self._bubble_down(0)
#         return min_key, min_value

#     def _bubble_up(self, i):
#         while i > 0:
#             parent = (i - 1) // 2
#             if self.heap[i][1] < self.heap[parent][1]:
#                 self._swap(i, parent)
#                 i = parent
#             else:
#                 break

#     def _bubble_down(self, i):
#         while 2 * i + 1 < len(self.heap):
#             left_child = 2 * i + 1
#             right_child = 2 * i + 2
#             min_child = left_child
#             if right_child < len(self.heap) and self.heap[right_child][1] < self.heap[left_child][1]:
#                 min_child = right_child
#             if self.heap[min_child][1] < self.heap[i][1]:
#                 self._swap(i, min_child)
#                 i = min_child
#             else:
#                 break

#     def _swap(self, i, j):
#         self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

#     def is_empty(self):
#         return len(self.heap) == 0

import heapq

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def is_empty(self):
        return len(self._queue) == 0

    def insert(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def pop(self):
        if not self.is_empty():
            priority, _, (key, value) = heapq.heappop(self._queue)
            return (key, value), priority
        else:
            raise IndexError("Priority queue is empty")


    
def dijkstra(s, t, m,n):
    # initialize priority queue
    queue = PriorityQueue()
    queue.insert((0,0), 0)

    # initialize adjacency list
    adj_list = {}

    # initialize distance dict
    dist = {}
    dist[(0,0)] = 0

    while queue: 
        # pop key and value for minimum value 
        key, value = queue.pop()

        # check if the key is the index m,n
        if key == (m,n):
            return value, dist
        
        # define adjacent nodes of the key with their weights
        if key not in adj_list:
                adj_list[key] = []

        # check if the key is an index in the last row or last column 
        if key[0] != m and key[1] != n:
            adj_list[key].append(((key[0]+1,key[1]), 1))
            adj_list[key].append(((key[0],key[1]+1), 1))
            adj_list[key].append(((key[0]+1,key[1]+1), (1 if s[key[0]] != t[key[1]] else 0)))
        elif key[0] == m:
            adj_list[key].append(((key[0],key[1]+1), 1))
        elif key[1] == n:
            adj_list[key].append(((key[0]+1,key[1]), 1))

      

        # iterate over the neighbors and insert the values into the priority queue
        for neighbor, weight in adj_list.get(key, []):
                if neighbor not in dist:
                    dist[neighbor] = value+weight
                    queue.insert(neighbor, value+weight)
                elif dist[neighbor] > value+weight:
                    dist[neighbor] = value+weight
                    queue.insert(neighbor, value+weight)

                
    return -1

#############



#####A star########
def astar_seed(A,B, m, n, k):

#push all kmers from B to a hash table H (for finding seed matches)
    H ={B[j:j+k] for j in range(len(B)-k+1) } 

    #split A to seeds S
    S = [A[i:i+k] for i in range(0, len(A), k)]

    #for each seed s, let matches[s] be 1 if s matches at least once in B by a lookup in H (using the hash table)
    matches = [1 if s in H else 0 for s in S]

    # partial sums
    partial_sums = []
    partial_sum = 0
    for idx in range(len(matches)-1,-1, -1):
        partial_sum +=  (1-matches[idx])
        partial_sums.append(partial_sum)

    partial_sums = partial_sums[::-1]



    # #h number of seeds starting after i and cannot be matched. Use partial sums sum[s]:=matches[s..]=matches[s]+sum[s+1] for computing h(i,j) for O(1).

    def h(i,j):
    #     h(i,j) - approximating the edit distance between two suffixes
        return partial_sums[math.floor(i/k)-1]



    def a_star(A,B,m,n):
        """ 
        use A* algo to get shortest distance from src to sink vertices of graph g
        construct the edit graph on the fly

        g[v] - shortest distance from vertex src to vertex v (inf if not known)
        f[v] = g[v] + h(v) - where h(v) is the number of unmatchable upcoming seeds (starting after v[1]) for vertex u
        """

        # initialize priority queue
        queue = PriorityQueue()
        queue.insert((0,0), 0)

        # initialize adjacency list
        adj_list = {}

        # initialize g and f
        g = {} 
        f = {}
        g[(0,0)] = 0
        f[(0,0)] = 0  # f = g + h


        while queue: 
            # pop key and value for minimum value 
            key, value = queue.pop()

            # check if the key is the index m,n
            if key == (m,n):
                # return g[key], g, f
                return g[key], g
            
            # define adjacent nodes of the key with their weights
            if key not in adj_list:
                    adj_list[key] = []

            # check if the key is an index in the last row or last column 
            if key[0] != m and key[1] != n:
                adj_list[key].append(((key[0]+1,key[1]), 1))
                adj_list[key].append(((key[0],key[1]+1), 1))
                adj_list[key].append(((key[0]+1,key[1]+1), (1 if A[key[0]] != B[key[1]] else 0)))
            elif key[0] == m:
                adj_list[key].append(((key[0],key[1]+1), 1))
            elif key[1] == n:
                adj_list[key].append(((key[0]+1,key[1]), 1))

            # iterate over the neighbors and insert the values into the priority queue
            for neighbor, weight in adj_list.get(key, []):
                    g_n = g[key]+weight
                    f_n = g_n+h(neighbor[0], neighbor[1])
                    if neighbor not in f:
                        g[neighbor] = g_n
                        f[neighbor] = f_n
                        queue.insert(neighbor, f_n)
                    elif f[neighbor] > f_n:
                        g[neighbor] = g_n
                        f[neighbor] = f_n
                        queue.insert(neighbor, f_n)
                   
        return -1
    
    return a_star(A,B, len(A), len(B))









  

