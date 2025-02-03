import os
import pandas as pd
from folium.plugins import FastMarkerCluster, HeatMap
from folium import Marker, Map
import webbrowser

# Define base directory (Windows only)
Base = r'C:\VKHCG'
print(f'Working Base: {Base}')

# Load the CSV file
sFileName = os.path.join(Base, '02-Krennwallner', '01-Retrieve', '01-EDS', '02-Python', 'Retrieve_DE_Billboard_Locations.csv')
df = pd.read_csv(sFileName, header=0, low_memory=False, encoding="latin-1")
df.fillna(value=0, inplace=True)

print(f'Data Shape: {df.shape}')

# Initialize lists for clustering and mapping
DataCluster = []
DataPoint = []

# Iterate over rows
for _, row in df.iterrows():
    try:
        sLongitude = float(row["Longitude"])
        sLatitude = float(row["Latitude"])
        sDescription = f"{row['Place_Name']} ({row['Country']})"
    except Exception:
        sLongitude, sLatitude, sDescription = 0.0, 0.0, 'VKHCG'

    # Append data if coordinates are valid
    if sLongitude != 0.0 and sLatitude != 0.0:
        DataCluster.append([sLatitude, sLongitude])
        DataPoint.append([sLatitude, sLongitude, sDescription])

# Convert DataPoint to DataFrame
pins = pd.DataFrame(DataPoint, columns=['Latitude', 'Longitude', 'Description'])

# Base map location (centered around Germany)
base_location = [48.1459806, 11.4985484]

# 1️⃣ **Map with FastMarkerCluster**
stops_map1 = Map(location=base_location, zoom_start=5)
FastMarkerCluster(DataCluster).add_to(stops_map1)

sFileNameHtml = os.path.join(Base, '02-Krennwallner', '06-Report', '01-EDS', '02-Python', 'Billboard1.html')
stops_map1.save(sFileNameHtml)
webbrowser.open('file://' + os.path.realpath(sFileNameHtml))

# 2️⃣ **Map with Individual Markers**
stops_map2 = Map(location=base_location, zoom_start=5)
for _, row in pins.iloc[:100].iterrows():
    Marker([row["Latitude"], row["Longitude"]], popup=row["Description"]).add_to(stops_map2)

sFileNameHtml = os.path.join(Base, '02-Krennwallner', '06-Report', '01-EDS', '02-Python', 'Billboard2.html')
stops_map2.save(sFileNameHtml)
webbrowser.open('file://' + os.path.realpath(sFileNameHtml))

# 3️⃣ **Heatmap Visualization**
stops_heatmap = Map(location=base_location, zoom_start=5)
stops_heatmap.add_child(HeatMap([[row["Latitude"], row["Longitude"]] for _, row in pins.iloc[:100].iterrows()]))

sFileNameHtml = os.path.join(Base, '02-Krennwallner', '06-Report', '01-EDS', '02-Python', 'Billboard_heatmap.html')
stops_heatmap.save(sFileNameHtml)
webbrowser.open('file://' + os.path.realpath(sFileNameHtml))

print('Execution Done!')
