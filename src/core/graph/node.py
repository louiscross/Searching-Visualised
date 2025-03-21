"""Node class for graph representation."""
from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class Node:
    """Represents a node in a graph.
    
    Attributes:
        id: Unique identifier for the node
        name: Display name for the node
        position: (x, y) coordinates for visualization
        weight: Node weight/cost
        metadata: Additional node data
    """
    id: str
    name: str
    position: tuple[float, float]
    weight: float = 1.0
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        """Initialize metadata if None."""
        if self.metadata is None:
            self.metadata = {}

    def distance_to(self, other: 'Node') -> float:
        """Calculate Euclidean distance to another node.
        
        Args:
            other: Target node to calculate distance to
            
        Returns:
            float: Euclidean distance between nodes
        """
        x1, y1 = self.position
        x2, y2 = other.position
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def __str__(self) -> str:
        """String representation of the node."""
        return f"Node(id={self.id}, name={self.name}, pos={self.position})"

    def __repr__(self) -> str:
        """Detailed string representation of the node."""
        return f"Node(id={self.id}, name={self.name}, pos={self.position}, weight={self.weight})" 