import sys
import os
import pandas as pd
import sqlite3 as sq

Base = r'C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals'
print('################################')
print('Working Base :', Base)
print('################################')


Company = '01-Vermeulen'

sDataWarehouseDir = os.path.join(Base, '99-DW')
if not os.path.exists(sDataWarehouseDir):
    os.makedirs(sDataWarehouseDir)

# Connect to the Data Warehouse database
sDatabaseWarehouse = r"C:\Users\Rohsn Chimbaikar\Downloads\datawarehouse.db"
conn1 = sq.connect(sDatabaseWarehouse)

# Connect to the Data Mart database
sDatabaseMart = os.path.join(sDataWarehouseDir,
                             'datamart.db')
conn2 = sq.connect(sDatabaseMart)

# Define table name
sTable = 'Dim-BMI'

# Load the full dataset from the Data Warehouse
print('Loading from:', sDatabaseWarehouse, 'Table:', sTable)
sSQL = "SELECT * FROM [Dim-BMI];"
PersonFrame0 = pd.read_sql_query(sSQL, conn1)

# Filter and load specific columns from the Data Warehouse
print('Loading filtered data...')
sSQL = """ 
SELECT  
    Height, 
    Weight, 
    Indicator 
FROM  
    [Dim-BMI]; 
"""
PersonFrame1 = pd.read_sql_query(sSQL, conn1)

# Set the index for the filtered dataset
DimPerson = PersonFrame1
DimPersonIndex = DimPerson.set_index(['Indicator'],
                                     inplace=False)

# Define new table name for Data Mart
sTable = 'Dim-BMI-Vertical'

# Store the indexed data into the Data Mart
print('Storing to:', sDatabaseMart, '\nTable:', sTable)
DimPersonIndex.to_sql(sTable, conn2, if_exists="replace")

# Load the stored dataset from the Data Mart
print('Loading from:', sDatabaseMart, 'Table:', sTable)
sSQL = "SELECT * FROM [Dim-BMI-Vertical];"
PersonFrame2 = pd.read_sql_query(sSQL, conn2)

# Print dataset information
print('Full Data Set (Rows):', PersonFrame0.shape[0])
print('Full Data Set (Columns):', PersonFrame0.shape[1])
print('Vertical Data Set (Rows):', PersonFrame2.shape[0])
print('Vertical Data Set (Columns):', PersonFrame2.shape[1])
print("Execution Completed - Vertical Style")