"""Script to generate and store sample graphs in the database."""
from src.core.graph.graph import Graph
from src.core.graph.node import Node
from src.core.graph.edge import Edge
from src.utils.database.db_manager import DatabaseManager
import math
from src.visualization import GraphViewer

def create_grid_graph(width: int, height: int, directed: bool = False, prefix: str = "grid") -> Graph:
    """Create a grid graph with the specified dimensions.
    
    Args:
        width: Number of nodes in each row
        height: Number of nodes in each column
        directed: Whether the graph is directed
        prefix: Prefix for node IDs to ensure uniqueness
        
    Returns:
        A grid graph
    """
    graph = Graph(directed=directed)
    
    # Create nodes
    for y in range(height):
        for x in range(width):
            node_id = f"{prefix}_n{x}_{y}"
            node = Node(
                id=node_id,
                name=f"Node {x},{y}",
                position=(x * 100, y * 100),  # Space nodes 100 units apart
                weight=1.0
            )
            graph.add_node(node)
    
    # Create edges (connect to right and down)
    for y in range(height):
        for x in range(width):
            current_id = f"{prefix}_n{x}_{y}"
            
            # Connect to right
            if x < width - 1:
                right_id = f"{prefix}_n{x+1}_{y}"
                edge = Edge(
                    source=graph.nodes[current_id],
                    target=graph.nodes[right_id],
                    weight=1.0,
                    directed=directed
                )
                graph.add_edge(edge)
            
            # Connect to down
            if y < height - 1:
                down_id = f"{prefix}_n{x}_{y+1}"
                edge = Edge(
                    source=graph.nodes[current_id],
                    target=graph.nodes[down_id],
                    weight=1.0,
                    directed=directed
                )
                graph.add_edge(edge)
    
    return graph

def create_circular_graph(num_nodes: int, radius: float = 200.0, prefix: str = "circle") -> Graph:
    """Create a circular graph with evenly spaced nodes.
    
    Args:
        num_nodes: Number of nodes in the circle
        radius: Radius of the circle
        prefix: Prefix for node IDs to ensure uniqueness
        
    Returns:
        A circular graph
    """
    graph = Graph(directed=False)
    
    # Create nodes in a circle
    for i in range(num_nodes):
        angle = (2 * math.pi * i) / num_nodes
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        
        node = Node(
            id=f"{prefix}_n{i}",
            name=f"Node {i}",
            position=(x, y),
            weight=1.0
        )
        graph.add_node(node)
    
    # Connect each node to its next neighbor
    for i in range(num_nodes):
        current = graph.nodes[f"{prefix}_n{i}"]
        next_idx = (i + 1) % num_nodes
        next_node = graph.nodes[f"{prefix}_n{next_idx}"]
        
        edge = Edge(
            source=current,
            target=next_node,
            weight=1.0,
            directed=False
        )
        graph.add_edge(edge)
    
    return graph

def create_binary_tree(depth: int, spacing: float = 100.0, prefix: str = "tree") -> Graph:
    """Create a complete binary tree.
    
    Args:
        depth: Depth of the binary tree
        spacing: Horizontal spacing between nodes
        prefix: Prefix for node IDs to ensure uniqueness
        
    Returns:
        A binary tree graph
    """
    graph = Graph(directed=True)
    
    def create_node(level: int, position: int, x: float, y: float):
        node_id = f"{prefix}_n{level}_{position}"
        node = Node(
            id=node_id,
            name=f"Node {level},{position}",
            position=(x, y),
            weight=1.0
        )
        graph.add_node(node)
        
        if level < depth - 1:
            # Calculate positions for children
            child_spacing = spacing / (2 ** (level + 1))
            left_x = x - child_spacing
            right_x = x + child_spacing
            child_y = y + spacing
            
            # Create left child
            left_id = create_node(level + 1, position * 2, left_x, child_y)
            edge = Edge(
                source=node,
                target=graph.nodes[left_id],
                weight=1.0,
                directed=True
            )
            graph.add_edge(edge)
            
            # Create right child
            right_id = create_node(level + 1, position * 2 + 1, right_x, child_y)
            edge = Edge(
                source=node,
                target=graph.nodes[right_id],
                weight=1.0,
                directed=True
            )
            graph.add_edge(edge)
        
        return node_id
    
    # Start from root node
    create_node(0, 0, 0, 0)
    return graph

def store_sample_graphs():
    """Generate and store sample graphs in the database."""
    db = DatabaseManager()
    
    # Clear existing data
    db.clear_database()
    
    # Create and store a 4x4 grid
    grid_graph = create_grid_graph(4, 4, prefix="grid1")
    db.save_graph(grid_graph, "4x4 Grid")
    
    # Create and store a circular graph with 8 nodes
    circular_graph = create_circular_graph(8, prefix="circle1")
    db.save_graph(circular_graph, "8-Node Circle")
    
    # Create and store a binary tree of depth 3
    binary_tree = create_binary_tree(3, prefix="tree1")
    db.save_graph(binary_tree, "Binary Tree (Depth 3)")
    
    # Create and store a directed grid
    directed_grid = create_grid_graph(3, 3, directed=True, prefix="grid2")
    db.save_graph(directed_grid, "3x3 Directed Grid")
    
    print("Sample graphs have been stored in the database:")
    for graph_id, name, directed in db.list_graphs():
        print(f"- {name} (ID: {graph_id}, Directed: {directed})")

if __name__ == "__main__":
    # First, store all sample graphs
    store_sample_graphs()
    
    # Create the viewer
    viewer = GraphViewer()
    
    # Load and display the 4x4 grid with a highlighted path
    # We'll highlight a path from top-left to bottom-right
    path = ['grid1_n0_0', 'grid1_n1_0', 'grid1_n1_1', 'grid1_n2_1', 'grid1_n2_2', 'grid1_n3_2', 'grid1_n3_3']
    viewer.load_and_display_graph(1, highlighted_path=path)
    
    # Start the visualization
    viewer.run() 