"""Edge class for graph representation."""
from dataclasses import dataclass
from typing import Dict, Any, Optional
from .node import Node

@dataclass
class Edge:
    """Represents an edge in a graph.
    
    Attributes:
        source: Source node
        target: Target node
        weight: Edge weight/cost
        directed: Whether the edge is directed
        metadata: Additional edge data
    """
    source: Node
    target: Node
    weight: float = 1.0
    directed: bool = False
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        """Initialize metadata if None."""
        if self.metadata is None:
            self.metadata = {}

    def __str__(self) -> str:
        """String representation of the edge."""
        direction = "->" if self.directed else "<->"
        return f"Edge({self.source.id} {direction} {self.target.id}, weight={self.weight})"

    def __repr__(self) -> str:
        """Detailed string representation of the edge."""
        return f"Edge(source={self.source}, target={self.target}, weight={self.weight}, directed={self.directed})"

    def __eq__(self, other: object) -> bool:
        """Check if two edges are equal.
        
        For undirected edges, (A->B) equals (B->A).
        For directed edges, direction matters.
        """
        if not isinstance(other, Edge):
            return NotImplemented
        
        if self.directed or other.directed:
            return (self.source == other.source and 
                   self.target == other.target and 
                   self.directed == other.directed)
        
        return ((self.source == other.source and self.target == other.target) or
                (self.source == other.target and self.target == other.source)) 