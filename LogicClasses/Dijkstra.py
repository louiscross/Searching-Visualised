import collections
from queue import PriorityQueue

def Dijkstra(map,startNode,goalNode):
    #initialises lists needed
    priorityqueue = PriorityQueue()
    visited = set()
    distance = {}
    unvisited = []
    bestPathCur = {}
    print(map)
    print(map.getNodeByIndex(1))

    startNode = map.getNodeByName("A")
    goalNode = map.getNodeByName("Z")
    #populates the visited and distance list/dictionary
    for node in map.nodes:
        nodeName = node.get_nodeName()
        unvisited.append(nodeName)
        #sets all distances very high to start so can be replaced later
        distance[nodeName] = 1000000000
    # start node will have distance set to 0
    distance[startNode.get_nodeName()] = 0
    print(unvisited)
    priorityqueue.put((startNode.get_nodeName(),0))
    CurNode = startNode
    CurDistance = distance[startNode.get_nodeName()]



    while priorityqueue.qsize() > 0:
        print(priorityqueue.qsize())
        #removes node with lowest distance
        CurNode, CurDistance = priorityqueue.get()
        #if CurNode == goalNode.get_nodeName():
        #     print("Goal Node Reached!")
        #     return
        print("CURRENT NODE / WEIGHT:")
        print(CurDistance)
        print(CurNode)
        print("\n\n")

        if CurDistance > distance[CurNode]:
             continue
                                  

        # if the current node is inside the visited loop, then pass / skip the rest of the while loop

        for neighbour in map.getNodeByName(CurNode).adjacencies:
                
                print("NEIGHBOUR: ")
                print(neighbour["Node"])
                weight = neighbour["Weight"]
                print(weight)
                totalDistance = CurDistance + weight

                # condition to check if the route to the neighbour is cheaper than the current route, this is why start node needs to be 0
                if totalDistance < distance[neighbour["Node"]]:
                    print("Shorter Path found:")
                    distance[neighbour["Node"]] = totalDistance

                    #updating the best path to show the node
                    bestPathCur[neighbour["Node"]] = CurNode
                    priorityqueue.put((neighbour["Node"],distance[neighbour["Node"]]))
                    print(neighbour["Node"] + str(distance[neighbour["Node"]]))
                    
    #print(bestPathCur)
    bestPath = []
    finalGoal = goalNode.get_nodeName()
    #print(finalGoal)
    while True:
         bestPath.insert(0,finalGoal)
         #print(bestPath)
         if finalGoal == startNode.get_nodeName():
              break
         finalGoal = bestPathCur[finalGoal]
         #print("final goal:")
         #print(finalGoal)
         if finalGoal is None:
              break
         
    print(" This is the best Path: ")
    print(bestPath)
    print(" Shortest Paths: ")
    print(distance)
    return bestPath

def shortestPath(bestPath):
     return bestPath

def shortestPaths(distance):
     return distance
