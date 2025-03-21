import pygame
import yaml
from LogicClasses.OpenMapFileYaml import openMapFileYaml
from UIClasses.LoadedAstarAlgorithm import loadedAstarAlgorithm
from UIClasses.LoadedDijkstras import loadedDijkstrasAlgorithm

from UIClasses.draw_text import draw_text

def DijkstrasOptionsPage(screen,userText):
    running = False
    running = True
    textFont = pygame.font.SysFont("Rockwell",20, bold = True, italic = True)
    textFontTitle = pygame.font.SysFont("Rockwell",35, bold = True, italic = True)

    StartNodeRect = pygame.Rect(750,300,250,50)
    EndNodeRect = pygame.Rect(750,450,250,50)
    ConfirmRect = pygame.Rect(1300,375,250,50)
    BackRect = pygame.Rect(1300,1000,250,50)
    QuitRect = pygame.Rect(1350,1000,250,50)
    userText = "testmapDijkstra"
    loadedMap = openMapFileYaml(userText)
    print(loadedMap)
    ListOfNodes = []
    # set to choose which text box is active at one time
    start_bool = False
    Goal_bool = False
    startText = ""
    goalText = ""
    #print(loadedMap)
    #outputs the nodes in the map

    for node in loadedMap.nodes:
        #print("\n\n Nodes: \n\n")
        #print(type(node.get_xCoordinate()))
        nodeName = node.get_nodeName()
        ListOfNodes.append(nodeName)
    print(ListOfNodes)


    while running:
            mx,my = pygame.mouse.get_pos()
            screen.fill((50, 125, 168))
            pygame.display.set_caption("Dijkstras ConfigurationPage Page:")
            draw_text(screen,"Select Targets for your map: ",textFontTitle,(0,0,0),750,160)
            draw_text(screen,"Starting Node: ",textFontTitle,(0,0,0),750,250)
            pygame.draw.rect(screen,(180, 185, 194),StartNodeRect)
            startTextSurface = textFont.render(startText,True,"white")
            screen.blit(startTextSurface,(750,300))

            draw_text(screen,"Goal Node: ",textFontTitle,(0,0,0),750,400)
            pygame.draw.rect(screen,(180, 185, 194),EndNodeRect)
            goalTextSurface = textFont.render(goalText,True,"white")
            screen.blit(goalTextSurface,(750,450))

            pygame.draw.rect(screen,(180, 185, 194),ConfirmRect)
            draw_text(screen,"CONFIRM",textFontTitle,(0,0,0),1300,375)
            
            pygame.draw.rect(screen,(180, 185, 194),BackRect)
            draw_text(screen,"Back",textFontTitle,(0,0,0),1300,1000)
            pygame.draw.rect(screen,(180, 185, 194),QuitRect)
            draw_text(screen,"Quit",textFontTitle,(0,0,0),1350,1000)
            




            draw_text(screen,"List Of nodes in Map:",textFontTitle,(0,0,0),50,300)
            draw_text(screen,userText,textFontTitle,(0,0,0),50,400)
            # using enumerate i can add pos as an index to my for loop, this allows me to increment the ycoord
            for pos, node in enumerate(ListOfNodes):
                dataSurface = textFont.render(node,True,"white")
                screen.blit(dataSurface,(50,500 + pos * 25))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if StartNodeRect.collidepoint(mx,my):
                        start_bool = True
                        Goal_bool = False
                    if EndNodeRect.collidepoint(mx,my):
                         start_bool = False
                         Goal_bool = True
                    if event.button == 1:
                        click = True
                    if ConfirmRect.collidepoint((mx,my)):
                        if click:
                            print(userText)
                            print("Click page registered.")
                            mapName = userText
                            #loadedBreadthFirstSearch(screen)
                            loadedDijkstrasAlgorithm(screen,startText,goalText)

                if event.type == pygame.KEYDOWN:
                    if start_bool:
                        if event.key == pygame.K_BACKSPACE:
                            startText = startText[:-1]
                        else:
                            startText += event.unicode
                    if Goal_bool:
                        if event.key == pygame.K_BACKSPACE:
                            goalText = goalText[:-1]
                        else:
                            goalText += event.unicode
                

                        
                     

            pygame.display.flip()

                