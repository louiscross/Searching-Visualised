"""Database manager for SQLite operations."""
import sqlite3
import json
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from ...core.graph import Graph, Node, Edge

class DatabaseManager:
    """Manages SQLite database operations for graph storage."""
    
    def __init__(self, db_path: str = "graph_data.db"):
        """Initialize the database manager.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._init_db()
        
    def _init_db(self) -> None:
        """Initialize the database schema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create nodes table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS nodes (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    x_coord REAL NOT NULL,
                    y_coord REAL NOT NULL,
                    weight REAL DEFAULT 1.0,
                    metadata TEXT
                )
            ''')
            
            # Create edges table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS edges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_id TEXT NOT NULL,
                    target_id TEXT NOT NULL,
                    weight REAL DEFAULT 1.0,
                    directed BOOLEAN DEFAULT 0,
                    metadata TEXT,
                    FOREIGN KEY (source_id) REFERENCES nodes (id),
                    FOREIGN KEY (target_id) REFERENCES nodes (id),
                    UNIQUE(source_id, target_id)
                )
            ''')
            
            # Create graphs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS graphs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    directed BOOLEAN DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create graph_nodes table (many-to-many relationship)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS graph_nodes (
                    graph_id INTEGER,
                    node_id TEXT,
                    FOREIGN KEY (graph_id) REFERENCES graphs (id),
                    FOREIGN KEY (node_id) REFERENCES nodes (id),
                    PRIMARY KEY (graph_id, node_id)
                )
            ''')
            
            conn.commit()
            
    def clear_database(self) -> None:
        """Clear all data from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Drop all tables
            cursor.execute("DROP TABLE IF EXISTS graph_nodes")
            cursor.execute("DROP TABLE IF EXISTS edges")
            cursor.execute("DROP TABLE IF EXISTS nodes")
            cursor.execute("DROP TABLE IF EXISTS graphs")
            
            conn.commit()
            
        # Reinitialize the database
        self._init_db()
            
    def save_graph(self, graph: Graph, name: str) -> int:
        """Save a graph to the database.
        
        Args:
            graph: The graph to save
            name: Name for the graph
            
        Returns:
            The ID of the saved graph
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Insert graph
            cursor.execute(
                "INSERT INTO graphs (name, directed) VALUES (?, ?)",
                (name, graph.directed)
            )
            graph_id = cursor.lastrowid
            
            # Insert nodes
            for node in graph.nodes.values():
                cursor.execute(
                    """
                    INSERT INTO nodes (id, name, x_coord, y_coord, weight, metadata)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        node.id,
                        node.name,
                        node.position[0],
                        node.position[1],
                        node.weight,
                        json.dumps(node.metadata)
                    )
                )
                
                # Link node to graph
                cursor.execute(
                    "INSERT INTO graph_nodes (graph_id, node_id) VALUES (?, ?)",
                    (graph_id, node.id)
                )
            
            # Insert edges
            for edge in graph.edges.values():
                cursor.execute(
                    """
                    INSERT INTO edges (source_id, target_id, weight, directed, metadata)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        edge.source.id,
                        edge.target.id,
                        edge.weight,
                        edge.directed,
                        json.dumps(edge.metadata)
                    )
                )
            
            conn.commit()
            return graph_id
            
    def load_graph(self, graph_id: int) -> Graph:
        """Load a graph from the database.
        
        Args:
            graph_id: The ID of the graph to load
            
        Returns:
            The loaded graph
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get graph info
            cursor.execute(
                "SELECT name, directed FROM graphs WHERE id = ?",
                (graph_id,)
            )
            name, directed = cursor.fetchone()
            
            # Create new graph
            graph = Graph(directed=bool(directed))
            
            # Load nodes
            cursor.execute(
                """
                SELECT n.id, n.name, n.x_coord, n.y_coord, n.weight, n.metadata
                FROM nodes n
                JOIN graph_nodes gn ON n.id = gn.node_id
                WHERE gn.graph_id = ?
                """,
                (graph_id,)
            )
            
            for row in cursor.fetchall():
                node_id, name, x, y, weight, metadata = row
                node = Node(
                    id=node_id,
                    name=name,
                    position=(x, y),
                    weight=weight,
                    metadata=json.loads(metadata) if metadata else {}
                )
                graph.add_node(node)
            
            # Load edges
            cursor.execute(
                """
                SELECT e.source_id, e.target_id, e.weight, e.directed, e.metadata
                FROM edges e
                JOIN graph_nodes gn1 ON e.source_id = gn1.node_id
                JOIN graph_nodes gn2 ON e.target_id = gn2.node_id
                WHERE gn1.graph_id = ? AND gn2.graph_id = ?
                """,
                (graph_id, graph_id)
            )
            
            for row in cursor.fetchall():
                source_id, target_id, weight, directed, metadata = row
                source = graph.nodes[source_id]
                target = graph.nodes[target_id]
                edge = Edge(
                    source=source,
                    target=target,
                    weight=weight,
                    directed=bool(directed),
                    metadata=json.loads(metadata) if metadata else {}
                )
                graph.add_edge(edge)
            
            return graph
            
    def list_graphs(self) -> List[Tuple[int, str, bool]]:
        """List all saved graphs.
        
        Returns:
            List of tuples containing (graph_id, name, directed)
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, directed FROM graphs")
            return cursor.fetchall()
            
    def delete_graph(self, graph_id: int) -> None:
        """Delete a graph and its associated data.
        
        Args:
            graph_id: The ID of the graph to delete
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Delete graph_nodes entries
            cursor.execute("DELETE FROM graph_nodes WHERE graph_id = ?", (graph_id,))
            
            # Delete edges
            cursor.execute(
                """
                DELETE FROM edges
                WHERE source_id IN (SELECT node_id FROM graph_nodes WHERE graph_id = ?)
                OR target_id IN (SELECT node_id FROM graph_nodes WHERE graph_id = ?)
                """,
                (graph_id, graph_id)
            )
            
            # Delete nodes
            cursor.execute(
                """
                DELETE FROM nodes
                WHERE id IN (SELECT node_id FROM graph_nodes WHERE graph_id = ?)
                """,
                (graph_id,)
            )
            
            # Delete graph
            cursor.execute("DELETE FROM graphs WHERE id = ?", (graph_id,))
            
            conn.commit() 