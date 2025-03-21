# Search Algorithm Visualization

> **Note**: This is a work in progress. Not all features are currently integrated, and existing features are being improved as development continues. The project is being actively developed and updated.

> **Repository Status**: While this project builds upon my capstone work, which has received verbal approval for publication, this repository will remain private for security purposes. I'm open to collaboration and welcome discussions about potential improvements or contributions.

A refined and enhanced visualization tool for understanding graph search algorithms, building upon my previous capstone project. This version focuses on providing a more robust and educational experience for learning about pathfinding algorithms.

## Overview

This project evolved from my undergraduate capstone work, where I first explored the challenge of making complex algorithms more accessible through visualization. The new version incorporates several key improvements:

- Modular architecture that separates core algorithms from visualization logic
- Type-safe implementation using Python's type hints for better code maintainability
- Efficient graph representation using adjacency lists for O(1) edge lookups
- Real-time visualization with PyQt6 for smooth user interaction
- Comprehensive test suite ensuring algorithm correctness
- Persistent storage using SQLite for saving and loading graph layouts

## Technical Features

### Graph Implementation
- Custom graph data structure supporting both directed and undirected edges
- Efficient node and edge management with O(1) lookups
- Flexible architecture allowing easy addition of new algorithms

### Search Algorithms
- Depth-First Search (DFS) with step-by-step visualization
- Greedy pathfinding with heuristic-based node selection
- Real-time path visualization and cost calculation

### User Interface
- Interactive 10x10 grid with organic node layout
- Color-coded visualization for algorithm states
- Educational panel showing current algorithm state
- Map management system for saving and loading custom layouts

### Data Persistence
- SQLite database for storing graph layouts and configurations
- Efficient serialization and deserialization of graph structures
- Support for saving and loading custom map layouts

## Project Structure

```
search-algo/
├── src/
│   ├── core/           # Core graph and algorithm implementations
│   │   ├── graph/      # Graph data structures and operations
│   │   └── algorithms/ # Pathfinding algorithms
│   ├── visualization/  # UI and visualization components
│   └── utils/         # Utility functions and helpers
├── tests/             # Test suite
└── Maps/             # Custom map storage
```

## Key Design Decisions

1. **Graph Representation**: Chose adjacency lists over adjacency matrices for better space efficiency with sparse graphs and O(1) edge lookups.

2. **Algorithm Visualization**: Implemented step-by-step visualization to help users understand how algorithms make decisions, rather than just showing the final result.

3. **Type Safety**: Used Python's type hints throughout the codebase to catch potential errors early and improve code maintainability.

4. **Modular Architecture**: Separated core algorithms from visualization logic to make the codebase more maintainable and extensible.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/louiscross/Searching-Visualised.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the visualization tool:
```bash
python -m src.visualization.dfs_visualizer
```

### DFS Mode
1. Select "DFS Explore" from the dropdown
2. Click any node to set it as the start node
3. Click "Start" to begin the exploration

### Greedy Pathfinding Mode
1. Select "Greedy Path" from the dropdown
2. Click to set the start node (green)
3. Click to set the end node (red)
4. Click "Start" to find the path

## Development

- Python 3.8+
- PyQt6 for the UI
- NetworkX for graph operations
- pytest for testing

## License

MIT License
