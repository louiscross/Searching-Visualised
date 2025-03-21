"""Depth-First Search implementation."""
from typing import Set, List, Callable
from ..graph.graph import Graph

class DepthFirstSearch:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.visited: Set[str] = set()
        self.current_path: List[str] = []
        
    def run(self, start_node: str, step_callback: Callable[[List[str]], None] = None) -> List[str]:
        """Run DFS from start_node.
        
        Args:
            start_node: ID of the starting node
            step_callback: Optional callback function that receives the current path at each step
            
        Returns:
            List of node IDs in the order they were visited
        """
        self.visited.clear()
        self.current_path.clear()
        return self._dfs(start_node, step_callback)
        
    def _dfs(self, node_id: str, step_callback: Callable[[List[str]], None] = None) -> List[str]:
        """Recursive DFS implementation."""
        if node_id in self.visited:
            return []
            
        self.visited.add(node_id)
        self.current_path.append(node_id)
        
        if step_callback:
            step_callback(self.current_path)
            
        path = [node_id]
        
        # Get all neighbors using the adjacency list
        neighbors = self.graph.get_neighbors(node_id)
        
        # Sort neighbors for consistent ordering
        neighbors = sorted(neighbors)
        
        # Visit each unvisited neighbor
        for neighbor in neighbors:
            if neighbor not in self.visited:
                path.extend(self._dfs(neighbor, step_callback))
        
        return path 