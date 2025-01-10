import os
import pandas as pd

# Define the input and output file paths directly
sFileName = r"C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Raw_Data\IP_DATA_ALL.csv"
print('Loading:', sFileName)

# Define the output file path directly
sFileName2 = r'C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Processed Data\Retrieve_IP_DATA.csv'

# Load the CSV file
try:
    IP_DATA_ALL = pd.read_csv(sFileName, encoding="latin-1",low_memory=False)
    print(f'Rows: {IP_DATA_ALL.shape[0]}')
    print(f'Columns: {IP_DATA_ALL.shape[1]}')
except FileNotFoundError:
    print(f"Error: File not found at {sFileName}")
    exit()

# Display column details for the raw dataset
print('### Raw Data Set #####################################')
for col in IP_DATA_ALL.columns:
    print(col, type(col))

# Fix column names: Replace spaces with dots and strip extra spaces
print('### Fixed Data Set ###################################')
IP_DATA_ALL_FIX = IP_DATA_ALL.copy()
IP_DATA_ALL_FIX.columns = [col.strip().replace(" ", ".") for col in IP_DATA_ALL_FIX.columns]
for col in IP_DATA_ALL_FIX.columns:
    print(col, type(col))

# Add RowID as an index
print('Fixed Data Set with ID')
IP_DATA_ALL_with_ID = IP_DATA_ALL_FIX.copy()
IP_DATA_ALL_with_ID.index.names = ['RowID']

# Save the fixed dataset with RowID to a new file
IP_DATA_ALL_with_ID.to_csv(sFileName2, index=True, encoding="latin-1")
print(f'Saved fixed dataset to: {sFileName2}')

print('-----------------------Done!! -------------------------------')
