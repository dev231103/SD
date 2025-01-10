import networkx as nx
import pandas as pd
from geopy.distance import distance
import os

# Base directory setup
Base = r'C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals'

print('################################')
print('Working Base:', Base)
print('################################')

sOutputFileName = 'Assess-DE-Billboard-Visitor.gml'

# Input CSV Files
billboard_data_file = r"C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Raw_Data\Assess_BillboardData.csv"
visitor_data_file = r"C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Raw_Data\Assess_VisitorData.csv"

# Output directory setup
sFileDir = os.path.join(Base, r'02-Assess\01-EDS\02-Python')
os.makedirs(sFileDir, exist_ok=True)

################################################################
# Load Data from CSV
BillboardData = pd.read_csv(billboard_data_file)
VisitorData = pd.read_csv(visitor_data_file)

# Merging Billboard and Visitor Data
BillboardVisitorData = pd.merge(BillboardData, VisitorData, how='inner', on='Place_Name')

################################################################
# Calculate Distance Using Geopy
def calculate_distance(row):
    return round(distance(
        (row['Latitude_x'], row['Longitude_x']),
        (row['Latitude_y'], row['Longitude_y'])
    ).miles, 4)

BillboardVisitorData['Distance'] = BillboardVisitorData.apply(calculate_distance, axis=1)

################################################################
# Graph Construction
G = nx.Graph()

for i, row in BillboardVisitorData.iterrows():
    # Nodes for Media Hub and Billboard
    sNode0 = 'MediaHub-' + row['Country_x']
    sNode1 = f"B-{row['Latitude_x']}-{row['Longitude_x']}"

    # Adding Billboard Node
    G.add_node(sNode1,
               Nodetype='Billboard',
               Country=row['Country_x'],
               PlaceName=row['Place_Name'],
               Latitude=row['Latitude_x'],
               Longitude=row['Longitude_x'])

    # Nodes for Visitor (Mobile)
    sNode2 = f"M-{row['Latitude_y']}-{row['Longitude_y']}"
    G.add_node(sNode2,
               Nodetype='Mobile',
               Country=row['Country_y'],
               PlaceName=row['Place_Name'],
               Latitude=row['Latitude_y'],
               Longitude=row['Longitude_y'])

    # Adding Edges (Links)
    print(f'Link Media Hub: {sNode0} to Billboard: {sNode1}')
    G.add_edge(sNode0, sNode1)

    print(f'Link Post Code: {sNode1} to GPS: {sNode2}')
    G.add_edge(sNode1, sNode2, distance=row['Distance'])

################################################################
# Output Information
print('################################')
print("Nodes of graph:", nx.number_of_nodes(G))
print("Edges of graph:", nx.number_of_edges(G))
print('################################')

sFileName = os.path.join(sFileDir, sOutputFileName)
print('Storing:', sFileName)
nx.write_gml(G, sFileName)

# Saving as gzipped version
sFileNameGz = sFileName + '.gz'
nx.write_gml(G, sFileNameGz)

################################################################
print('### Done!! ############################################')
