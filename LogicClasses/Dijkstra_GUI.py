import collections
from queue import PriorityQueue
import pygame


def DijkstraGUI(screen,map,startNode,goalNode):
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
                    CurNodeUI = map.getNodeByName(CurNode)
                    NeighbourNodeUI = map.getNodeByName(neighbour["Node"])
                    pygame.draw.circle(screen,(235, 193, 115),(CurNodeUI.get_xCoordinate(),CurNodeUI.get_yCoordinate()),10)
                    pygame.time.delay(1000)
                    pygame.draw.line(screen,(0,0,0),((CurNodeUI.xCoordinate,CurNodeUI.yCoordinate)),(NeighbourNodeUI.xCoordinate,NeighbourNodeUI.yCoordinate),3)
                    pygame.draw.circle(screen,(235, 193, 115),(CurNodeUI.get_xCoordinate(),CurNodeUI.get_yCoordinate()),10)
                    pygame.display.flip()
                    pygame.draw.circle(screen,(161, 235, 115),(NeighbourNodeUI.get_xCoordinate(),NeighbourNodeUI.get_yCoordinate()),10)
                    pygame.display.flip()
                    pygame.time.delay(1000)
    #print(bestPathCur)
    bestPath = []
    finalGoal = goalNode.get_nodeName()
    #print(finalGoal)
    while True:
         bestPath.insert(0,finalGoal)
         #print(bestPath)
         if finalGoal == startNode.get_nodeName():
            for x in range (0,(len(bestPath)-1)):
                current = map.getNodeByName(bestPath[x])
                neighbour = map.getNodeByName(bestPath[x + 1])
                pygame.draw.line(screen,(248, 252, 3),((current.xCoordinate,current.yCoordinate)),(neighbour.xCoordinate,neighbour.yCoordinate),3)
                pygame.display.flip()
            pygame.time.delay(15000)
            break
         finalGoal = bestPathCur[finalGoal]
         #print("final goal:")
         #print(finalGoal)
         if finalGoal is None:
              break


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
    
    


    






    pass