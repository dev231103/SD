import pandas as pd
import numpy as np
from geopy.distance import geodesic

# Load shop and warehouse data
shops_file = r"C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Raw_Data\GB_Postcodes_Shops.csv"
warehouse_file = r"C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Raw_Data\Retrieve_GB_Postcode_Warehouse.csv"

shops_data = pd.read_csv(shops_file)
warehouse_data = pd.read_csv(warehouse_file)

# Check for duplicates and null values
print(f"Shops Data Duplicates: {shops_data.duplicated(subset=['latitude', 'longitude']).sum()}")
print(f"Warehouses Data Duplicates: {warehouse_data.duplicated(subset=['latitude', 'longitude']).sum()}")
print(f"Null Values in Shops Data: {shops_data.isnull().sum()}")
print(f"Null Values in Warehouses Data: {warehouse_data.isnull().sum()}")

def calculate_nearest_warehouse(shop, warehouses):
    """Calculate the nearest warehouse to a shop."""
    shop_location = (shop['latitude'], shop['longitude'])
    distances = warehouses.apply(
        lambda warehouse: geodesic(shop_location, (warehouse['latitude'], warehouse['longitude'])).kilometers,
        axis=1
    )
    # Debug: Print distances for each shop
    print(f"Distances for Shop {shop['postcode']}: {distances.values}")
    nearest_index = distances.idxmin()
    return warehouses.loc[nearest_index, 'postcode'], distances[nearest_index]

# Assign nearest warehouse to each shop
route = []

for _, shop in shops_data.iterrows():
    nearest_warehouse, distance = calculate_nearest_warehouse(shop, warehouse_data)
    route.append({
        'shop_id': shop['id'],
        'shop_postcode': shop['postcode'],
        'warehouse_postcode': nearest_warehouse,
        'distance_km': distance
    })

# Convert route to DataFrame
route_df = pd.DataFrame(route)

# Save the delivery route to a CSV file
output_file = 'delivery_route.csv'
route_df.to_csv(output_file, index=False)

print(f"Delivery route calculated and saved to {output_file}.")
