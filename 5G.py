import os
import pandas as pd


InputFileName = r"C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Raw_Data\Retrieve_All_Countries.csv"
OutputDir = r'C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Processed Data'
OutputFileName = 'Assess_All_Warehouse.csv'


sFileName = InputFileName
print(f'Loading: {sFileName}')
Warehouse = pd.read_csv(sFileName, header=0, low_memory=False, encoding="latin-1")

# Rename columns
sColumns = {
    'X1': 'Country',
    'X2': 'PostCode',
    'X3': 'PlaceName',
    'X4': 'AreaName',
    'X5': 'AreaCode',
    'X10': 'Latitude',
    'X11': 'Longitude'
}
Warehouse.rename(columns=sColumns, inplace=True)

# Save the updated data
sOutputFileName = os.path.join(OutputDir, OutputFileName)
Warehouse.to_csv(sOutputFileName, index=False)

print('### Done!!')
