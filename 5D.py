import pandas as pd
import os

# Set file paths (adjust as needed)
base_path = 'C:/Users/Rohsn Chimbaikar/PycharmProjects/Data-Science_Practicals'
billboard_file = os.path.join(base_path, 'Raw_Data/DE_Billboard_Locations.csv')
visitor_file = os.path.join(base_path, 'Raw_Data/Retrieve_Online_Visitor.csv')

# Load the data
billboard_data = pd.read_csv(billboard_file, encoding="latin-1")
visitor_data = pd.read_csv(visitor_file, encoding="latin-1")

# Merge the data based on 'Country' and 'Place_Name'
merged_data = pd.merge(billboard_data, visitor_data, on=["Country", "Place_Name"], how="inner")

# Determine the logic for selecting content
# Example: Pick the top 5 billboards with the highest visitor rate
merged_data['VisitorYearRate'] = (merged_data['Last_IP_Number'] - merged_data['First_IP_Number']) * 365.25 * 24 * 12
selected_billboards = merged_data.nlargest(5, 'VisitorYearRate')

# Example logic: Assign content based on the highest visitor rate
selected_billboards['Content'] = selected_billboards['VisitorYearRate'].apply(lambda x: "High Traffic Content" if x > 10000 else "Standard Content")

# Display the selected billboards and their content
print(selected_billboards[['Country', 'Place_Name', 'VisitorYearRate', 'Content']])

# Optionally: Save this information to a new file or database
selected_billboards.to_csv('Selected_Billboards_Content.csv', index=False)
