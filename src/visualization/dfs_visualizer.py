from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QComboBox, QInputDialog, QMessageBox, QDialog, QLineEdit, QSlider, QSpinBox, QDialogButtonBox, QFormLayout, QGraphicsDropShadowEffect
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPainter, QColor, QPen, QFont, QIcon
import sys
import random
from typing import Dict, List, Tuple, Set
from .map_visualizer import MapVisualizer
from ..core.graph.graph import Graph
from ..core.graph.node import Node
from ..core.graph.edge import Edge
from ..core.algorithms.dfs import DepthFirstSearch
from ..core.algorithms.greedy import GreedyBestFirstSearch
import json
import os
from datetime import datetime

class SaveMapDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Save Map")
        self.setFixedWidth(400)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Create form layout for inputs
        form_layout = QFormLayout()
        
        # Add name input with validation
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter a name for your map...")
        form_layout.addRow("Map Name:", self.name_input)
        
        # Add description input (optional)
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Optional description...")
        form_layout.addRow("Description:", self.description_input)
        
        layout.addLayout(form_layout)
        
        # Add some spacing
        layout.addSpacing(20)
        
        # Add buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
        
    def get_data(self):
        return {
            'name': self.name_input.text().strip(),
            'description': self.description_input.text().strip()
        }

class PathVisualizer(MapVisualizer):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.visited_nodes: Set[str] = set()
        self.current_path: List[str] = []
        self.path_steps: List[List[str]] = []
        self.step_index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_step)
        self.animation_speed = 1000  # Slower animation (1 second per step)
        
        # Create maps directory if it doesn't exist
        self.maps_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'maps')
        os.makedirs(self.maps_dir, exist_ok=True)
        
        # Updated color scheme
        self.visited_color = QColor(100, 149, 237)  # Cornflower blue for visited nodes
        self.current_color = QColor(255, 215, 0)    # Gold for current path
        self.start_color = QColor(50, 205, 50)      # Lime green for start node
        self.target_color = QColor(220, 20, 60)     # Crimson for target node
        self.future_color = QColor(169, 169, 169)   # Dark gray for future nodes
        self.edge_color = QColor(128, 128, 128)     # Gray for unvisited edges
        self.visited_edge_color = QColor(100, 149, 237)  # Cornflower blue for visited edges
        self.current_edge_color = QColor(255, 215, 0)    # Gold for current path edges
        
        # Data structure tracking
        self.stack = []  # For DFS
        self.priority_queue = []  # For Greedy
        self.unvisited_nodes = set()  # For both algorithms
        
        self.total_steps = 0
        self.start_node = None
        self.target_node = None
        self.selection_mode = 'start'  # 'start' or 'end'
        
        # Updated algorithm steps with shorter lines
        self.dfs_steps = [
            "1. Start at selected node",
            "2. Mark node as visited",
            "3. Add to current path",
            "4. Get unvisited neighbors",
            "5. For each neighbor:",
            "   Move to neighbor",
            "   Explore recursively",
            "6. Backtrack if needed",
            "7. Continue till done"
        ]
        
        self.greedy_steps = [
            "1. Start at selected node",
            "2. Calculate heuristics",
            "3. Add to priority queue",
            "4. While queue has nodes:",
            "   Get lowest h-value",
            "   Check if target found",
            "   Mark as visited",
            "   Add to current path",
            "   Queue new neighbors",
            "5. No path if queue empty"
        ]
        
        self.node_count = 100  # Default node count
        
        # Create control panel
        self.setup_controls()
        
        # Set window size
        self.setMinimumSize(1600, 1000)  # Increased minimum width to accommodate panels
        
    def setup_controls(self):
        """Create modern control panel with algorithm selection and controls"""
        # Create control panel widget with dark background
        control_panel = QWidget(self)
        control_panel.setStyleSheet("""
            QWidget {
                background-color: #2D2D37;
                border-radius: 8px;
            }
            QPushButton {
                background-color: #3D3D47;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #4D4D57;
            }
            QPushButton:pressed {
                background-color: #5D5D67;
            }
            QComboBox {
                background-color: #3D3D47;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                min-width: 120px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
                background: #4D4D57;
                width: 12px;
                height: 12px;
                border-radius: 6px;
            }
            QComboBox QAbstractItemView {
                background-color: #3D3D47;
                color: white;
                selection-background-color: #4D4D57;
                selection-color: white;
                border: none;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
            QSpinBox {
                background-color: #3D3D47;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QSlider {
                height: 24px;
            }
            QSlider::groove:horizontal {
                background: #3D3D47;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #6D6D77;
                width: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }
            QSlider::handle:horizontal:hover {
                background: #7D7D87;
            }
        """)
        
        # Main horizontal layout with padding
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20, 10, 20, 10)  # Reduced vertical padding
        main_layout.setSpacing(20)  # Slightly reduced spacing between groups
        
        # Left group - Algorithm Controls
        left_group = QWidget()
        left_group.setStyleSheet("background-color: #35353F; padding: 10px; border-radius: 6px;")
        left_layout = QHBoxLayout()
        left_layout.setSpacing(15)
        
        # Algorithm selector with label
        algo_label = QLabel("Algorithm:")
        left_layout.addWidget(algo_label)
        
        self.algo_selector = QComboBox()
        self.algo_selector.addItems(['DFS Explore', 'Greedy Path'])
        self.algo_selector.currentTextChanged.connect(self.algorithm_changed)
        self.algo_selector.setMinimumWidth(120)
        left_layout.addWidget(self.algo_selector)
        
        # Control buttons
        self.start_button = QPushButton('Start')
        self.start_button.setStyleSheet("background-color: #4CAF50;")  # Green for start
        self.start_button.clicked.connect(self.start_algorithm)
        left_layout.addWidget(self.start_button)
        
        self.reset_button = QPushButton('Reset')
        self.reset_button.clicked.connect(self.reset_visualization)
        left_layout.addWidget(self.reset_button)
        
        left_group.setLayout(left_layout)
        main_layout.addWidget(left_group)
        
        # Center group - Node Count Controls
        center_group = QWidget()
        center_group.setStyleSheet("background-color: #35353F; padding: 10px; border-radius: 6px;")
        center_layout = QHBoxLayout()
        center_layout.setSpacing(15)
        
        # Node count controls
        node_count_label = QLabel("Nodes:")
        center_layout.addWidget(node_count_label)
        
        self.node_count_spin = QSpinBox()
        self.node_count_spin.setRange(10, 200)
        self.node_count_spin.setValue(self.node_count)
        self.node_count_spin.valueChanged.connect(self.update_node_count)
        self.node_count_spin.setMinimumWidth(70)
        center_layout.addWidget(self.node_count_spin)
        
        self.node_count_slider = QSlider(Qt.Orientation.Horizontal)
        self.node_count_slider.setRange(10, 200)
        self.node_count_slider.setValue(self.node_count)
        self.node_count_slider.setMinimumWidth(150)  # Make slider wider
        self.node_count_slider.valueChanged.connect(self.node_count_spin.setValue)
        self.node_count_spin.valueChanged.connect(self.node_count_slider.setValue)
        center_layout.addWidget(self.node_count_slider)
        
        center_group.setLayout(center_layout)
        main_layout.addWidget(center_group)
        
        # Right group - Map Controls
        right_group = QWidget()
        right_group.setStyleSheet("background-color: #35353F; padding: 10px; border-radius: 6px;")
        right_layout = QHBoxLayout()
        right_layout.setSpacing(15)
        
        # Map management buttons
        self.random_button = QPushButton('Random Map')
        self.random_button.clicked.connect(self.randomize_map)
        right_layout.addWidget(self.random_button)
        
        self.save_button = QPushButton('Save Map')
        self.save_button.clicked.connect(self.save_map)
        right_layout.addWidget(self.save_button)
        
        # Load map selector with label
        load_label = QLabel("Load:")
        right_layout.addWidget(load_label)
        
        self.map_selector = QComboBox()
        self.map_selector.addItem("Select Map...")
        self.update_map_list()
        self.map_selector.currentTextChanged.connect(self.load_map)
        self.map_selector.setMinimumWidth(150)  # Increased width for map selector
        right_layout.addWidget(self.map_selector)
        
        right_group.setLayout(right_layout)
        main_layout.addWidget(right_group)
        
        # Set the main layout
        control_panel.setLayout(main_layout)
        
        # Size and position the control panel
        control_panel.setFixedHeight(80)
        control_panel.setMinimumWidth(1500)  # Increased width
        control_panel.move(20, 10)  # Moved left edge closer to window edge
        
        # Add drop shadow effect to the control panel
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 50))
        control_panel.setGraphicsEffect(shadow)
        
    def update_map_list(self):
        """Update the list of available maps"""
        self.map_selector.clear()
        self.map_selector.addItem("Select Map...")
        
        # List all JSON files in the maps directory
        if os.path.exists(self.maps_dir):
            for filename in os.listdir(self.maps_dir):
                if filename.endswith('.json'):
                    self.map_selector.addItem(filename[:-5])  # Remove .json extension
                    
    def update_node_count(self, value):
        """Update node count and regenerate map"""
        self.node_count = value
        self.randomize_map()
        
    def save_map(self):
        """Save the current map to a file with custom name"""
        dialog = SaveMapDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            name = data['name']
            description = data['description']
            
            if not name:
                QMessageBox.warning(self, "Error", "Please enter a map name.")
                return
                
            # Clean the filename to be safe
            safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '_', '-'))
            filename = f"{safe_name}.json"
            filepath = os.path.join(self.maps_dir, filename)
            
            # Check if file already exists
            if os.path.exists(filepath):
                reply = QMessageBox.question(
                    self, 
                    'Map exists', 
                    'A map with this name already exists. Do you want to overwrite it?',
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.No:
                    return
            
            # Prepare map data
            map_data = {
                'nodes': {node_id: [x, y] for node_id, (x, y) in self.nodes.items()},
                'edges': self.edges,
                'name': safe_name,
                'description': description,
                'node_count': self.node_count,
                'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Save to file
            with open(filepath, 'w') as f:
                json.dump(map_data, f, indent=2)
                
            print(f"Saved map '{safe_name}' to {filepath}")
            self.update_map_list()
        
    def load_map(self, map_name):
        """Load a map from a file"""
        if map_name == "Select Map...":
            return
            
        filepath = os.path.join(self.maps_dir, f"{map_name}.json")
        
        try:
            with open(filepath, 'r') as f:
                map_data = json.load(f)
                
            # Convert node positions back to tuples
            nodes = {node_id: tuple(pos) for node_id, pos in map_data['nodes'].items()}
            edges = map_data['edges']
            
            # Set the new graph
            self.set_graph(nodes, edges)
            self.reset_visualization()
            print(f"Loaded map from {filepath}")
            
        except Exception as e:
            print(f"Error loading map: {e}")
            
    def randomize_map(self):
        """Create a new random map"""
        # Calculate grid dimensions based on node count
        # Try to keep it roughly square
        side = int(self.node_count ** 0.5)
        width = side
        height = self.node_count // side
        if width * height < self.node_count:
            width += 1
        
        # Generate new random grid
        nodes, edges = create_interesting_grid(width, height, self.node_count)
        
        # Set the new graph
        self.set_graph(nodes, edges)
        self.reset_visualization()
        print(f"Created new random map with {self.node_count} nodes")
        
    def reset_visualization(self):
        """Reset the visualization state"""
        self.stop_animation()
        self.visited_nodes.clear()
        self.current_path.clear()
        self.step_index = 0
        # Don't reset selection_mode, start_node, or target_node
        # This allows rerunning the algorithm with the same nodes
        self.update()

    def mousePressEvent(self, event):
        """Handle mouse clicks for selecting start and end nodes"""
        # Find closest node to click
        click_x = event.position().x()
        click_y = event.position().y()
        closest_node = None
        min_dist = float('inf')
        
        # Don't process clicks in the control panel or info panel areas
        if click_y < 100 or click_x > self.width() - 220:
            return
        
        for node_id, (x, y) in self.nodes.items():
            dist = ((x - click_x) ** 2 + (y - click_y) ** 2) ** 0.5
            if dist < min_dist:
                min_dist = dist
                closest_node = node_id
        
        if closest_node and min_dist < 30:  # Only select if click is close enough
            if self.algo_selector.currentText() == 'Greedy Path':
                if self.selection_mode == 'start':
                    self.start_node = closest_node
                    self.selection_mode = 'end'
                    self.show_status_message(f"Selected start node {closest_node}. Now click to select end node.")
                else:
                    if closest_node == self.start_node:
                        self.show_status_message("Cannot select same node as start and end. Please choose a different node.")
                        return
                    self.target_node = closest_node
                    self.selection_mode = 'start'
                    self.show_status_message(f"Selected end node {closest_node}. Click Start to begin pathfinding.")
            else:  # DFS mode
                self.start_node = closest_node
                self.target_node = None  # Clear target node in DFS mode
                self.show_status_message(f"Selected start node {closest_node}. Click Start to begin exploration.")
            self.update()

    def show_status_message(self, message):
        """Show a status message to the user"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText(message)
        msg.setWindowTitle("Status")
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2D2D37;
            }
            QMessageBox QLabel {
                color: white;
                font-size: 12px;
            }
            QPushButton {
                background-color: #3D3D47;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #4D4D57;
            }
        """)
        msg.exec()

    def set_path_steps(self, steps: List[List[str]]):
        """Set the path steps to visualize"""
        print(f"Setting {len(steps)} path steps")
        self.path_steps = steps
        self.total_steps = len(steps)
        self.step_index = 0
        self.visited_nodes.clear()
        self.current_path.clear()
        # Initialize unvisited nodes
        self.unvisited_nodes = set(self.nodes.keys())
        # Initialize data structures
        self.stack = []
        self.priority_queue = []

    def start_algorithm(self):
        """Start the selected algorithm"""
        # Validate start node
        if not self.start_node or self.start_node not in self.nodes:
            self.show_status_message("Please select a valid start node by clicking on any node in the graph.")
            return
            
        # Validate target node for Greedy
        if self.algo_selector.currentText() == 'Greedy Path':
            if not self.target_node or self.target_node not in self.nodes:
                self.show_status_message("Please select a valid end node by clicking on another node in the graph.")
                return
            if self.start_node == self.target_node:
                self.show_status_message("Start and end nodes cannot be the same. Please select different nodes.")
                return
            
        self.reset_visualization()
        
        try:
            if self.algo_selector.currentText() == 'DFS Explore':
                # Run DFS exploration from the start node
                print(f"Running DFS from start node: {self.start_node}")
                steps = run_dfs(self.nodes, self.edges, self.start_node)
                if steps:
                    self.set_path_steps(steps)
                    self.start_animation()
                else:
                    self.show_status_message(f"No valid path found from node {self.start_node}.")
            
            elif self.algo_selector.currentText() == 'Greedy Path':
                # Run Greedy pathfinding
                print(f"Running Greedy algorithm from {self.start_node} to {self.target_node}")
                steps = run_greedy(self.nodes, self.edges, self.start_node, self.target_node)
                if steps:
                    self.set_path_steps(steps)
                    self.start_animation()
                else:
                    self.show_status_message(f"No path found from {self.start_node} to {self.target_node}.")
                    
        except Exception as e:
            print(f"Error running algorithm: {e}")
            self.show_status_message(f"Error running algorithm: {str(e)}")
            import traceback
            traceback.print_exc()

    def algorithm_changed(self):
        """Handle algorithm selection change"""
        self.reset_visualization()
        # Clear nodes when changing algorithms
        self.start_node = None
        self.target_node = None
        self.selection_mode = 'start'
        if self.algo_selector.currentText() == 'DFS Explore':
            self.show_status_message("DFS Mode: Click any node to set it as the start node for exploration.")
        else:
            self.show_status_message("Greedy Mode: First click a node to set start, then click another for the end node.")

    def _draw_background(self, painter):
        """Draw the dark background"""
        painter.fillRect(0, 0, self.width(), self.height(), QColor(30, 30, 35))
        
    def paintEvent(self, event):
        """Override paint event to show algorithm state"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw the base map first
        self._draw_background(painter)
        
        # Draw step information at the top
        self._draw_step_info(painter)
        
        # Draw the graph
        self._draw_edges(painter)
        self._draw_nodes(painter)
        
        # Draw info panels
        self._draw_data_structure_panel(painter)
        self._draw_educational_panel(painter)
        
    def _draw_step_info(self, painter):
        """Draw step counter and progress bar"""
        # Panel background for steps - moved to right side
        panel_x = self.width() - 220  # 220px from right edge
        panel_y = 100  # Just below control panel
        panel_width = 200
        panel_height = 150  # Reduced height
        painter.fillRect(panel_x, panel_y, panel_width, panel_height, QColor(45, 45, 55))
        
        # Draw step counter
        font = QFont("Arial", 14)
        painter.setFont(font)
        text = f"Step: {self.step_index}/{self.total_steps}"
        painter.setPen(Qt.GlobalColor.white)
        painter.drawText(panel_x + 10, panel_y + 30, text)
        
        # Draw progress bar background
        bar_width = 180  # Adjusted to fit panel
        bar_height = 20
        x = panel_x + 10
        y = panel_y + 40
        painter.fillRect(x, y, bar_width, bar_height, QColor(60, 60, 70))
        
        # Draw progress bar
        if self.total_steps > 0:
            progress = self.step_index / self.total_steps
            progress_width = int(bar_width * progress)
            painter.fillRect(x, y, progress_width, bar_height, self.current_color)
            
        # Draw current algorithm step description
        if self.total_steps > 0:
            steps = self.dfs_steps if self.algo_selector.currentText() == 'DFS Explore' else self.greedy_steps
            current_step = int((self.step_index / self.total_steps) * len(steps))
            if current_step < len(steps):
                painter.setPen(self.current_color)
                painter.setFont(QFont("Arial", 12))
                
                # Create text rectangle for word wrapping
                text = steps[current_step]
                text_rect = painter.boundingRect(
                    panel_x + 10, panel_y + 70,
                    panel_width - 20, 60,
                    Qt.TextFlag.TextWordWrap | Qt.AlignmentFlag.AlignLeft,
                    text
                )
                
                # Draw the text with proper flags
                painter.drawText(
                    text_rect,
                    Qt.TextFlag.TextWordWrap | Qt.AlignmentFlag.AlignLeft,
                    text
                )

    def _draw_edges(self, painter):
        """Override edge drawing to show visited edges"""
        # Draw unvisited edges
        pen = QPen(self.edge_color)
        pen.setWidth(2)
        painter.setPen(pen)
        
        for start_id, end_id in self.edges:
            if start_id in self.nodes and end_id in self.nodes:
                start_pos = self.nodes[start_id]
                end_pos = self.nodes[end_id]
                
                # Check if this edge is part of the current path
                is_current = False
                if len(self.current_path) > 1:
                    for i in range(len(self.current_path) - 1):
                        if (self.current_path[i] == start_id and self.current_path[i+1] == end_id) or \
                           (self.current_path[i] == end_id and self.current_path[i+1] == start_id):
                            is_current = True
                            break
                
                # Draw edge with appropriate color
                if is_current:
                    # Draw glowing edge for current path
                    glow_pen = QPen(self.current_edge_color)
                    for width in [8, 6, 4, 2]:
                        glow_pen.setWidth(width)
                        painter.setPen(glow_pen)
                        painter.drawLine(
                            int(start_pos[0]), int(start_pos[1]),
                            int(end_pos[0]), int(end_pos[1])
                        )
                elif start_id in self.visited_nodes and end_id in self.visited_nodes:
                    # Draw visited edge
                    painter.setPen(QPen(self.visited_edge_color, 2))
                    painter.drawLine(
                        int(start_pos[0]), int(start_pos[1]),
                        int(end_pos[0]), int(end_pos[1])
                    )
                else:
                    # Draw unvisited edge
                    painter.setPen(pen)
                    painter.drawLine(
                        int(start_pos[0]), int(start_pos[1]),
                        int(end_pos[0]), int(end_pos[1])
                    )
                    
    def _draw_nodes(self, painter):
        """Override node drawing to show algorithm state"""
        for node_id, (x, y) in self.nodes.items():
            # Draw visited nodes in a different color
            if node_id == self.start_node:
                # Start node in lime green
                self._draw_node_with_glow(painter, x, y, self.start_color)
            elif node_id == self.target_node:
                # Target node in crimson
                self._draw_node_with_glow(painter, x, y, self.target_color)
            elif node_id in self.visited_nodes:
                if node_id in self.current_path:
                    # Current path nodes in gold
                    self._draw_node_with_glow(painter, x, y, self.current_color)
                else:
                    # Visited nodes in cornflower blue
                    self._draw_node_with_glow(painter, x, y, self.visited_color)
            else:
                # Unvisited nodes in dark gray
                self._draw_node_with_glow(painter, x, y, self.future_color)
            
            # Draw node label
            painter.setPen(Qt.GlobalColor.white)
            painter.setFont(QFont("Arial", 8))
            
            # Get node text metrics to center it
            metrics = painter.fontMetrics()
            text_width = metrics.horizontalAdvance(node_id)
            text_x = int(x - text_width // 2)  # Convert to int
            text_y = int(y + 20)  # Convert to int
            
            # Create a point for the text position
            painter.drawText(text_x, text_y, node_id)

    def _draw_data_structure_panel(self, painter):
        """Draw the data structure panel showing visited nodes"""
        # Panel background - positioned below steps panel
        panel_x = self.width() - 220
        panel_y = 270  # Moved down below steps panel
        panel_width = 200
        panel_height = 400
        painter.fillRect(panel_x, panel_y, panel_width, panel_height, QColor(45, 45, 55))
        
        # Panel title
        font = QFont("Arial", 14, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(Qt.GlobalColor.white)
        title = "Visited Nodes"
        painter.drawText(panel_x + 10, panel_y + 30, title)
        
        # Draw visited nodes in a grid format
        y = panel_y + 60
        visited_list = sorted(list(self.visited_nodes))
        
        # Calculate grid dimensions
        nodes_per_row = 4  # Show 4 nodes per row
        node_width = 45    # Slightly wider nodes
        
        # Draw nodes in a grid
        for i, node in enumerate(visited_list):
            row = i // nodes_per_row
            col = i % nodes_per_row
            
            # Calculate position
            x = panel_x + 10 + (col * node_width)
            y = panel_y + 60 + (row * 30)  # 30 pixels per row
            
            # Draw node with background
            node_width = 40  # Slightly wider
            node_height = 25
            
            # Use different background colors based on node type
            if node == self.start_node:
                bg_color = self.start_color
            elif node == self.target_node:
                bg_color = self.target_color
            elif node in self.current_path:
                bg_color = self.current_color
            else:
                bg_color = self.visited_color
            
            # Draw background
            painter.fillRect(x, y, node_width, node_height, bg_color)
            
            # Draw border with slightly darker version of background color
            painter.setPen(QPen(bg_color.darker(120)))
            painter.drawRect(x, y, node_width, node_height)
            
            # Draw node text in black for better visibility
            painter.setPen(Qt.GlobalColor.black)
            painter.setFont(QFont("Arial", 8))  # Slightly smaller font to fit node IDs
            
            # Get node text metrics to center it
            metrics = painter.fontMetrics()
            text_width = metrics.horizontalAdvance(node)
            text_x = x + (node_width - text_width) // 2
            text_y = y + (node_height + metrics.height()) // 2 - 2  # -2 for slight vertical adjustment
            
            painter.drawText(text_x, text_y, node)
        
        # Draw count at the bottom
        y = panel_y + panel_height - 30
        painter.setPen(Qt.GlobalColor.white)
        painter.setFont(QFont("Arial", 12))
        painter.drawText(panel_x + 10, y, f"Total: {len(visited_list)} nodes")

    def _draw_educational_panel(self, painter):
        """Draw the educational panel showing algorithm steps"""
        # Panel background - positioned at bottom
        panel_x = self.width() - 220
        panel_y = 690  # Moved down below visited nodes panel
        panel_width = 200
        panel_height = 280  # Reduced height to fit in window
        painter.fillRect(panel_x, panel_y, panel_width, panel_height, QColor(45, 45, 55))
        
        # Panel title
        font = QFont("Arial", 14, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(Qt.GlobalColor.white)
        title = "Algorithm Steps"
        painter.drawText(panel_x + 10, panel_y + 30, title)
        
        # Get current algorithm steps
        steps = self.dfs_steps if self.algo_selector.currentText() == 'DFS Explore' else self.greedy_steps
        
        # Draw each step with word wrapping
        y = panel_y + 60
        for i, step in enumerate(steps, 1):
            # Calculate which step should be highlighted based on current path
            if self.total_steps > 0:
                current_step = i - 1
                total_steps = len(steps)
                current_progress = self.step_index / self.total_steps
                highlighted_step = int(current_progress * total_steps)
                
                if current_step == highlighted_step:
                    painter.setPen(self.current_color)
                    painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
                elif current_step < highlighted_step:
                    painter.setPen(self.visited_color)
                    painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
                else:
                    painter.setPen(self.future_color)
                    painter.setFont(QFont("Arial", 10))
            else:
                painter.setPen(self.future_color)
                painter.setFont(QFont("Arial", 10))
            
            # Calculate text bounding rectangle
            metrics = painter.fontMetrics()
            text_width = panel_width - 20  # Leave 10px padding on each side
            
            # Split text into words and create wrapped lines
            words = step.split()
            current_line = words[0]
            lines = []
            
            for word in words[1:]:
                test_line = current_line + " " + word
                if metrics.horizontalAdvance(test_line) <= text_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word
            lines.append(current_line)
            
            # Draw each line
            line_height = metrics.height()
            for line in lines:
                painter.drawText(panel_x + 10, y + line_height, line)
                y += line_height
            
            y += 5  # Add padding between steps

    def start_animation(self):
        """Start the animation"""
        print(f"Starting animation with {self.total_steps} steps")
        self.timer.start(self.animation_speed)
        
    def stop_animation(self):
        """Stop the animation"""
        self.timer.stop()
        
    def next_step(self):
        """Show the next step in the animation"""
        if self.step_index < len(self.path_steps):
            self.current_path = self.path_steps[self.step_index]
            self.visited_nodes.update(self.current_path)
            self.unvisited_nodes.difference_update(self.current_path)
            
            # Update data structures based on algorithm
            if self.algo_selector.currentText() == 'DFS Explore':
                # For DFS, stack contains the current path
                self.stack = self.current_path.copy()
            else:  # Greedy
                # For Greedy, priority queue contains unvisited neighbors with their heuristics
                self.priority_queue = []
                for node in self.current_path:
                    if node in self.nodes:
                        # Calculate heuristic (distance to target)
                        if self.target_node and self.target_node in self.nodes:
                            current_pos = self.nodes[node]
                            target_pos = self.nodes[self.target_node]
                            heuristic = ((current_pos[0] - target_pos[0])**2 + 
                                       (current_pos[1] - target_pos[1])**2)**0.5
                            self.priority_queue.append((node, heuristic))
            
            self.step_index += 1
            print(f"Showing step {self.step_index}/{self.total_steps}")
            self.update()  # Force a repaint
        else:
            print("Animation complete")
            self.timer.stop()

    def _draw_node_with_glow(self, painter, x, y, color):
        """Draw a node with a glowing effect and increased size"""
        # Draw glow
        for size in [20, 16, 12, 8]:
            glow_color = QColor(color)
            glow_color.setAlpha(50)
            painter.setPen(QPen(glow_color, size))
            painter.drawPoint(int(x), int(y))
        
        # Draw main node
        painter.setPen(QPen(color, 2))
        painter.setBrush(color)
        painter.drawEllipse(int(x) - 6, int(y) - 6, 12, 12)

def create_interesting_grid(width: int, height: int, target_nodes: int) -> Tuple[Dict[str, Tuple[float, float]], List[Tuple[str, str]]]:
    """Create a more organic and random graph structure with specified node count"""
    nodes = {}
    edges = []
    
    # Calculate available space (accounting for right panel and margins)
    WINDOW_WIDTH = 1600
    WINDOW_HEIGHT = 1000
    RIGHT_PANEL_WIDTH = 250
    TOP_MARGIN = 100
    BOTTOM_MARGIN = 50
    LEFT_MARGIN = 50
    RIGHT_MARGIN = RIGHT_PANEL_WIDTH + 50
    
    # Calculate usable area
    usable_width = WINDOW_WIDTH - LEFT_MARGIN - RIGHT_MARGIN
    usable_height = WINDOW_HEIGHT - TOP_MARGIN - BOTTOM_MARGIN
    
    # Calculate center point of usable area
    center_x = LEFT_MARGIN + (usable_width / 2)
    center_y = TOP_MARGIN + (usable_height / 2)
    
    # Calculate optimal node spacing based on available space and node count
    area_per_node = (usable_width * usable_height) / target_nodes
    node_spacing = min(
        usable_width / (width + 1),
        usable_height / (height + 1),
        (area_per_node ** 0.5) * 1.5  # 1.5 factor for some spacing between nodes
    )
    
    # Calculate grid dimensions to center it
    grid_width = node_spacing * (width - 1)
    grid_height = node_spacing * (height - 1)
    start_x = center_x - (grid_width / 2)
    start_y = center_y - (grid_height / 2)
    
    # Use sequential numbering for nodes
    node_counter = 1
    node_positions = []  # Store actual positions for better distribution
    
    # Create base nodes with more random positioning
    attempts_per_node = 50
    total_attempts = 0
    while len(nodes) < target_nodes and total_attempts < target_nodes * attempts_per_node:
        # Calculate random position within usable area
        x = random.uniform(start_x, start_x + grid_width)
        y = random.uniform(start_y, start_y + grid_height)
        
        # Add some clustering tendency towards the center
        if random.random() < 0.3:  # 30% chance of clustering
            x = x * 0.7 + center_x * 0.3
            y = y * 0.7 + center_y * 0.3
        
        # Check if position is too close to existing nodes
        too_close = False
        for pos in node_positions:
            dist = ((pos[0] - x) ** 2 + (pos[1] - y) ** 2) ** 0.5
            min_distance = node_spacing * 0.6
            if dist < min_distance:
                too_close = True
                break
        
        if not too_close:
            node_id = f"Node {node_counter}"
            nodes[node_id] = (x, y)
            node_positions.append((x, y))
            node_counter += 1
        
        total_attempts += 1
    
    # Create edges with varying patterns
    node_list = list(nodes.keys())
    for i, node1 in enumerate(node_list):
        pos1 = nodes[node1]
        
        # Connect to nearby nodes with probability based on distance
        for j, node2 in enumerate(node_list[i+1:], i+1):
            pos2 = nodes[node2]
            dist = ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5
            
            # Dynamic max distance based on node spacing
            max_dist = node_spacing * 2.5
            
            if dist <= max_dist:
                # Closer nodes have higher chance of connection
                prob = 1.0 - (dist / max_dist) ** 1.5
                if random.random() < prob:
                    edges.append((node1, node2))
                    
                    # Add some triangular connections for interesting patterns
                    if random.random() < 0.3:
                        # Find a third node to create a triangle
                        potential_thirds = [
                            n for n in node_list 
                            if n != node1 and n != node2
                        ]
                        random.shuffle(potential_thirds)  # Randomize potential connections
                        
                        for node3 in potential_thirds[:5]:  # Only check first 5 candidates
                            pos3 = nodes[node3]
                            dist1 = ((pos1[0] - pos3[0]) ** 2 + (pos1[1] - pos3[1]) ** 2) ** 0.5
                            dist2 = ((pos2[0] - pos3[0]) ** 2 + (pos2[1] - pos3[1]) ** 2) ** 0.5
                            if dist1 <= max_dist and dist2 <= max_dist:
                                edges.append((node1, node3))
                                edges.append((node2, node3))
                                break
    
    # Ensure graph is connected
    def find_connected_components():
        components = {}
        visited = set()
        
        def dfs(node, component):
            visited.add(node)
            components[node] = component
            for edge in edges:
                if edge[0] == node and edge[1] not in visited:
                    dfs(edge[1], component)
                elif edge[1] == node and edge[0] not in visited:
                    dfs(edge[0], component)
        
        component_id = 0
        for node in nodes:
            if node not in visited:
                dfs(node, component_id)
                component_id += 1
        return components
    
    # Connect disconnected components
    components = find_connected_components()
    component_groups = {}
    for node, comp_id in components.items():
        if comp_id not in component_groups:
            component_groups[comp_id] = []
        component_groups[comp_id].append(node)
    
    # Connect components with shortest possible edges
    comp_ids = list(component_groups.keys())
    for i in range(len(comp_ids) - 1):
        comp1 = component_groups[comp_ids[i]]
        comp2 = component_groups[comp_ids[i + 1]]
        min_dist = float('inf')
        closest_pair = None
        
        for node1 in comp1:
            pos1 = nodes[node1]
            for node2 in comp2:
                pos2 = nodes[node2]
                dist = ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5
                if dist < min_dist:
                    min_dist = dist
                    closest_pair = (node1, node2)
        
        if closest_pair:
            edges.append(closest_pair)
    
    print(f"\nCreated centered organic grid with {len(nodes)} nodes and {len(edges)} edges")
    return nodes, edges

def run_dfs(nodes: Dict[str, Tuple[float, float]], edges: List[Tuple[str, str]], start_node: str) -> List[List[str]]:
    """Run DFS and return the steps"""
    graph = create_graph(nodes, edges)
    dfs = DepthFirstSearch(graph)
    path_steps = []
    
    def step_callback(current_path):
        path_steps.append(current_path.copy())
    
    dfs.run(start_node, step_callback)
    return path_steps

def run_greedy(nodes: Dict[str, Tuple[float, float]], edges: List[Tuple[str, str]], 
               start_node: str, target_node: str) -> List[List[str]]:
    """Run Greedy Best-First Search and return the steps"""
    print(f"\nStarting Greedy search from {start_node} to {target_node}")
    graph = create_graph(nodes, edges)
    greedy = GreedyBestFirstSearch(graph)
    path_steps = []
    
    def step_callback(current_path):
        print(f"Greedy step: {current_path}")
        path_steps.append(current_path.copy())
    
    # Run the algorithm and ensure we capture all steps
    print(f"Running Greedy algorithm with start={start_node}, target={target_node}")
    final_path = greedy.run(start_node, target_node, step_callback)
    print(f"Final path found: {final_path}")
    
    # If no path was found, return empty steps
    if not final_path:
        print("No path found to target")
        return []
    
    print(f"Found path with {len(path_steps)} steps")
    return path_steps

def create_graph(nodes: Dict[str, Tuple[float, float]], edges: List[Tuple[str, str]]) -> Graph:
    """Create a Graph object from nodes and edges"""
    print(f"Creating graph with {len(nodes)} nodes and {len(edges)} edges")
    graph = Graph(directed=False)  # Create an undirected graph
    
    # Add nodes
    for node_id, pos in nodes.items():
        node = Node(
            id=node_id,
            name=node_id,
            position=pos,
            weight=1.0
        )
        graph.add_node(node)
        print(f"Added node: {node_id} at position {pos}")
    
    # Add edges
    for start, end in edges:
        if start not in graph.nodes or end not in graph.nodes:
            print(f"Warning: Edge {start}->{end} references non-existent nodes")
            continue
            
        source = graph.nodes[start]
        target = graph.nodes[end]
        
        # Create a single edge - the Graph class will handle the reverse edge
        edge = Edge(
            source=source,
            target=target,
            weight=1.0,
            directed=False
        )
        
        try:
            graph.add_edge(edge)
            print(f"Added undirected edge: {start} <-> {end}")
        except Exception as e:
            print(f"Error adding edge {start}->{end}: {e}")
    
    # Print adjacency list for debugging
    print("\nAdjacency list:")
    for node_id, neighbors in graph.adjacency_list.items():
        print(f"{node_id}: {neighbors}")
    
    # Verify graph structure
    print("\nGraph verification:")
    print(f"Number of nodes: {len(graph.nodes)}")
    print(f"Number of edges: {len(graph.edges)}")
    print(f"Number of adjacency list entries: {len(graph.adjacency_list)}")
    
    # Verify start node has neighbors
    start_node = min(nodes.keys(), key=lambda n: nodes[n][0])
    print(f"\nVerifying start node {start_node}:")
    print(f"Neighbors: {graph.get_neighbors(start_node)}")
    
    # Verify target node exists and has neighbors
    if 'target_node' in locals():
        print(f"\nVerifying target node {target_node}:")
        print(f"Exists: {target_node in graph.nodes}")
        if target_node in graph.nodes:
            print(f"Neighbors: {graph.get_neighbors(target_node)}")
    
    return graph

def main():
    app = QApplication(sys.argv)
    
    # Create visualization
    vis = PathVisualizer()
    vis.setWindowTitle('Path Visualization')
    vis.setMinimumSize(1600, 1000)  # Increased minimum width
    
    # Create initial grid with default node count
    nodes, edges = create_interesting_grid(10, 10, vis.node_count)
    vis.set_graph(nodes, edges)
    
    # Show visualization
    vis.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 