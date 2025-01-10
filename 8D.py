import os
import pandas as pd
import sqlite3 as sq

# Define the base directory
Base = r'C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals'
print('################################')
print('Working Base :', Base)
print('################################')


Company = '01-Vermeulen'
# Define the Data Warehouse directory and ensure it exists
sDataWarehouseDir = os.path.join(Base, '99-DW')
if not os.path.exists(sDataWarehouseDir):
    os.makedirs(sDataWarehouseDir)

# Connect to the Data Warehouse database
sDatabaseWarehouse =  r"C:\Users\Rohsn Chimbaikar\Downloads\datawarehouse.db"
conn1 = sq.connect(sDatabaseWarehouse)

# Connect to the Data Mart database
sDatabaseMart = os.path.join(sDataWarehouseDir, 'datamart.db')
conn2 = sq.connect(sDatabaseMart)

# Load the full dataset from the Data Warehouse
sTable = 'Dim-BMI'
print(f'Loading from: {sDatabaseWarehouse}, Table: {sTable}')
sSQL = "SELECT * FROM [Dim-BMI];"
PersonFrame0 = pd.read_sql_query(sSQL, conn1)

# Filter and transform the dataset
print(f'Filtering and Transforming Data from: {sDatabaseWarehouse}, Table: {sTable}')
sSQL = """ 
SELECT  
    Height, 
    Weight, 
    Indicator, 
    CASE  
        WHEN Indicator = 1 THEN 'Pip' 
        WHEN Indicator = 2 THEN 'Norman' 
        WHEN Indicator = 3 THEN 'Grant'
        ELSE 'Sam' 
    END AS Name 
FROM  
    [Dim-BMI] 
WHERE  
    Indicator > 2 
ORDER BY  
    Height, 
    Weight; 
"""
PersonFrame1 = pd.read_sql_query(sSQL, conn1)

# Set the index for the transformed dataset
DimPerson = PersonFrame1
DimPersonIndex = DimPerson.set_index(['Indicator'], inplace=False)

# Store the transformed dataset into the Data Mart
sTableSecure = 'Dim-BMI-Secure'
print(f'Storing to: {sDatabaseMart}, Table: {sTableSecure}')
DimPersonIndex.to_sql(sTableSecure, conn2, if_exists="replace")

# Load the filtered dataset for entries with Name = 'Sam'
print(f'Loading from: {sDatabaseMart}, Table: {sTableSecure}')
sSQL = "SELECT * FROM [Dim-BMI-Secure] WHERE Name = 'Sam';"
PersonFrame2 = pd.read_sql_query(sSQL, conn2)

# Print dataset information
print('Full Data Set (Rows):', PersonFrame0.shape[0])
print('Full Data Set (Columns):', PersonFrame0.shape[1])
print('Filtered Data Set (Rows):', PersonFrame2.shape[0])
print('Filtered Data Set (Columns):', PersonFrame2.shape[1])
# Display filtered data for Name = 'Sam'
print('Only Same Data:')
print(PersonFrame2.head())
print("Execution Completed - Secure Vault Style")
