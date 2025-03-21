"""Graph class for managing nodes and edges."""
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict
from .node import Node
from .edge import Edge

class Graph:
    """A graph data structure supporting both directed and undirected edges.
    
    This implementation uses adjacency lists for efficient edge lookups and
    maintains separate sets of nodes and edges for easy iteration.
    """
    
    def __init__(self, directed: bool = False):
        """Initialize an empty graph.
        
        Args:
            directed: Whether the graph is directed by default
        """
        self.directed = directed
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[Tuple[str, str], Edge] = {}
        self.adjacency_list: Dict[str, Set[str]] = defaultdict(set)
        
    def add_node(self, node: Node) -> None:
        """Add a node to the graph.
        
        Args:
            node: The node to add
        """
        if node.id in self.nodes:
            raise ValueError(f"Node with id {node.id} already exists")
        self.nodes[node.id] = node
        
    def add_edge(self, edge: Edge) -> None:
        """Add an edge to the graph.
        
        Args:
            edge: The edge to add
        """
        if edge.source.id not in self.nodes or edge.target.id not in self.nodes:
            raise ValueError("Both source and target nodes must exist in the graph")
            
        # Create a unique key for the edge
        edge_key = (edge.source.id, edge.target.id)
        if edge_key in self.edges:
            raise ValueError(f"Edge between {edge.source.id} and {edge.target.id} already exists")
            
        self.edges[edge_key] = edge
        self.adjacency_list[edge.source.id].add(edge.target.id)
        
        # For undirected graphs, add the reverse edge
        if not edge.directed and not self.directed:
            reverse_key = (edge.target.id, edge.source.id)
            self.edges[reverse_key] = Edge(
                source=edge.target,
                target=edge.source,
                weight=edge.weight,
                directed=False,
                metadata=edge.metadata.copy()
            )
            self.adjacency_list[edge.target.id].add(edge.source.id)
            
    def remove_node(self, node_id: str) -> None:
        """Remove a node and all its edges from the graph.
        
        Args:
            node_id: The ID of the node to remove
        """
        if node_id not in self.nodes:
            raise ValueError(f"Node with id {node_id} does not exist")
            
        # Remove all edges connected to this node
        edges_to_remove = []
        for edge_key in self.edges:
            if edge_key[0] == node_id or edge_key[1] == node_id:
                edges_to_remove.append(edge_key)
                
        for edge_key in edges_to_remove:
            self.remove_edge(edge_key[0], edge_key[1])
            
        # Remove the node
        del self.nodes[node_id]
        del self.adjacency_list[node_id]
        
    def remove_edge(self, source_id: str, target_id: str) -> None:
        """Remove an edge from the graph.
        
        Args:
            source_id: The ID of the source node
            target_id: The ID of the target node
        """
        edge_key = (source_id, target_id)
        if edge_key not in self.edges:
            raise ValueError(f"Edge between {source_id} and {target_id} does not exist")
            
        edge = self.edges[edge_key]
        self.adjacency_list[source_id].remove(target_id)
        del self.edges[edge_key]
        
        # For undirected graphs, remove the reverse edge
        if not edge.directed and not self.directed:
            reverse_key = (target_id, source_id)
            self.adjacency_list[target_id].remove(source_id)
            del self.edges[reverse_key]
            
    def get_neighbors(self, node_id: str) -> Set[str]:
        """Get the set of neighbor node IDs for a given node.
        
        Args:
            node_id: The ID of the node
            
        Returns:
            Set of neighbor node IDs
        """
        if node_id not in self.nodes:
            raise ValueError(f"Node with id {node_id} does not exist")
        return self.adjacency_list[node_id]
        
    def get_edge(self, source_id: str, target_id: str) -> Optional[Edge]:
        """Get the edge between two nodes.
        
        Args:
            source_id: The ID of the source node
            target_id: The ID of the target node
            
        Returns:
            The edge if it exists, None otherwise
        """
        edge_key = (source_id, target_id)
        return self.edges.get(edge_key)
        
    def is_connected(self, source_id: str, target_id: str) -> bool:
        """Check if two nodes are connected by an edge.
        
        Args:
            source_id: The ID of the source node
            target_id: The ID of the target node
            
        Returns:
            True if the nodes are connected, False otherwise
        """
        return target_id in self.adjacency_list[source_id]
        
    def __str__(self) -> str:
        """String representation of the graph."""
        return f"Graph(nodes={len(self.nodes)}, edges={len(self.edges)}, directed={self.directed})"
        
    def __repr__(self) -> str:
        """Detailed string representation of the graph."""
        return f"Graph(nodes={self.nodes}, edges={self.edges}, directed={self.directed})" 