"""Greedy Best-First Search implementation."""
from typing import Set, List, Callable, Dict, Optional
from queue import PriorityQueue
from ..graph.graph import Graph
from ..graph.node import Node

class GreedyBestFirstSearch:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.visited: Set[str] = set()
        self.current_path: List[str] = []
        
    def heuristic(self, node: Node, target: Node) -> float:
        """Calculate heuristic (Euclidean distance) between nodes."""
        return node.distance_to(target)
        
    def run(self, start_node: str, target_node: str, step_callback: Optional[Callable[[List[str]], None]] = None) -> List[str]:
        """Run Greedy Best-First Search from start_node to target_node.
        
        Args:
            start_node: ID of the starting node
            target_node: ID of the target node
            step_callback: Optional callback function that receives the current path at each step
            
        Returns:
            List of node IDs representing the path found
        """
        print(f"Starting Greedy search from {start_node} to {target_node}")
        self.visited.clear()
        self.current_path.clear()
        
        # Priority queue of (priority, node_id, path)
        frontier = PriorityQueue()
        start = self.graph.nodes[start_node]
        target = self.graph.nodes[target_node]
        
        print(f"Start node: {start_node}, Target node: {target_node}")
        print(f"Start position: {start.position}, Target position: {target.position}")
        
        # Add start node with its heuristic value as priority
        initial_heuristic = self.heuristic(start, target)
        print(f"Initial heuristic value: {initial_heuristic}")
        frontier.put((initial_heuristic, start_node, [start_node]))
        
        while not frontier.empty():
            _, current_id, path = frontier.get()
            
            # Skip if already visited
            if current_id in self.visited:
                continue
                
            self.visited.add(current_id)
            self.current_path = path
            
            if step_callback:
                print(f"Calling callback with path: {path}")
                step_callback(self.current_path)
                
            # If we found the target, we're done
            if current_id == target_node:
                print(f"Found target node! Path: {path}")
                return path
                
            # Get current node
            current = self.graph.nodes[current_id]
            
            # Add unvisited neighbors to frontier
            neighbors = self.graph.get_neighbors(current_id)
            print(f"Found {len(neighbors)} neighbors for node {current_id}: {neighbors}")
            
            for neighbor_id in neighbors:
                if neighbor_id not in self.visited:
                    neighbor = self.graph.nodes[neighbor_id]
                    priority = self.heuristic(neighbor, target)
                    new_path = path + [neighbor_id]
                    print(f"Adding neighbor {neighbor_id} with priority {priority}")
                    frontier.put((priority, neighbor_id, new_path))
                    
        print("No path found to target")
        return []  # No path found 