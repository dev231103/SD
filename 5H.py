# -*- coding: utf-8 -*-
import os
import pandas as pd
import networkx as nx
from geopy.distance import geodesic
import sqlite3 as sql

# Define base directory and file paths
Base = 'C:/Users/Rohsn Chimbaikar/PycharmProjects/Data-Science_Practicals'
Company = '03-Hillman'
InputDir = 'C:/Users/Rohsn Chimbaikar/PycharmProjects/Data-Science_Practicals/Raw_Data'
InputFileName = 'Retrieve_All_Countries.csv'
EDSDir = '02-Assess/01-EDS'
OutputDir = f'{EDSDir}/02-Python'
OutputFileName = 'Assess_Best_Logistics.gml'

# Create necessary directories
for dir_path in [f'{Base}/{Company}/{EDSDir}', f'{Base}/{Company}/{OutputDir}', f'{Base}/{Company}/02-Assess/SQLite']:
    os.makedirs(dir_path, exist_ok=True)

# Define SQLite database
sDatabaseName = f'{Base}/{Company}/02-Assess/SQLite/Hillman.db'
conn = sql.connect(sDatabaseName)

# Load input data
sFileName = f'{InputDir}/{InputFileName}'

print(f'Loading: {sFileName}')
Warehouse = pd.read_csv(sFileName, header=0, low_memory=False, encoding="latin-1")

# Rename columns
Warehouse.rename(columns={
    'X1': 'Country', 'X2': 'PostCode', 'X3': 'PlaceName',
    'X4': 'AreaName', 'X5': 'AreaCode', 'X10': 'Latitude', 'X11': 'Longitude'
}, inplace=True)

# Group data and store in SQLite
groupings = {
    'Assess_RoutePointsCountry': ['Country'],
    'Assess_RoutePointsPostCode': ['Country', 'PostCode'],
    'Assess_RoutePointsPlaceName': ['Country', 'PostCode', 'PlaceName']
}

for table_name, group_by_cols in groupings.items():
    grouped = Warehouse.groupby(group_by_cols)[['Latitude', 'Longitude']].mean()
    grouped.to_sql(table_name, conn, if_exists="replace")

# Create and populate views
views = {
    'Assess_RouteCountries': """
        SELECT DISTINCT
            S.Country AS SourceCountry, S.Latitude AS SourceLatitude, S.Longitude AS SourceLongitude,
            T.Country AS TargetCountry, T.Latitude AS TargetLatitude, T.Longitude AS TargetLongitude
        FROM Assess_RoutePointsCountry AS S, Assess_RoutePointsCountry AS T
        WHERE S.Country <> T.Country 
        AND S.Country IN ('GB', 'DE', 'BE', 'AU', 'US', 'IN')
        AND T.Country IN ('GB', 'DE', 'BE', 'AU', 'US', 'IN');
    """,
    'Assess_RoutePostCode': """
        SELECT DISTINCT
            S.Country AS SourceCountry, S.Latitude AS SourceLatitude, S.Longitude AS SourceLongitude,
            T.Country AS TargetCountry, T.PostCode AS TargetPostCode,
            T.Latitude AS TargetLatitude, T.Longitude AS TargetLongitude
        FROM Assess_RoutePointsCountry AS S, Assess_RoutePointsPostCode AS T
        WHERE S.Country = T.Country 
        AND S.Country IN ('GB', 'DE', 'BE', 'AU', 'US', 'IN');
    """,
    'Assess_RoutePlaceName': """
        SELECT DISTINCT
            S.Country AS SourceCountry, S.PostCode AS SourcePostCode,
            S.Latitude AS SourceLatitude, S.Longitude AS SourceLongitude,
            T.Country AS TargetCountry, T.PostCode AS TargetPostCode,
            T.PlaceName AS TargetPlaceName, T.Latitude AS TargetLatitude,
            T.Longitude AS TargetLongitude
        FROM Assess_RoutePointsPostCode AS S, Assess_RoutePointsPlaceName AS T
        WHERE S.Country = T.Country AND S.PostCode = T.PostCode
        AND S.Country IN ('GB', 'DE', 'BE', 'AU', 'US', 'IN');
    """
}

# Create and populate views
for view_name, sql_query in views.items():
    conn.execute(f"DROP VIEW IF EXISTS {view_name};")
    conn.execute(f"CREATE VIEW {view_name} AS {sql_query}")


# Calculate distances and store in graph
G = nx.Graph()


def process_view(view_name, source_prefix, target_prefix, additional_columns=[]):
    sSQL = f"SELECT * FROM {view_name};"
    data = pd.read_sql_query(sSQL, conn)

    data['Distance'] = data.apply(
        lambda row: round(geodesic((row['SourceLatitude'], row['SourceLongitude']),
                                   (row['TargetLatitude'], row['TargetLongitude'])).miles, 4),
        axis=1
    )

    for i, row in data.iterrows():
        source = f"{source_prefix}-{row['SourceCountry']}" if 'SourcePostCode' not in row else f"{source_prefix}-{row['SourcePostCode']}-{row['SourceCountry']}"
        target = f"{target_prefix}-{row['TargetCountry']}" if 'TargetPostCode' not in row else f"{target_prefix}-{row['TargetPostCode']}-{row['TargetCountry']}"

        G.add_node(source,
                   **{col: row[col] for col in ['SourceCountry', 'Latitude', 'Longitude'] + additional_columns if
                      col in row})
        G.add_node(target,
                   **{col: row[col] for col in ['TargetCountry', 'Latitude', 'Longitude'] + additional_columns if
                      col in row})
        G.add_edge(source, target, distance=row['Distance'])


process_view('Assess_RouteCountries', 'C', 'C')
process_view('Assess_RoutePostCode', 'C', 'P', ['PostCode'])
process_view('Assess_RoutePlaceName', 'P', 'L', ['PostCode', 'PlaceName'])

# Save graph
sOutputPath = f'{Base}/{Company}/{OutputDir}/{OutputFileName}'
nx.write_gml(G, sOutputPath)
nx.write_gml(G, sOutputPath + '.gz')

# Display some results
print('################################')
print('Shortest path:', nx.shortest_path(G, source='P-SW1-GB', target='P-01001-US', weight='distance'))
print('Path length:', nx.shortest_path_length(G, source='P-SW1-GB', target='P-01001-US', weight='distance'))
print('Routes < 2 from P-SW1-GB:', nx.single_source_shortest_path(G, source='P-SW1-GB', cutoff=1))

# Clean up database
conn.execute("VACUUM;")


print('### Done!!')
