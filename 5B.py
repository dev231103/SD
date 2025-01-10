import networkx as nx
import matplotlib.pyplot as plt
import os
import pandas as pd


Base = 'C:/Users/Rohsn Chimbaikar/PycharmProjects/Data-Science_Practicals'

print('################################')
print('Working Base:', Base)
print('################################')

# Input and Output file names
sFileName = r"C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Raw_Data\Retrieve_Router_Location.csv"
sOutputFileName1 = 'Assess-DAG-Company-Country.png'
sOutputFileName2 = 'Assess-DAG-Company-Country-Place.png'

# Load Data
print('################################')
print('Loading:', sFileName)
print('################################')

try:
    CompanyData = pd.read_csv(sFileName, header=0, low_memory=False, encoding="latin-1")
    print('Loaded Data:', CompanyData.columns.values)
    print('################################')

    # Display data info
    print(CompanyData)
    print('################################')
    print('Rows:', CompanyData.shape[0])
    print('################################')

except FileNotFoundError:
    print(f"Error: File not found at {sFileName}")
    exit()

# Create two directed graphs
G1 = nx.DiGraph()
G2 = nx.DiGraph()

# Add nodes to the graphs
for i in range(CompanyData.shape[0]):
    G1.add_node(CompanyData['Country'][i])
    sPlaceName = CompanyData['Place_Name'][i] + '-' + CompanyData['Country'][i]
    G2.add_node(sPlaceName)

# Add edges to G1 (connections between countries)
print('################################')
for n1 in G1.nodes():
    for n2 in G1.nodes():
        if n1 != n2:
            print('Link:', n1, 'to', n2)
            G1.add_edge(n1, n2)
print('################################')

# Display the graph information for G1
print('################################')
print("Nodes of G1 graph:", G1.nodes())
print("Edges of G1 graph:", G1.edges())
print('################################')

# Create output directory if it doesn't exist
sFileDir = Base + '/02-Assess/01-EDS/02-Python'
if not os.path.exists(sFileDir):
    os.makedirs(sFileDir)

# Save the G1 graph as an image
sFileName = sFileDir + '/' + sOutputFileName1
print('################################')
print('Storing:', sFileName)
print('################################')

# Visualize and save the first graph (G1) with a spectral layout
nx.draw(G1, pos=nx.spectral_layout(G1), node_color='r', edge_color='g',
        with_labels=True, node_size=8000, font_size=12)
plt.savefig(sFileName)  # Save as PNG
plt.show()  # Display the graph

# Add edges to G2 (connections between places and countries)
print('################################')
for n1 in G2.nodes():
    for n2 in G2.nodes():
        if n1 != n2:
            print('Link:', n1, 'to', n2)
            G2.add_edge(n1, n2)
print('################################')

# Display the graph information for G2
print('################################')
print("Nodes of G2 graph:", G2.nodes())
print("Edges of G2 graph:", G2.edges())
print('################################')

# Save the G2 graph as an image
sFileName = sFileDir + '/' + sOutputFileName2
print('################################')
print('Storing:', sFileName)
print('################################')

# Visualize and save the second graph (G2) with a spectral layout
nx.draw(G2, pos=nx.spectral_layout(G2), node_color='r', edge_color='b',
        with_labels=True, node_size=8000, font_size=12)
plt.savefig(sFileName)  # Save as PNG
plt.show()  # Display the graph

print('################################')
print('Process completed successfully!')
print('################################')
