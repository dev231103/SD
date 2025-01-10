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


sDataWarehousePath = r"C:\Users\Rohsn Chimbaikar\Downloads\datawarehouse.db"
conn1 = sq.connect(sDataWarehousePath)

sDataMartPath = os.path.join(sDataWarehouseDir, 'datamart.db')
conn2 = sq.connect(sDataMartPath)

print('################')
sTable = 'Dim-BMI'
print('Loading :', sDataWarehousePath, ' Table:', sTable)
sSQL = "SELECT * FROM [Dim-BMI];"
PersonFrame0 = pd.read_sql_query(sSQL, conn1)

print('################################')
sTable = 'Dim-BMI'
print('Loading :', sDataWarehousePath, ' Table:', sTable)
print('################################')
sSQL = """
SELECT 
    PersonID,
    Height,
    Weight,
    bmi,
    Indicator
FROM [Dim-BMI]
WHERE 
    Height > 1.5 
    AND Indicator = 1
ORDER BY  
    Height,
    Weight;
"""
PersonFrame1 = pd.read_sql_query(sSQL, conn1)

DimPerson = PersonFrame1
DimPersonIndex = DimPerson.set_index(['PersonID'], inplace=False)

sTable = 'Dim-BMI-Horizontal'
print('\n#################################')
print('Storing :', sDataMartPath, '\n Table:', sTable)
print('\n#################################')
DimPersonIndex.to_sql(sTable, conn2, if_exists="replace")

# Reload and display data
print('################################')
sTable = 'Dim-BMI-Horizontal'
print('Loading :', sDataMartPath, ' Table:', sTable)
print('################################')
sSQL = "SELECT * FROM [Dim-BMI-Horizontal];"
PersonFrame2 = pd.read_sql_query(sSQL, conn2)

# Print dataset information
print('################################')
print('Full Data Set (Rows):', PersonFrame0.shape[0])
print('Full Data Set (Columns):', PersonFrame0.shape[1])
print('################################')
print('Horizontal Data Set (Rows):', PersonFrame2.shape[0])
print('Horizontal Data Set (Columns):', PersonFrame2.shape[1])
print('################################')
