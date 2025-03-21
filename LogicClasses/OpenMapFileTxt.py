from yaml import Node
from LogicClasses.Map import Map

# function which opens map from Maps folder and will read data to form node objects which will be then formed into the map object

def openMapFileTxt(userText):
    mapName = userText
    # this will open the file and read file
    with open("Maps/"+mapName+".txt","r") as file:
        nodesInMap = file.read().split("\n\n")
    
    # creates Map class with no instances
    loadedMap = Map([])
    
    # loop to seperate the nodes
    for data in nodesInMap:
        lines = data.strip().split("\n")
        #dictionary is created to store info on current node in loop
        nodeData = {}
        for line in lines:
            # splits lines so each dictionary element can be populated correctly with key and value
            key, value = line.split(": ")

            if key == "Node Name":
                nodeData["nodeName"] = value

            elif key == "X Coordinate":
                nodeData["xCoordinate"] = int(value)

            elif key == "Y Coordinate":
                nodeData["yCoordinate"] = int(value)

            elif key == "Weight":
                nodeData["weight"] = int(value)

            elif key == "Adjacencies":
                # as this is not a single value, instead a list I split the value into value(s) which can then be added back
                adjacencies = value.split(", ")
                nodeData["adjacencies"] = adjacencies
            
        node = Node(**nodeData)
        loadedMap.addNodes(node)
    return loadedMap