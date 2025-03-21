
#Going to do calcs with math import first, then hopefully when running will try pow method without import
import math
import time
import queue
from collections import deque
from LogicClasses.Map import Map
from LogicClasses.Node import Node
import pygame



def AstarAlgorithmGUI(screen,map,startNode,goalNode):
    running = False
    running = True
    textFontMap = pygame.font.SysFont("Rockwell",20, bold = True, italic = True)
    mapHeight = 1080
    mapWidth = 1920
    x = 0
    startNode = map.getNodeByName(str(startNode))
    print(startNode)

    goalNode = map.getNodeByName(str(goalNode))
    print(goalNode)
    print(type(goalNode))

    #loads map based on input given prior

    #new window
    #while running:
    clock = pygame.time.Clock()
    clock.tick(60)
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
            print("neighbours name: " + str(neighboursNames))
            print(type(neighboursNames))
            neighbour = map.getNodeByName(str(neighboursNames['Node']))
            print(neighbour)
            print(type(neighbour))
            #get node for said adjacency.
            Heuristic = math.sqrt(((int(goalNode.get_xCoordinate()) - int(neighbour.get_xCoordinate()))**2) + ((int(goalNode.get_yCoordinate()) - int(neighbour.get_yCoordinate()))**2))
            print("cur" + str(cur))
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
        weight = neighbour.get_weight()
        if weight == None:
            weight = 1
        pygame.draw.circle(screen,(235, 193, 115),(cur.get_xCoordinate(),cur.get_yCoordinate()),weight*3)
        pygame.time.delay(1000)
        pygame.draw.line(screen,(0,0,0),((cur.xCoordinate,cur.yCoordinate)),(neighbour.xCoordinate,neighbour.yCoordinate),3)
        pygame.draw.circle(screen,(235, 193, 115),(cur.get_xCoordinate(),cur.get_yCoordinate()),weight*3)
        pygame.display.flip()
        pygame.draw.circle(screen,(161, 235, 115),(neighbour.get_xCoordinate(),neighbour.get_yCoordinate()),weight*3)
        pygame.display.flip()
        pygame.time.delay(1000)
        del curPriority[minname]
        print("deleting : " + minname)
  
    return