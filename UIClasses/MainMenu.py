import pygame
from LogicClasses.Dijkstra import Dijkstra
from UIClasses.AlgorithmPage import AlgorithmPage
from UIClasses.LoadedBreadthFirstSearch import loadedBreadthFirstSearch

from UIClasses.draw_text import draw_text

# Start of UI following format of pygame docs
def mainmenuUI():
    pygame.init()

    screenHeight = 1080
    screenWidth = 1920
    screen = pygame.display.set_mode((screenWidth,screenHeight))
    pygame.display.set_caption('Visualising Search Algorithms: Main Menu')
    textFont = pygame.font.SysFont("Rockwell",48, bold = True, italic = True)
    button = pygame.Rect(850,450,200,50)
    userText = ""
    inputRect = pygame.Rect(650,250,500,50)
    enterRect = pygame.Rect(1200,250,250,50)
    click = False





    running = True
    while running:
        mx,my = pygame.mouse.get_pos()
        screen.fill((50, 125, 168))
        draw_text(screen,"Select Map to choose: ",textFont,(0,0,0),650,160)
        pygame.draw.rect(screen,(180, 185, 194),inputRect)
        pygame.draw.rect(screen,(180, 185, 194),enterRect)
        draw_text(screen,"Load map",textFont,(0,0,0),1200,250)
        textSurface = textFont.render(userText,True,"white")
        screen.blit(textSurface,(650,250))
        for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
                        print(mx,my)
                    if enterRect.collidepoint((mx,my)):
                        if click:
                            print(userText)
                            print("Click page registered.")
                            mapName = userText
                            #loadedBreadthFirstSearch(screen)
                            AlgorithmPage(screen,userText)
                # checks for keypresses
                if event.type == pygame.KEYDOWN:
                    #this is the type of keypress checked
                    if event.key == pygame.K_BACKSPACE:
                        userText = userText[:-1]
                    if event.key == pygame.K_KP_ENTER:
                        mapName = userText
                        AlgorithmPage(screen,userText)
                    userText+=event.unicode
                

        pygame.display.flip()

            
    pygame.quit()