import pulp
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict

# Define the optimization problem
def create_optimization_model():
    # Create a Linear Program
    prob = pulp.LpProblem("SupplyChainOptimization", pulp.LpMinimize)

    # Define warehouses and customers
    warehouses = ['Warehouse1', 'Warehouse2']
    customers = ['Customer1', 'Customer2', 'Customer3']

    # Define transportation costs (just an example)
    cost = {
        ('Warehouse1', 'Customer1'): 10,
        ('Warehouse1', 'Customer2'): 15,
        ('Warehouse1', 'Customer3'): 20,
        ('Warehouse2', 'Customer1'): 25,
        ('Warehouse2', 'Customer2'): 30,
        ('Warehouse2', 'Customer3'): 35
    }

    # Define the shipment quantities as decision variables
    shipment_quantities = pulp.LpVariable.dicts(
        "Shipment",
        ((w, c) for w in warehouses for c in customers),
        lowBound=0, cat='Continuous'
    )

    # Define the objective function (minimize transportation cost)
    prob += pulp.lpSum([cost[w, c] * shipment_quantities[w, c] for w in warehouses for c in customers]), "Total Cost"

    # Define the supply and demand constraints
    demand = {'Customer1': 100, 'Customer2': 150, 'Customer3': 200}
    supply = {'Warehouse1': 200, 'Warehouse2': 300}

    # Add demand constraints (each customer must receive the right amount)
    for c in customers:
        prob += pulp.lpSum([shipment_quantities[w, c] for w in warehouses]) == demand[c], f"Demand_{c}"

    # Add supply constraints (each warehouse can only supply up to its capacity)
    for w in warehouses:
        prob += pulp.lpSum([shipment_quantities[w, c] for c in customers]) <= supply[w], f"Supply_{w}"

    # Solve the optimization problem
    prob.solve()

    # Get the results (shipment quantities)
    results = {}
    for w in warehouses:
        for c in customers:
            results[(w, c)] = pulp.value(shipment_quantities[w, c])

    return results, prob

# Visualization of the supply chain network
def visualize_supply_chain(shipment_quantities):
    # Create a directed graph to represent the supply chain network
    G = nx.DiGraph()

    # Add nodes (warehouses and customers)
    warehouses = ['Warehouse1', 'Warehouse2']
    customers = ['Customer1', 'Customer2', 'Customer3']
    for warehouse in warehouses:
        G.add_node(warehouse, type='warehouse')
    for customer in customers:
        G.add_node(customer, type='customer')

    # Add edges (shipments) based on the optimal shipment quantities
    for (warehouse, customer), quantity in shipment_quantities.items():
        if quantity > 0:  # Only show edges with non-zero shipment quantities
            G.add_edge(warehouse, customer, weight=quantity)

    # Plotting the network
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)  # Layout for positioning nodes

    # Draw the nodes
    nx.draw_networkx_nodes(G, pos, node_size=2000, node_color='lightblue', alpha=0.8)

    # Draw the edges with labels
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), width=2, edge_color='gray', alpha=0.6)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', font_color='black')

    # Display shipment quantities as edge labels
    edge_labels = {(u, v): f'{d["weight"]} units' for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

    # Title and show plot
    plt.title('Optimal Supply Chain Network')
    plt.axis('off')
    plt.show()

# Sensitivity Analysis Plot (optional)
def sensitivity_analysis_plot(shipment_quantities):
    shipment_quantities_values = list(shipment_quantities.values())
    cost_factor = [1.0, 1.2, 1.5, 1.8, 2.0]  # Hypothetical cost factors for analysis

    # Sensitivity analysis for one route (for simplicity, we’ll pick the first route)
    sensitivity_quantities = [shipment_quantities_values[0] * factor for factor in cost_factor]

    plt.figure(figsize=(8, 6))
    plt.plot(cost_factor, sensitivity_quantities, marker='o', color='b')
    plt.title('Sensitivity Analysis: Shipment Quantity vs. Cost Factor')
    plt.xlabel('Cost Factor')
    plt.ylabel('Shipment Quantity (units)')
    plt.grid(True)
    plt.show()

# Main execution function
def main():
    # Create and solve the optimization model
    shipment_quantities, prob = create_optimization_model()

    # Display results
    print(f"Optimal Objective Value: {pulp.value(prob.objective)}")
    print("Optimal Shipment Quantities:")
    for (w, c), quantity in shipment_quantities.items():
        print(f"Shipment from {w} to {c}: {quantity} units")

    # Visualize the supply chain network
    visualize_supply_chain(shipment_quantities)

    # Optional: Perform sensitivity analysis
    sensitivity_analysis_plot(shipment_quantities)

if __name__ == "__main__":
    main()
