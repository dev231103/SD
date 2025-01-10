import os
import pandas as pd
from geopy.geocoders import Nominatim

# Initialize geolocator
geolocator = Nominatim(user_agent="warehouse_geocoder",timeout=10)


InputFileName = r"C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Raw_Data\Retrieve_GB_Postcode_Warehouse.csv"
OutputDir = r'C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Processed Data'
OutputFileName = 'Assess_GB_Warehouse_Address.csv'

# Load the input file
sFileName = InputFileName
print(f'Loading: {sFileName}')
Warehouse = pd.read_csv(sFileName, header=0, low_memory=False)

# Sort data by postcode
Warehouse.sort_values(by='postcode', ascending=True, inplace=True)

# Limit data to first 5 and last 5 valid rows based on latitude
WarehouseGoodHead = Warehouse[Warehouse.latitude != 0].head(5)
WarehouseGoodTail = Warehouse[Warehouse.latitude != 0].tail(5)

# Function to get address from coordinates
def get_address(row):
    point = f"{row['latitude']},{row['longitude']}"
    return geolocator.reverse(point).address

# Process head and tail data
for df in [WarehouseGoodHead, WarehouseGoodTail]:
    df['Warehouse_Address'] = df.apply(get_address, axis=1)
    df.drop(['id', 'postcode'], axis=1, inplace=True)

# Combine processed data
WarehouseGood = pd.concat([WarehouseGoodHead, WarehouseGoodTail], ignore_index=True)
print(WarehouseGood)

# Save the output
sOutputFileName = os.path.join(OutputDir, OutputFileName)
WarehouseGood.to_csv(sOutputFileName, index=False)
print('### Done!!')
