import collections
import yaml
from LogicClasses.Map import Map
from LogicClasses.Node import Node


# function which opens map from Maps folder and will read data to form node objects which will be then formed into the map object
def openMapFileYaml(userText):
    mapName = userText
    # this will open the file and read file
    with open("Maps/"+mapName+".yaml","r") as file:
        nodesInMap = yaml.safe_load(file)
    # creates Map class with no instances
    loadedMap = Map([])
    # loop to seperate the nodes
    for data in nodesInMap: 
        node = Node(
            data["Node Name"],
            data.get("X Coordinate",None),
            data.get("Y Coordinate",None),
            data.get("Weight",None),
            data.get("Adjacencies",[])
        )
        loadedMap.addNodes(node)
    return loadedMap