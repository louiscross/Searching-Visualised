import collections
from queue import PriorityQueue
import math

def GreedyFirstSearch(map,startNode,goalNode):
    priorityqueue = PriorityQueue()
    visited = set()
    heuristic = {}
    unvisited = []
    startNode = map.getNodeByName("A")
    goalNode = map.getNodeByName("B")
    #populates the visited and distance list/dictionary
    for node in map.nodes:
        nodeName = node.get_nodeName()
        unvisited.append(nodeName)
        #sets all Heuristic very high to start so can be replaced later ( will be using manhattan heuristic )
        heuristic[nodeName] = 1000000000
    # start node will have distance set to 0
    heuristic[startNode.get_nodeName()] = 0
    print(heuristic)
    print("\n\n")
    print(unvisited)
    priorityqueue.put((startNode.get_nodeName(),0))
    CurNode = startNode
    CurDistance = heuristic[startNode.get_nodeName()]



    while priorityqueue.qsize() > 0:
        print("SIZE OF PQ IS : ")
        print(priorityqueue.qsize())
        print("\n")
        #removes node with lowest distance
        CurNode, CurHeuristic = priorityqueue.get()
        if CurNode == goalNode.get_nodeName():
             print("Goal Node Reached!")
             return
        print("CURRENT NODE / Heuristic:")
        print(CurHeuristic)
        print(CurNode)
        print("\n\n")

        # if the current node is inside the visited loop, then pass / skip the rest of the while loop
        if CurNode in visited:
            print("visited:" + str(CurNode))
            continue
        visited.add(CurNode)
        for neighbour in map.getNodeByName(CurNode).adjacencies:
                
                print("Current node & NEIGHBOUR & Heuristic: ")

                # Need to figure out the Heuristic Value between neighbours.
                currentHeuristic = map.getNodeByName(CurNode)
                neighbourHeuristic = map.getNodeByName(neighbour["Node"])
                heuristicValue = math.sqrt(((int(goalNode.get_xCoordinate()) - int(startNode.get_xCoordinate()))**2) + ((int(goalNode.get_yCoordinate()) - int(startNode.get_yCoordinate()))**2))
                print(currentHeuristic.get_nodeName(),neighbourHeuristic.get_nodeName(),heuristicValue)

                # condition to check if the route to the neighbour is cheaper than the current route, this is why start node needs to be 0
                print(heuristic[neighbour["Node"]])
                print(currentHeuristic)
                if CurHeuristic + heuristicValue < heuristic[neighbour["Node"]]:
                    print("Shorter Path found:")
                    heuristic[neighbour["Node"]] = CurHeuristic + heuristicValue

                    priorityqueue.put((neighbour["Node"],heuristic[neighbour["Node"]]))
                    print("Node: " + neighbour["Node"] + " Heuristic" + str(heuristic[neighbour["Node"]]))
    
    
    print(visited)

    pass