import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

def visualize_antimagic_labeling(labeling, figsize=(12, 10), node_size=80, save_path=None, dpi=300):
    """
    Visualize antimagic labeling in the style of the provided figures.
    
    Parameters:
    - labeling: dictionary returned by solve_kn_antimagic
    - figsize: tuple for figure size
    - node_size: size of vertex nodes
    - save_path: path to save PNG file (e.g., 'k8_antimagic.png'). If None, doesn't save
    - dpi: resolution for saved image (default: 300)
    """
    if labeling is None:
        print("No labeling to visualize.")
        return
    
    n = labeling["n"]
    edges = labeling["edges"]
    labels = labeling["labels"]
    a = labeling["a"]
    
    # Create graph
    G = nx.Graph()
    G.add_nodes_from(range(n))
    G.add_edges_from(edges)
    
    # Calculate vertex sums
    vertex_sums = {}
    for v in range(n):
        total = 0
        for edge, label in labels.items():
            if v in edge:
                total += label
        vertex_sums[v] = total
    
    # Create circular layout
    pos = nx.circular_layout(G)
    
    # Create figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # Draw edges with labels
    nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.6, ax=ax, edge_color='black')
    
    # Draw edge labels (in black)
    edge_labels = {edge: label for edge, label in labels.items()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=10, 
                                  font_color='black', ax=ax)
    
    # Draw nodes (vertices) in blue
    nx.draw_networkx_nodes(G, pos, node_color='blue', 
                           node_size=node_size, ax=ax)
    
    # Draw vertex labels and sums
    # Vertex indices in blue on the left side
    for node, (x, y) in pos.items():
        # Calculate offset for labels (outside the circle)
        angle = np.arctan2(y, x)
        offset = 0.15
        x_offset = x + offset * np.cos(angle)
        y_offset = y + offset * np.sin(angle)
        
        # Draw vertex index in blue
        ax.text(x_offset, y_offset, str(node), 
                fontsize=12, color='blue', fontweight='bold',
                ha='center', va='center')
        
        # Draw vertex sum in red (further outside)
        sum_offset = 0.25
        x_sum = x + sum_offset * np.cos(angle)
        y_sum = y + sum_offset * np.sin(angle)
        ax.text(x_sum, y_sum, str(vertex_sums[node]), 
                fontsize=14, color='red', fontweight='bold',
                ha='center', va='center')
    
    # Set title with more padding
    ax.set_title(f'Antimagic labeling of K_{n} (a={a}, d=1)', 
                 fontsize=16, fontweight='bold', pad=40)
    
    # Remove axes
    ax.axis('off')
    ax.set_aspect('equal')
    
    plt.tight_layout()
    
    # Save figure if path is provided
    if save_path:
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight', facecolor='white')
        print(f"\nFigure saved to: {save_path}")
    
    plt.show()
    
    # Print verification
    print(f"\nVerification for K_{n}:")
    print(f"Parameter a = {a}")
    print(f"\nVertex sums (should be consecutive integers starting from {a}):")
    for v in range(n):
        expected = a + v
        actual = vertex_sums[v]
        status = "✓" if actual == expected else "✗"
        print(f"  v{v}: {actual} (expected {expected}) {status}")


# Example usage - uncomment the one you want to visualize:

# For K_8:
result8 = solve_kn_antimagic(8, time_limit_seconds=60, verbose=False)
if result8:
    visualize_antimagic_labeling(result8, save_path='k8_antimagic.png')

# For K_12:
result12 = solve_kn_antimagic(12, time_limit_seconds=600, verbose=False)
if result12:
    visualize_antimagic_labeling(result12, save_path='k12_antimagic.png')

# For K_16:
result16 = solve_kn_antimagic(16, time_limit_seconds=1800, verbose=False)
if result16:
    visualize_antimagic_labeling(result16, save_path='k16_antimagic.png')
