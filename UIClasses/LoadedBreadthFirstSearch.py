import pygame
from LogicClasses.BFS_GUI import breadthFirstSearchGUI
from LogicClasses.Node import Node
from LogicClasses.OpenMapFileYaml import openMapFileYaml
from UIClasses.draw_text import draw_text


def loadedBreadthFirstSearch(screen):
        running = False
        running = True
        textFontMap = pygame.font.SysFont("Rockwell",20, bold = True, italic = True)
        mapHeight = 1080
        mapWidth = 1920
        x = 0

        #loads map based on input given prior

        #new window
        while running:
                screen.fill((210, 214, 208))
                #pygame.display.flip()
                pygame.display.set_caption("Breadth First Search Simulation")
                userText = "testmap3"
                loadedMap = openMapFileYaml(userText)
                #print(loadedMap)
                #outputs the nodes in the map

                for node in loadedMap.nodes:
                    #print("\n\n Nodes: \n\n")
                    #print(type(node.get_xCoordinate()))
                    weight = node.get_weight()
                    # Some maps do not include a weight in the yaml files, therefore will cause error if left as NoneType
                    if weight == None:
                        weight = 1
                    
                    pygame.draw.circle(screen,(255,255,255),(node.get_xCoordinate(),node.get_yCoordinate()),weight*3)
                    draw_text(screen,node.get_nodeName(),textFontMap,(0, 0, 0),node.get_xCoordinate(),node.get_yCoordinate()-50)
                    draw_text(screen,str(node.get_weight()),textFontMap,(0, 0, 0),node.get_xCoordinate(),node.get_yCoordinate()+40)
                    adjacencies = node.get_adjacencies()
                    #print("\n\nAdjacencies")
                    #print(adjacencies)
                    #Drawing the Lines between Adjacencies
                    for relatives in node.adjacencies:
                        #print("Relatives: ")
                        #print(relatives)
                        newNode = Node([],[],[],[],[])
                        newNode = loadedMap.getNodeByName(relatives["Node"])
                        #print(newNode)
                        pygame.draw.line(screen,(255,255,255),((node.get_xCoordinate(),node.get_yCoordinate())),(newNode.get_xCoordinate(),newNode.get_yCoordinate()),1)

                    #print(node)
                pygame.display.flip()

                # can be used as a starting node (optional)
                # node = loadedMap.getNodeByIndex(4)

                #this function provides the bfs
                #breadthFirstSearch(loadedMap,node)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            click = True
                            breadthFirstSearchGUI(screen,loadedMap)