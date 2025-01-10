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

print('################################')
print('## Raw Data Values')
print('################################')
print(RawData)
print('################################')
print('## Data Profile')
print('################################')
print('Rows:', RawData.shape[0])
print('Columns:', RawData.shape[1])
print('################################')

# Save the raw data to the output directory
sFileName = sFileDir + '/' + sInputFileName
RawData.to_csv(sFileName, index=False)

# Clean data by dropping columns with fewer than 2 non-NA values
TestData = RawData.dropna(thresh=2)

print('################################')
print('## Test Data Values')
print('################################')
print(TestData)
print('################################')
print('## Data Profile')
print('################################')
print('Rows:', TestData.shape[0])
print('Columns:', TestData.shape[1])
print('################################')

# Save the cleaned test data
sFileName = sFileDir + '/' + sOutputFileName
TestData.to_csv(sFileName, index=False)

print('################################')
print('### Done!! #####################')
print('################################')
