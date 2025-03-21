class Node:
    def __init__(self, nodeName, xCoordinate, yCoordinate,weight,adjacencies):
        self.nodeName = nodeName
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
        self.weight = weight
        self.adjacencies = adjacencies

    def get_nodeName(self):
        return self.nodeName
    
    def get_xCoordinate(self):
        return self.xCoordinate
    
    def get_yCoordinate(self):
        return self.yCoordinate
    
    def get_weight(self):
        return self.weight
    
    def get_adjacencies(self):
        return self.adjacencies
    
    def __str__(self):
        return (
            f"Node Name: {self.nodeName}, "
            f"X Coordinate: {self.xCoordinate}, "
            f"Y Coordinate: {self.yCoordinate}, "
            f"Weight: {self.weight}, "
            f"Adjacencies: {self.adjacencies}"

        )
    
    def __repr__(self):
        return (
            f"Node Name: {self.nodeName}, "
            f"X Coordinate: {self.xCoordinate}, "
            f"Y Coordinate: {self.yCoordinate}, "
            f"Weight: {self.weight}, "
            f"Adjacencies: {self.adjacencies}"

        )


    
    