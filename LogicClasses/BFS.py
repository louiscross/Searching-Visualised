#This will form as the Breadth First search file
#Deque is a much more efficient queue for python
from collections import deque
import time

# Although nodes have weights, in BFS weights are not accounted for 

def breadthFirstSearch(Map,Node):
    #Initialise queue and visited nodes
    #need to set queues to set() not leave as none otherwise error for Nonetype
    visitedNodes = set()
    queue = deque()

    #Pushes the node parameter/start node onto the queue 
    queue.append(Node)
    print("start node : " + Node.get_nodeName())
    print("\n\n")

    visitedNodes.add(Node)
    cursize = []
    start = time.time()
    while queue:
        cur = queue.popleft()
        cursize.append(cur)
        print("Amount of nodes visited: " + str(len(cursize)))
        print("\n")

        #print(cursize)
        print("Visiting node: " + cur.nodeName)

        for neighbourName in cur.adjacencies:
            print("Neighbour: " + neighbourName["Node"])
            neighbour = Map.getNodeByName(neighbourName["Node"])
            if neighbour not in visitedNodes:
                queue.append(neighbour)
                visitedNodes.add(neighbour)
                print("Visiting neighbor:" + neighbour.nodeName)
                print("\n\n")

    end = time.time()
    print("time Taken: "+ str((end-start)))
    return cursize, 
