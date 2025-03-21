from unittest import TestCase, main
import collections
from queue import PriorityQueue
import yaml
from Node import Node

class TestMap(TestCase):
    def setUp(self):
        self.nodes = Node(
            nodeName ="A",
            xCoordinate = "257",
            yCoordinate = "670",
            weight = None,
            adjacencies = [{'Node': 'B', 'Weight': 4}, {'Node': 'C', 'Weight': 2}]
        )
        self.node2 = Node(
            nodeName ="B",
            xCoordinate = "430",
            yCoordinate = "484",
            weight = None,
            adjacencies = [{'Node': 'A', 'Weight': 4}, {'Node': 'D', 'Weight': 5}, {'Node': 'C', 'Weight': 1}]
        )
        self.node3 = Node(
            nodeName ="C",
            xCoordinate = "506",
            yCoordinate = "734",
            weight = None,
            adjacencies = [{'Node': 'A', 'Weight': 2}, {'Node': 'B', 'Weight': 1}, {'Node': 'D', 'Weight': 8}, {'Node': 'E', 'Weight': 10}]
        )
        self.node4 = Node(
            nodeName ="D",
            xCoordinate = "778",
            yCoordinate = "481",
            weight = None,
            adjacencies = [{'Node': 'B', 'Weight': 5}, {'Node': 'C', 'Weight': 8}, {'Node': 'E', 'Weight': 2}, {'Node': 'Z', 'Weight': 6}]
        )
        self.node5 = Node(
            nodeName ="E",
            xCoordinate = "809",
            yCoordinate = "723",
            weight = None,
            adjacencies = [{'Node': 'C', 'Weight': 10}, {'Node': 'D', 'Weight': 2}, {'Node': 'Z', 'Weight': 5}]
        )
        self.node6 = Node(
            nodeName ="Z",
            xCoordinate = "1039",
            yCoordinate = "606",
            weight = None,
            adjacencies = [{'Node': 'D', 'Weight': 6}, {'Node': 'E', 'Weight': 5}]
        )

    def nodeSetUp(self):
        self.nodes = [{
            "nodeName": "A",
            "xCoordinate": "257",
            "yCoordinate": "670",
            "weight": None,
            "adjacencies": [{'Node': 'B', 'Weight': 4}, {'Node': 'C', 'Weight': 2}]

        },
        {
            "nodeName": "B",
            "xCoordinate": "430",
            "yCoordinate": "484",
            "weight": None,
            "adjacencies": [{'Node': 'A', 'Weight': 4}, {'Node': 'D', 'Weight': 5}, {'Node': 'C', 'Weight': 1}]
       

        }
        ]

    def test_openMapFileYaml(self):
        loadedMap = map([],[])
        for data in self.nodes: 
            node = Node(
            data["Node Name"],
            data.get("X Coordinate",None),
            data.get("Y Coordinate",None),
            data.get("Weight",None),
            data.get("Adjacencies",[])
        )
        loadedMap.addNodes(node)

    
        
        

if __name__ == "__main__":
    main()