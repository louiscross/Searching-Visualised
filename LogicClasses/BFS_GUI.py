#This will form as the Breadth First search file
#Deque is a much more efficient queue for python
from collections import deque
import time
import pygame

# Although nodes have weights, in BFS weights are not accounted for 

def breadthFirstSearchGUI(screen,loadedMap):
    running = False
    running = True
    textFontMap = pygame.font.SysFont("Rockwell",20, bold = True, italic = True)
    mapHeight = 1080
    mapWidth = 1920
    x = 0

    #loads map based on input given prior

    #new window
    #while running:
    clock = pygame.time.Clock()
    clock.tick(60)
    visitedNodes = set()
    queue = deque()
    Node = loadedMap.getNodeByName("C")

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
            neighbour = loadedMap.getNodeByName(neighbourName["Node"])
            if neighbour not in visitedNodes:
                queue.append(neighbour)
                visitedNodes.add(neighbour)
                print("Visiting neighbor:" + neighbour.nodeName)
                print("\n\n")
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

    end = time.time()
    print("time Taken: "+ str((end-start)))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
