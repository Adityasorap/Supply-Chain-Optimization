# Supply Chain Optimization Project

## Problem Overview
This project is designed to optimize supply chain operations, focusing on minimizing transportation costs, managing inventory, and determining optimal warehouse locations. The system uses various optimization techniques such as:
- Linear Programming (LP) to minimize transportation and inventory holding costs.
- Mixed-Integer Programming (MIP) for warehouse placement, vehicle selection, and quantity optimization.
- Network Flow Models for optimizing the flow of goods between suppliers, warehouses, and customers.
- Heuristic Algorithms (Greedy) for warehouse selection when dealing with large-scale problems.

## Solution Approach
1. **Linear Programming (LP)**: Formulated a Linear Programming problem to minimize transportation costs while satisfying demand and supply constraints.
2. **Mixed-Integer Programming (MIP)**: Used MIP for optimizing decisions that require discrete variables like warehouse location and vehicle selection.
3. **Network Flow Models**: Used network flow techniques to minimize transportation costs and meet demand while respecting supply capacities.
4. **Heuristic Models**: Implemented a greedy algorithm to select warehouses based on cost-effectiveness, suitable for large-scale supply chain problems.

## Getting Started

### Prerequisites
Ensure you have Python 3.x installed, and install the following dependencies:
```bash
pip install numpy pandas scipy networkx matplotlib pulp
