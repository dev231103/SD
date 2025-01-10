import sys
import os
import pandas as pd


Base = r'C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals'

# Input and Output file names
sInputFileName = 'Good-or-Bad.csv'
sOutputFileName = 'Good-or-Bad-01.csv'


# Create the directory for output if it doesn't exist
sFileDir = os.path.join(Base, '02-Assess', '01-EDS', '02-Python')
if not os.path.exists(sFileDir):
    os.makedirs(sFileDir)

# Load the raw data
sFileName = os.path.join(Base, 'Raw_Data', sInputFileName)
print(f'Loading: {sFileName}')
RawData = pd.read_csv(sFileName, header=0)

# Print raw data information
print('## Raw Data Values')
print('################################')
print(RawData)
print('################################')
print('## Data Profile')
print('################################')
print(f'Rows: {RawData.shape[0]}')
print(f'Columns: {RawData.shape[1]}')
print('################################')

# Save the raw data to the output directory
sFileName = os.path.join(sFileDir, sInputFileName)
RawData.to_csv(sFileName, index=False)

# Clean data: Remove columns that are completely empty
TestData = RawData.dropna(axis=1, how='all')

# Print cleaned data information
print('################################')
print('## Test Data Values')
print('################################')
print(TestData)
print('################################')
print('## Data Profile')
print('################################')
print(f'Rows: {TestData.shape[0]}')
print(f'Columns: {TestData.shape[1]}')
print('################################')

# Save the cleaned data
sFileName = os.path.join(sFileDir, sOutputFileName)
TestData.to_csv(sFileName, index=False)

# Final message
print('################################')
print('### Done!! #####################')
print('################################')
