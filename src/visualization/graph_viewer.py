from PyQt6.QtWidgets import QApplication
import sys
import math
from typing import Optional, List, Dict, Tuple

from .map_visualizer import MapVisualizer
from ..core.graph.graph import Graph
from ..utils.database.db_manager import DatabaseManager

class GraphViewer:
    def __init__(self):
        self.db = DatabaseManager()
        self.app = QApplication(sys.argv)
        self.visualizer = MapVisualizer()
        
    def load_and_display_graph(self, graph_id: int, highlighted_path: Optional[List[str]] = None):
        """Load a graph from the database and display it"""
        graph = self.db.load_graph(graph_id)
        if not graph:
            print(f"No graph found with ID {graph_id}")
            return
            
        # Convert graph to visualization format
        nodes, edges = self._prepare_graph_for_visualization(graph)
        
        # Set the graph data
        self.visualizer.set_graph(nodes, edges)
        
        # Set highlighted path if provided
        if highlighted_path:
            self.visualizer.set_highlighted_path(highlighted_path)
            
        # Show the visualization
        self.visualizer.show()
        
    def run(self):
        """Start the visualization application"""
        sys.exit(self.app.exec())
        
    def _prepare_graph_for_visualization(self, graph: Graph) -> Tuple[Dict[str, Tuple[float, float]], List[Tuple[str, str]]]:
        """Convert a Graph object to visualization format"""
        # Get graph dimensions
        nodes = graph.get_nodes()
        if not nodes:
            return {}, []
            
        # Find min/max coordinates to scale the graph
        min_x = min(node.x for node in nodes)
        max_x = max(node.x for node in nodes)
        min_y = min(node.y for node in nodes)
        max_y = max(node.y for node in nodes)
        
        # Add padding
        padding = 50
        width = self.visualizer.width() - 2 * padding
        height = self.visualizer.height() - 2 * padding
        
        # Scale factor
        scale_x = width / (max_x - min_x) if max_x != min_x else 1
        scale_y = height / (max_y - min_y) if max_y != min_y else 1
        scale = min(scale_x, scale_y)
        
        # Convert nodes to visualization format
        vis_nodes = {}
        for node in nodes:
            x = (node.x - min_x) * scale + padding
            y = (node.y - min_y) * scale + padding
            vis_nodes[node.id] = (x, y)
            
        # Convert edges to visualization format
        vis_edges = []
        for edge in graph.get_edges():
            vis_edges.append((edge.start_node, edge.end_node))
            
        return vis_nodes, vis_edges

def main():
    # Example usage
    viewer = GraphViewer()
    
    # Load and display graph 1 (4x4 Grid)
    viewer.load_and_display_graph(1)
    
    # Start the application
    viewer.run()

if __name__ == '__main__':
    main() 