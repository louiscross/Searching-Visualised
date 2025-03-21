from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter, QColor, QPen, QRadialGradient, QPainterPath
from PyQt6.QtCore import Qt, QPointF
import sys
import math

class MapVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Dark theme colors
        self.background_color = QColor(25, 25, 35)
        self.grid_color = QColor(45, 45, 55)
        self.highlight_color = QColor(255, 215, 0)  # Golden yellow
        self.node_color = QColor(200, 200, 220)
        
        # Grid settings
        self.grid_size = 40
        self.grid_opacity = 0.3
        
        # Initialize empty graph data
        self.nodes = {}  # Format: {node_id: (x, y)}
        self.edges = []  # Format: [(from_id, to_id)]
        self.highlighted_path = []  # Format: [node_id1, node_id2, ...]
        
        # Window settings
        self.setMinimumSize(800, 600)
        self.setWindowTitle('Graph Visualization')
        
    def set_graph(self, nodes, edges):
        """Set the graph to be visualized"""
        self.nodes = nodes
        self.edges = edges
        self.update()
        
    def set_highlighted_path(self, path):
        """Set the path to be highlighted"""
        self.highlighted_path = path
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw background
        painter.fillRect(self.rect(), self.background_color)
        
        # Draw grid
        self._draw_grid(painter)
        
        # Draw edges
        self._draw_edges(painter)
        
        # Draw highlighted path
        self._draw_highlighted_path(painter)
        
        # Draw nodes
        self._draw_nodes(painter)
        
    def _draw_grid(self, painter):
        """Draw a grid pattern that looks like a map background"""
        pen = QPen(self.grid_color)
        pen.setWidth(1)
        painter.setPen(pen)
        
        # Draw vertical lines
        for x in range(0, self.width(), self.grid_size):
            painter.drawLine(x, 0, x, self.height())
            
        # Draw horizontal lines
        for y in range(0, self.height(), self.grid_size):
            painter.drawLine(0, y, self.width(), y)
            
    def _draw_edges(self, painter):
        """Draw regular edges"""
        pen = QPen(self.grid_color.lighter(150))
        pen.setWidth(2)
        painter.setPen(pen)
        
        for start_id, end_id in self.edges:
            if start_id in self.nodes and end_id in self.nodes:
                start_pos = self.nodes[start_id]
                end_pos = self.nodes[end_id]
                painter.drawLine(
                    int(start_pos[0]), int(start_pos[1]),
                    int(end_pos[0]), int(end_pos[1])
                )
                
    def _draw_highlighted_path(self, painter):
        """Draw the highlighted path with glow effect"""
        if len(self.highlighted_path) < 2:
            return
            
        # Draw glow
        glow_pen = QPen(self.highlight_color)
        glow_pen.setWidth(8)
        painter.setPen(glow_pen)
        
        path = QPainterPath()
        start_id = self.highlighted_path[0]
        path.moveTo(self.nodes[start_id][0], self.nodes[start_id][1])
        
        for node_id in self.highlighted_path[1:]:
            if node_id in self.nodes:
                path.lineTo(self.nodes[node_id][0], self.nodes[node_id][1])
        
        # Draw the path multiple times for glow effect
        for width in [8, 6, 4, 2]:
            glow_pen.setWidth(width)
            painter.setPen(glow_pen)
            painter.drawPath(path)
            
    def _draw_nodes(self, painter):
        """Draw nodes"""
        for node_id, (x, y) in self.nodes.items():
            self._draw_single_node(painter, x, y, self.node_color)
            
    def _draw_single_node(self, painter, x, y, color):
        """Draw a single node"""
        painter.setBrush(color)
        painter.setPen(QPen(self.grid_color.lighter(150)))
        painter.drawEllipse(QPointF(x, y), 5, 5)
        
    def _draw_node_with_glow(self, painter, x, y, color):
        """Draw a node with a glowing effect"""
        # Draw glow
        glow = QRadialGradient(x, y, 15)
        glow.setColorAt(0, color)
        glow.setColorAt(1, QColor(0, 0, 0, 0))
        painter.setBrush(glow)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPointF(x, y), 15, 15)
        
        # Draw node
        self._draw_single_node(painter, x, y, color)

def main():
    app = QApplication(sys.argv)
    
    # Create visualization
    vis = MapVisualizer()
    
    # Example graph
    nodes = {
        1: (100, 100),
        2: (200, 150),
        3: (300, 100),
        4: (150, 200),
        5: (250, 250),
    }
    
    edges = [
        (1, 2), (2, 3),
        (1, 4), (2, 5),
        (3, 5), (4, 5)
    ]
    
    # Set graph data
    vis.set_graph(nodes, edges)
    
    # Set example highlighted path
    vis.set_highlighted_path([1, 2, 3])
    
    vis.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 