"""Tests for database operations."""
import pytest
import os
from src.utils.database import DatabaseManager
from src.core.graph import Graph, Node, Edge

@pytest.fixture
def db_manager():
    """Create a test database manager."""
    test_db = "test_graph_data.db"
    manager = DatabaseManager(test_db)
    yield manager
    # Cleanup after tests
    if os.path.exists(test_db):
        os.remove(test_db)

def test_save_and_load_graph(db_manager):
    """Test saving and loading a graph."""
    # Create a test graph
    graph = Graph(directed=True)
    
    # Add nodes
    node1 = Node(id="1", name="Node 1", position=(0, 0))
    node2 = Node(id="2", name="Node 2", position=(1, 1))
    graph.add_node(node1)
    graph.add_node(node2)
    
    # Add edge
    edge = Edge(source=node1, target=node2, weight=2.0, directed=True)
    graph.add_edge(edge)
    
    # Save graph
    graph_id = db_manager.save_graph(graph, "Test Graph")
    
    # Load graph
    loaded_graph = db_manager.load_graph(graph_id)
    
    # Verify loaded graph
    assert len(loaded_graph.nodes) == 2
    assert len(loaded_graph.edges) == 1
    assert loaded_graph.directed == True
    
    # Verify node data
    loaded_node1 = loaded_graph.nodes["1"]
    assert loaded_node1.name == "Node 1"
    assert loaded_node1.position == (0, 0)
    assert loaded_node1.weight == 1.0
    
    # Verify edge data
    loaded_edge = list(loaded_graph.edges.values())[0]
    assert loaded_edge.source.id == "1"
    assert loaded_edge.target.id == "2"
    assert loaded_edge.weight == 2.0
    assert loaded_edge.directed == True

def test_list_graphs(db_manager):
    """Test listing saved graphs."""
    # Create and save multiple graphs
    graph1 = Graph(directed=True)
    graph2 = Graph(directed=False)
    
    # Add nodes to graphs
    node1 = Node(id="1", name="Node 1", position=(0, 0))
    node2 = Node(id="2", name="Node 2", position=(1, 1))
    
    graph1.add_node(node1)
    graph2.add_node(node2)
    
    # Save graphs
    db_manager.save_graph(graph1, "Graph 1")
    db_manager.save_graph(graph2, "Graph 2")
    
    # List graphs
    graphs = db_manager.list_graphs()
    
    # Verify list
    assert len(graphs) == 2
    assert graphs[0][1] == "Graph 1"  # Check name
    assert graphs[1][1] == "Graph 2"  # Check name
    assert graphs[0][2] == True       # Check directed flag
    assert graphs[1][2] == False      # Check directed flag

def test_delete_graph(db_manager):
    """Test deleting a graph."""
    # Create and save a graph
    graph = Graph(directed=True)
    node = Node(id="1", name="Node 1", position=(0, 0))
    graph.add_node(node)
    
    graph_id = db_manager.save_graph(graph, "Test Graph")
    
    # Verify graph exists
    assert len(db_manager.list_graphs()) == 1
    
    # Delete graph
    db_manager.delete_graph(graph_id)
    
    # Verify graph is deleted
    assert len(db_manager.list_graphs()) == 0 