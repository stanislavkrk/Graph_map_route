# Description

This program simulates a simplified logistics map of major cities in the European Union, represented as a graph. Its primary purpose is to calculate the shortest route between two cities, factoring in distance and average travel speed. The implementation leverages Dijkstra's algorithm to efficiently determine the optimal path.

# Features

- Graph
  - Nodes: Represent cities, with coordinates provided for visualization.
  - Edges: Represent roads with two key parameters:
    - Distance: The distance between connected cities.
    - Average Speed: The estimated average travel speed.

- Visualization
  - A graphical representation of the logistics network:
    - Cities (nodes) are displayed as points.
    - Roads (edges) are displayed as connecting lines.

- Shortest Route Calculation
  - Implements Dijkstra's Algorithm to find the shortest path between two user-selected cities.
  - Utilizes a priority queue (heapq) to optimize route computation.

- Result Output
  - Shortest Route: Lists the sequence of cities forming the shortest path.
  - Travel Time: Calculates and displays the total travel time for the route.
  - Route Visualization: Highlights the identified shortest route on the graph.
