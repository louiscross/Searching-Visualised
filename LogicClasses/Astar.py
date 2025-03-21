
#Going to do calcs with math import first, then hopefully when running will try pow method without import
import math
import time
import queue
from collections import deque
from LogicClasses.Map import Map
from LogicClasses.Node import Node



def AstarAlgorithm(map,startNode,goalNode):

    start = time.time()
    #currentNode = Node(startNode.nodeName(),startNode.xCoordinate(),startNode.yCoordinate(),startNode.weight(),startNode.directional(),startNode.adjacencies())
    # to calculate heurisitc we will find distance between coordinates of states ( current / goal)

    pqueue = deque()
    # add startnode to queue
    pqueue.append(startNode)
    curlist = []
    curPriority = {}
    BestPaths = {}
    Heuristic = math.sqrt(((int(goalNode.get_xCoordinate()) - int(startNode.get_xCoordinate()))**2) + ((int(goalNode.get_yCoordinate()) - int(startNode.get_yCoordinate()))**2))
    #print(Heuristic)
    minvalue = 10000
    minname = ""
    

    while pqueue:
        cur = pqueue.popleft()
        curlist.append(cur)
        visitedNodes = []
        for neighboursNames in cur.adjacencies:
            # gets neighbour(s) in list
            neighbour = map.getNodeByName(neighboursNames)
            #print(neighbour)
            #get node for said adjacency.
            Heuristic = math.sqrt(((int(goalNode.get_xCoordinate()) - int(neighbour.get_xCoordinate()))**2) + ((int(goalNode.get_yCoordinate()) - int(neighbour.get_yCoordinate()))**2))
            priorityHeuristic = int(Heuristic) + int(cur.get_weight())
            currentNodeName = cur.get_nodeName()


            curPriority.update({neighboursNames:priorityHeuristic})
            print("Heuristic from " + str(currentNodeName) + " to " + neighboursNames + " is: " + str(priorityHeuristic))
            print(curPriority)

        #
        for neighbour,heuristic in curPriority.items():
            if heuristic < minvalue:
                minvalue = heuristic
                minname = neighbour
                print("best path to go is: " + minname)

                ## -- End State -- #
                if minname == goalNode.get_nodeName():
                    print("FINISHED ROUTE")
                    for names in curlist:
                        print(names.get_nodeName())
                    print(goalNode.get_nodeName())
                    return
                
        print("OVERALL best path to go is: " + minname)
        pqueue.append(map.getNodeByName(minname))
        del curPriority[minname]
        print("deleting : " + minname)
        















    return