
import sys
import os
import pandas as pd
import sqlite3 as sq


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
sDatabaseWarehouse = r"C:\Users\Rohsn Chimbaikar\Downloads\datawarehouse.db"
conn1 = sq.connect(sDatabaseWarehouse)

# Connect to the Data Mart database
sDatabaseMart = os.path.join(sDataWarehouseDir, 'datamart.db')
conn2 = sq.connect(sDatabaseMart)

# Load the full dataset from the Data Warehouse
sTable = 'Dim-BMI'
print(f'Loading from: {sDatabaseWarehouse}, Table: {sTable}')
sSQL = "SELECT * FROM [Dim-BMI];"
PersonFrame0 = pd.read_sql_query(sSQL, conn1)

# Filter and load specific rows where Indicator > 2
print(f'Filtering and Loading Data from: {sDatabaseWarehouse}, Table: {sTable}')
sSQL = """ 
SELECT  
    Height, 
    Weight, 
    Indicator 
FROM  
    [Dim-BMI] 
WHERE  
    Indicator > 2 
ORDER BY  
    Height, 
    Weight; 
"""
PersonFrame1 = pd.read_sql_query(sSQL, conn1)

# Set index for the filtered data
DimPerson = PersonFrame1
DimPersonIndex = DimPerson.set_index(['Indicator'], inplace=False)

# Store the filtered data into the Data Mart database under a new table
sTableVertical = 'Dim-BMI-Vertical'
print(f'Storing to: {sDatabaseMart}, Table: {sTableVertical}')
DimPersonIndex.to_sql(sTableVertical, conn2, if_exists="replace")

# Load the stored dataset from the Data Mart
print(f'Loading from: {sDatabaseMart}, Table: {sTableVertical}')
sSQL = f"SELECT * FROM [{sTableVertical}];"
PersonFrame2 = pd.read_sql_query(sSQL, conn2)

# Print dataset information
print('Full Data Set (Rows):', PersonFrame0.shape[0])
print('Full Data Set (Columns):', PersonFrame0.shape[1])
print('Filtered Data Set (Rows):', PersonFrame2.shape[0])
print('Filtered Data Set (Columns):', PersonFrame2.shape[1])
print("Execution Completed - Island Style")
