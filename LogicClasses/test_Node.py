from unittest import TestCase, main
from Node import Node



class TestNode(TestCase):

        def setUp(self):
            self.node1 = Node(
                nodeName ="A",
                xCoordinate ="257",
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

        def test_get_NodeName(self):
            result1 = self.node1.get_nodeName()
            result2 = self.node2.get_nodeName()
            self.assertEqual(result1,"A")
            self.assertEqual(result2,"B")

        def test_get_xCoordinate(self):
            result1 = self.node1.get_xCoordinate()
            result2 = self.node2.get_xCoordinate()
            self.assertEqual(result1,"257")
            self.assertEqual(result2,"430")
        
        def test_gety_Coordinate(self):
            result1 = self.node1.get_yCoordinate()
            result2 = self.node2.get_yCoordinate()
            self.assertEqual(result1,"670")
            self.assertEqual(result2,"484")

        def test_get_weight(self):
            result1 = self.node1.get_weight()
            result2 = self.node2.get_weight()
            self.assertEqual(result1,None)
            self.assertEqual(result2,None)
        
        def test_get_adjacencies(self):
            result1 = self.node1.get_adjacencies()
            result2 = self.node2.get_adjacencies()
            self.assertEqual(result1,[{'Node': 'B', 'Weight': 4}, {'Node': 'C', 'Weight': 2}])
            self.assertEqual(result2,[{'Node': 'A', 'Weight': 4}, {'Node': 'D', 'Weight': 5}, {'Node': 'C', 'Weight': 1}])

if __name__ == "__main__":
    main()