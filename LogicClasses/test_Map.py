from unittest import TestCase, main
from Node import Node
from Map import Map


class TestMap(TestCase):

        def setUp(self):
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
             
            self.loadedMap = Map([])
            for data in self.nodes: 
                node = Node(
                    data["nodeName"],
                    data.get("xCoordinate"),
                    data.get("yCoordinate"),
                    data.get("Weight"),
                    data.get("adjacencies")
                )
                self.loadedMap.addNodes(node)
                 

        def test_getNodeByIndex(self):
            result = repr(self.loadedMap.getNodeByIndex(1))
            self.assertEqual(result,"Node Name: B, X Coordinate: 430, Y Coordinate: 484, Weight: None, Adjacencies: [{'Node': 'A', 'Weight': 4}, {'Node': 'D', 'Weight': 5}, {'Node': 'C', 'Weight': 1}]")

        def test_getNodeByName(self):
            result = repr(self.loadedMap.getNodeByName("B"))
            self.assertEqual(result,"Node Name: B, X Coordinate: 430, Y Coordinate: 484, Weight: None, Adjacencies: [{'Node': 'A', 'Weight': 4}, {'Node': 'D', 'Weight': 5}, {'Node': 'C', 'Weight': 1}]")

        def test_getWeightByName(self):
            result = repr(self.loadedMap.getWeightByName("B"))
            self.assertEqual(result,"None")

if __name__ == "__main__":
    main()