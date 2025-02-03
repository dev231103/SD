import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Define base directory (Windows path only)

# Input and output file paths
sInputFileName = r"C:\Users\Rohsn Chimbaikar\Downloads\Assess-Network-Routing-Customer.csv"
sOutputFileName1 = 'processedata/Report-Network-Routing-Customer.gml'
sOutputFileName2 = 'processedata/Report-Network-Routing-Customer.png'

# Full input file path


# Load customer data
CustomerData = pd.read_csv(sInputFileName, header=0, low_memory=False, encoding="latin-1").head(100)
print(f'Loaded Data Columns: {CustomerData.columns.values}')
print(f'Data Shape: {CustomerData.shape}')

# Create a graph
G = nx.Graph()

# Add edges between different countries
for i in range(CustomerData.shape[0]):
    for j in range(i + 1, CustomerData.shape[0]):  # Avoid duplicate edges
        Node0 = CustomerData.at[i, 'Customer_Country_Name']
        Node1 = CustomerData.at[j, 'Customer_Country_Name']
        if Node0 != Node1:
            G.add_edge(Node0, Node1)

# Add edges between Country-Place and Place-Coordinates
for i in range(CustomerData.shape[0]):
    Country = CustomerData.at[i, 'Customer_Country_Name']
    Place = CustomerData.at[i, 'Customer_Place_Name'] + f' ({Country})'
    Coordinates = f'({CustomerData.at[i, "Customer_Latitude"]:.6f}, {CustomerData.at[i, "Customer_Longitude"]:.6f})'

    G.add_edge(Country, Place)
    G.add_edge(Place, Coordinates)

# Print graph details
print(f'Graph Nodes: {G.number_of_nodes()}')
print(f'Graph Edges: {G.number_of_edges()}')

# Save the graph in GML format
sFileName = os.path.join(sOutputFileName1)
nx.write_gml(G, sFileName)
print(f'Stored GML File: {sFileName}')

# Save the graph visualization as a PNG file
sFileName = os.path.join(sOutputFileName2)

plt.figure(figsize=(20, 20))
pos = nx.spectral_layout(G)
nx.draw(G, pos, node_color='black', node_size=10, edge_color='red', alpha=0.6, with_labels=True, font_size=10, font_color='blue')

plt.axis('off')
plt.savefig(sFileName, dpi=600)
print(f'Stored Graph Image: {sFileName}')

plt.show()
print('Execution Done!')
