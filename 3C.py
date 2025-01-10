import pandas as pd

# Define input and output file paths
InputFileName = 'IP_DATA_CORE.csv'
OutputFileName = 'Retrieve_Router_Location.csv'
Base = r'C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals'

# Print working base information
print('----------------------------------')
print(f'Working Base: {Base}')
print('----------------------------------')

# Define the file path for loading data
sFileName = f"{Base}\\Raw_Data\\{InputFileName}"
print(f'Loading: {sFileName}')

# Load the CSV file with selected columns
IP_DATA_ALL = pd.read_csv(
    sFileName,
    header=0,
    low_memory=False,
    usecols=['Country', 'Place Name', 'Latitude', 'Longitude'],
    encoding="latin-1"
)

# Rename columns for consistency
IP_DATA_ALL.rename(columns={'Place Name': 'Place_Name'}, inplace=True)

# Select relevant columns
AllData = IP_DATA_ALL[['Country', 'Place_Name', 'Latitude']]

# Print all data
print(AllData)

# Calculate mean latitude grouped by Country and Place_Name
MeanData = AllData.groupby(['Country', 'Place_Name'])['Latitude'].mean()

# Print mean data
print(MeanData)

# Save the mean data to a CSV file
output_path = f"{Base}\\Processed Data\\{OutputFileName}"
MeanData.to_csv(output_path, index=True)
print(f'Mean Data saved to: {output_path}')
