import pygame
from LogicClasses.Dijkstra import Dijkstra
from LogicClasses.GreedyFirstSearch import GreedyFirstSearch
from LogicClasses.OpenMapFileYaml import openMapFileYaml
from UIClasses.AstarOptionsPage import AstarOptionsPage
from UIClasses.DijkstrasOptionsPage import DijkstrasOptionsPage
from UIClasses.LoadedBreadthFirstSearch import loadedBreadthFirstSearch

from UIClasses.draw_text import draw_text
from UIClasses.loadedGreedyFirstSearch import loadedGreedyFirstSearch

def AlgorithmPage(screen,userText):
    running = False
    running = True
    textFont = pygame.font.SysFont("Rockwell",20, bold = True, italic = True)
    textFontTitle = pygame.font.SysFont("Rockwell",35, bold = True, italic = True)

    AStarRect = pygame.Rect(1200,500,250,50)
    BreadthFirstSearchRect = pygame.Rect(1200,250,250,50)
    GreedyFirstSearchRect = pygame.Rect(700,250,250,50)
    DijkstraRect = pygame.Rect(700,500,250,50)

    BackPageRect = pygame.Rect(300,250,250,50)
    QuitRect = pygame.Rect(300,500,250,50)

    #loads map based on input given prior

    #new window
    
    while running:
            mx,my = pygame.mouse.get_pos()
            screen.fill((50, 125, 168))
            pygame.display.set_caption("Algorithm Choice Page:")
            draw_text(screen,"Select Type of Algorithm to Run: ",textFontTitle,(0,0,0),650,160)

            pygame.draw.rect(screen,(180, 185, 194),AStarRect)
            pygame.draw.rect(screen,(180, 185, 194),BreadthFirstSearchRect)
            pygame.draw.rect(screen,(180, 185, 194),GreedyFirstSearchRect)
            pygame.draw.rect(screen,(180, 185, 194),DijkstraRect)

            pygame.draw.rect(screen,(180, 185, 194),BackPageRect)
            pygame.draw.rect(screen,(180, 185, 194),QuitRect)


            draw_text(screen,"A* Algorithm",textFont,(0,0,0),1200,500)
            draw_text(screen,"Breadth First Search",textFont,(0,0,0),1200,250)
            draw_text(screen,"Greedy First Search",textFont,(0,0,0),700,250)
            draw_text(screen,"Dijkstra Algorithm",textFont,(0,0,0),700,500)

            draw_text(screen,"Go Back",textFont,(0,0,0),300,250)
            draw_text(screen,"Quit",textFont,(0,0,0),300,500)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

                    if AStarRect.collidepoint((mx,my)):
                        if click:
                            print("Astar page registered.")
                            AstarOptionsPage(screen,userText)

                    if BreadthFirstSearchRect.collidepoint((mx,my)):
                        if click:
                            print("Breadth First Search page registered.")
                            loadedBreadthFirstSearch(screen)

                    if GreedyFirstSearchRect.collidepoint((mx,my)):
                        if click:
                            print("Greedy First Search page registered.")
                            map = openMapFileYaml("testmapGreedy")
                            startNode = "A"
                            goalNode =  "B"
                            loadedGreedyFirstSearch(screen,map,startNode,goalNode)

                    if DijkstraRect.collidepoint((mx,my)):
                        if click:
                            print("Dijkstra Algorithm page registered.")
                            map = openMapFileYaml("testmapDijkstra")
                            startNode = "A"
                            goalNode =  "I"
                            DijkstrasOptionsPage(screen,userText)

                    if BackPageRect.collidepoint((mx,my)):
                        if click:
                            print("back page registered.")
                            AlgorithmPage(screen)

                    if QuitRect.collidepoint((mx,my)):
                        if click:
                            print("Exit registered.")
                            pygame.quit()

        


            pygame.display.flip()
