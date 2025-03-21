"""Breadth-First Search implementation."""
from typing import List, Set, Dict, Optional, Callable
from queue import Queue
from ..graph.graph import Graph
from ..graph.node import Node
from ...utils.database.db_manager import DatabaseManager

def bfs(graph: Graph, start_node_id: str, target_node_id: Optional[str] = None) -> List[str]:
    """Run BFS from start_node to find target_node.
    
    Args:
        graph: The graph to search
        start_node_id: ID of the starting node
        target_node_id: Optional ID of target node. If None, visits all nodes.
        
    Returns:
        List of node IDs in the order they were visited
    """
    visited: Set[str] = set()
    queue: Queue = Queue()
    path: List[str] = []
    
    # Start from the start node
    queue.put(start_node_id)
    visited.add(start_node_id)
    
    while not queue.empty():
        current_id = queue.get()
        path.append(current_id)
        
        # If we found the target, we're done
        if target_node_id and current_id == target_node_id:
            break
            
        # Get the current node
        current = graph.get_node_by_id(current_id)
        if not current:
            continue
            
        # Add unvisited neighbors to queue
        for edge in graph.get_edges():
            neighbor_id = None
            if edge.start_node == current_id:
                neighbor_id = edge.end_node
            elif not graph.directed and edge.end_node == current_id:
                neighbor_id = edge.start_node
                
            if neighbor_id and neighbor_id not in visited:
                queue.put(neighbor_id)
                visited.add(neighbor_id)
                
    return path

def bfs_with_visualization(graph: Graph, start_node_id: str, target_node_id: Optional[str] = None, 
                         step_callback: Optional[Callable[[List[str]], None]] = None) -> List[str]:
    """Run BFS with visualization support.
    
    Args:
        graph: The graph to search
        start_node_id: ID of the starting node
        target_node_id: Optional ID of target node. If None, visits all nodes.
        step_callback: Optional callback function that receives the current path at each step
        
    Returns:
        List of node IDs in the order they were visited
    """
    visited: Set[str] = set()
    queue: Queue = Queue()
    path: List[str] = []
    
    # Start from the start node
    queue.put(start_node_id)
    visited.add(start_node_id)
    
    if step_callback:
        step_callback([start_node_id])
    
    while not queue.empty():
        current_id = queue.get()
        path.append(current_id)
        
        # If we found the target, we're done
        if target_node_id and current_id == target_node_id:
            break
            
        # Get the current node
        current = graph.get_node_by_id(current_id)
        if not current:
            continue
            
        # Add unvisited neighbors to queue
        neighbors = []
        for edge in graph.get_edges():
            neighbor_id = None
            if edge.start_node == current_id:
                neighbor_id = edge.end_node
            elif not graph.directed and edge.end_node == current_id:
                neighbor_id = edge.start_node
                
            if neighbor_id and neighbor_id not in visited:
                neighbors.append(neighbor_id)
                
        # Sort neighbors for consistent ordering
        neighbors.sort()
        
        # Add neighbors to queue and update visualization
        for neighbor_id in neighbors:
            queue.put(neighbor_id)
            visited.add(neighbor_id)
            if step_callback:
                current_path = path + [neighbor_id]
                step_callback(current_path)
                
    return path 