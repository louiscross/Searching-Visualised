#standard imports
import math
import pygame
from collections import deque
import time
import yaml
import sys

#imports from Logic Class folder all classes
from LogicClasses.Map import Map
from LogicClasses.Node import Node
from LogicClasses.Astar import AstarAlgorithm
from LogicClasses.BFS import breadthFirstSearch
from LogicClasses.BFS_GUI import breadthFirstSearchGUI
from LogicClasses.OpenMapFileYaml import openMapFileYaml
from LogicClasses.OpenMapFileTxt import openMapFileTxt


#Imports from UI Class folder
from UIClasses.draw_text import draw_text
from UIClasses.LoadedBreadthFirstSearch import loadedBreadthFirstSearch
from UIClasses.MainMenu import mainmenuUI



def addNodeToMap(loadedMap):
    #you want to get the last node to add into the 
    newNode = loadedMap[:-1]
    print("New Node: " + newNode)

    print("node at index 0" + newNode[0])
    for data in newNode:
        lines = data.strip().split("\n")
        loadedMap.addNodes(newNode)

    return loadedMap

# Function to add a node to an imported map
def addNode():
    addedNode = Node([],[],[],[],"True","")
    addedNodeAdjacencies = ""
    numberOfAdjacencies = 0

    nodeName = input("\nEnter node name: ")
    addedNode.nodeName = nodeName
    xCoordinate = input("\nEnter x Coordinate: ")
    addedNode.xCoordinate = xCoordinate
    yCoordinate = input("\nEnter y Coordinate: ")
    addedNode.yCoordinate = yCoordinate
    weight = input("\nEnter weight: ")
    addedNode.weight = weight
    adjacencies = input("\n Adjacencies? (y/n) ")
    Directional = False
    #cannot use adjacencies list as a list because for formatting into dictionary i need it to be string, as when stored in txt
    # however i could use it as a list, append the total node into the map, and then implement a 'save feature' which then reformats all lists back into strings before saving to txt
    adjacenciesList = []
    if adjacencies == "y":
        numberOfAdjacencies = input("\nHow many adjacencies? (int)")
        if int(numberOfAdjacencies) > 1:
            Directional = "True"
            #addedNode.directional = Directional
        else:
            Directional = "False"
            #addedNode.directional = Directional
        x = 0
        addedNode.directional = "True"
        for x in range(0,int(numberOfAdjacencies)):
            adjacenciesNum = input("\nEnter adjacency number " +str(x+1)+  " : ")
            adjacenciesList.append(adjacenciesNum)
            addedNodeAdjacencies+", "+adjacenciesNum
        addedNodeAdjacencies = addedNodeAdjacencies[:-2]
        addedNode.adjacencies = addedNodeAdjacencies
    
    nodeDictionary = {
        "Node Name": ": " +nodeName,
        "X Coordinate": ": "+xCoordinate,
        "Y Coordinate": ": "+yCoordinate,
        "Weight": ": "+weight,
        "Directional": ": "+str(Directional),
        "Adjacencies": ": "+str(adjacenciesList)
    }

    print("added node: " + str(addedNode))
    Map.addNodes(addedNode)
    addNodeToMap(Map)
    return 


mainmenuUI()