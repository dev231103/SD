import pandas as pd

# Define input and output file names and base directory
InputFileName = 'IP_DATA_CORE.csv'
OutputFileName = 'Retrieve_Router_Location.csv'
Base = r'C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals'

# Print working base directory
print('--------------------------------------------')
print(f'Working Base: {Base}')
print('--------------------------------------------')

# File path for input data
sFileName = f"{Base}\\Raw_Data\\{InputFileName}"
print(f'Loading: {sFileName}')

# Load the dataset
IP_DATA_ALL = pd.read_csv(
    sFileName,header=0,low_memory=False,
    usecols=['Country', 'Place Name', 'Latitude', 'Longitude'],
    encoding="latin-1"
)

# Rename columns for consistency
IP_DATA_ALL.rename(columns={'Place Name': 'Place_Name'}, inplace=True)

# Filter rows where Place_Name is 'London'
LondonData = IP_DATA_ALL.loc[IP_DATA_ALL['Place_Name'] == 'London']

# Select relevant columns
AllData = LondonData[['Country', 'Place_Name', 'Latitude']]

print('All Data:')
print(AllData)

# Calculate mean and standard deviation for Latitude, grouped by Country and Place_Name
MeanData = AllData.groupby(['Country', 'Place_Name'])['Latitude'].mean()
StdData = AllData.groupby(['Country', 'Place_Name'])['Latitude'].std()

# Define bounds for outliers
UpperBound = MeanData + StdData
LowerBound = MeanData - StdData

print('Upper Bound:')
print(UpperBound)

# Identify high outliers
Outliers_Higher = AllData[AllData['Latitude'] > UpperBound.loc[AllData.set_index(['Country', 'Place_Name']).index].values]
print('Higher Outliers:')
print(Outliers_Higher)

print('Lower Bound:')
print(LowerBound)

# Identify low outliers
Outliers_Lower = AllData[AllData['Latitude'] < LowerBound.loc[AllData.set_index(['Country', 'Place_Name']).index].values]
print('Lower Outliers:')
print(Outliers_Lower)

# Identify non-outliers
NonOutliers = AllData[
    (AllData['Latitude'] >= LowerBound.loc[AllData.set_index(['Country', 'Place_Name']).index].values) &
    (AllData['Latitude'] <= UpperBound.loc[AllData.set_index(['Country', 'Place_Name']).index].values)
]
print('Non-Outliers:')
print(NonOutliers)

output_path = f"{Base}\\Processed Data\\{OutputFileName}"
NonOutliers.to_csv(output_path, index=True)
print(f'Non Outliers saved to: {output_path}')

