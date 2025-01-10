import sys
import os
import pandas as pd
import sqlite3 as sq

Base = 'C:/Users/Rohsn Chimbaikar/PycharmProjects/Data-Science_Practicals'
print('################################')
print('Working Base:', Base, ' using ', sys.platform)
print('################################')

Company = '03-Hillman'
InputDir = '01-Retrieve'
InputFileName1 = 'Retrieve_Product.csv'
InputFileName2 = 'Retrieve_Box.csv'
InputFileName3 = 'Retrieve_Container.csv'
EDSDir = '02-Assess/01-EDS'
OutputDir = EDSDir + '/02-Python'
OutputFileName = 'Assess_Shipping_Containers.csv'

sFileDir = Base + '/' + Company + '/' + EDSDir
os.makedirs(sFileDir, exist_ok=True)

sFileDir = Base + '/' + Company + '/' + OutputDir
os.makedirs(sFileDir, exist_ok=True)

sDataBaseDir = Base + '/' + Company + '/02-Assess/SQLite'
os.makedirs(sDataBaseDir, exist_ok=True)

sDatabaseName = sDataBaseDir + '/hillman.db'
conn = sq.connect(sDatabaseName)

# Load Product Data
sFileName = Base + '/' + Company + '/' + InputDir + '/' + InputFileName1
print('###########')
print('Loading:', sFileName)
ProductRawData = pd.read_csv(sFileName, header=0, low_memory=False, encoding="latin-1")
ProductRawData.drop_duplicates(subset=None, keep='first', inplace=True)
ProductRawData.index.name = 'IDNumber'
ProductData = ProductRawData[ProductRawData.Length <= 0.5].head(10)
print('Loaded Product:', ProductData.columns.values)
print('################################')

# Store Product Data to SQLite
sTable = 'Assess_Product'
print('Storing:', sDatabaseName, ' Table:', sTable)
ProductData.to_sql(sTable, conn, if_exists="replace")

print(ProductData.head())
print('################################')
print('Rows:', ProductData.shape[0])
print('################################')

# Load Box Data
sFileName = Base + '/' + Company + '/' + InputDir + '/' + InputFileName2
print('###########')
print('Loading:', sFileName)
BoxRawData = pd.read_csv(sFileName, header=0, low_memory=False, encoding="latin-1")
BoxRawData.drop_duplicates(subset=None, keep='first', inplace=True)
BoxRawData.index.name = 'IDNumber'
BoxData = BoxRawData[BoxRawData.Length <= 1].head(1000)
print('Loaded Box:', BoxData.columns.values)
print('################################')

# Store Box Data to SQLite
sTable = 'Assess_Box'
print('Storing:', sDatabaseName, ' Table:', sTable)
BoxData.to_sql(sTable, conn, if_exists="replace")

print(BoxData.head())
print('################################')
print('Rows:', BoxData.shape[0])
print('################################')

# Load Container Data
sFileName = Base + '/' + Company + '/' + InputDir + '/' + InputFileName3
print('###########')
print('Loading:', sFileName)
ContainerRawData = pd.read_csv(sFileName, header=0, low_memory=False, encoding="latin-1")
ContainerRawData.drop_duplicates(subset=None, keep='first', inplace=True)
ContainerRawData.index.name = 'IDNumber'
ContainerData = ContainerRawData[ContainerRawData.Length <= 2].head(10)
print('Loaded Container:', ContainerData.columns.values)
print('################################')

# Store Container Data to SQLite
sTable = 'Assess_Container'
print('Storing:', sDatabaseName, ' Table:', sTable)
ContainerData.to_sql(sTable, conn, if_exists="replace")

print(ContainerData.head())
print('################################')
print('Rows:', ContainerData.shape[0])
print('################################')

# Fit Product in Box
print('################')
sView = 'Assess_Product_in_Box'
print('Creating:', sDatabaseName, ' View:', sView)
sSQL = "DROP VIEW IF EXISTS " + sView + ";"
conn.execute(sSQL)

sSQL = "CREATE VIEW " + sView + " AS SELECT P.UnitNumber AS ProductNumber, B.UnitNumber AS BoxNumber,"
sSQL += " (B.Thickness * 1000) AS PackSafeCode, (B.BoxVolume - P.ProductVolume) AS PackFoamVolume,"
sSQL += " ((B.Length*10) * (B.Width*10) * (B.Height*10)) * 167 AS Air_Dimensional_Weight,"
sSQL += " ((B.Length*10) * (B.Width*10) * (B.Height*10)) * 333 AS Road_Dimensional_Weight,"
sSQL += " ((B.Length*10) * (B.Width*10) * (B.Height*10)) * 1000 AS Sea_Dimensional_Weight,"
sSQL += " P.Length AS Product_Length, P.Width AS Product_Width, P.Height AS Product_Height,"
sSQL += " P.ProductVolume AS Product_cm_Volume, ((P.Length*10) * (P.Width*10) * (P.Height*10)) AS Product_ccm_Volume,"
sSQL += " (B.Thickness * 0.95) AS Minimum_Pack_Foam, (B.Thickness * 1.05) AS Maximum_Pack_Foam,"
sSQL += " B.Length - (B.Thickness * 1.10) AS Minimum_Product_Box_Length,"
sSQL += " B.Length - (B.Thickness * 0.95) AS Maximum_Product_Box_Length,"
sSQL += " B.Width - (B.Thickness * 1.10) AS Minimum_Product_Box_Width,"
sSQL += " B.Width - (B.Thickness * 0.95) AS Maximum_Product_Box_Width,"
sSQL += " B.Height - (B.Thickness * 1.10) AS Minimum_Product_Box_Height,"
sSQL += " B.Height - (B.Thickness * 0.95) AS Maximum_Product_Box_Height,"
sSQL += " B.Length AS Box_Length, B.Width AS Box_Width, B.Height AS Box_Height,"
sSQL += " B.BoxVolume AS Box_cm_Volume, ((B.Length*10) * (B.Width*10) * (B.Height*10)) AS Box_ccm_Volume,"
sSQL += " (2 * B.Length * B.Width) + (2 * B.Length * B.Height) + (2 * B.Width * B.Height) AS Box_sqm_Area,"
sSQL += " ((B.Length*10) * (B.Width*10) * (B.Height*10)) *  3.5 AS Box_A_Max_Kg_Weight,"
sSQL += " ((B.Length*10) * (B.Width*10) * (B.Height*10)) *  7.7 AS Box_B_Max_Kg_Weight,"
sSQL += " ((B.Length*10) * (B.Width*10) * (B.Height*10)) * 10.0 AS Box_C_Max_Kg_Weight"
sSQL += " FROM Assess_Product AS P, Assess_Box AS B"
sSQL += " WHERE P.Length >= (B.Length - (B.Thickness * 1.10))"
sSQL += " AND P.Width >= (B.Width - (B.Thickness * 1.10))"
sSQL += " AND P.Height >= (B.Height - (B.Thickness * 1.10))"
sSQL += " AND P.Length <= (B.Length - (B.Thickness * 0.95))"
sSQL += " AND P.Width <= (B.Width - (B.Thickness * 0.95))"
sSQL += " AND P.Height <= (B.Height - (B.Thickness * 0.95))"
sSQL += " AND (B.Height - B.Thickness) >= 0"
sSQL += " AND (B.Width - B.Thickness) >= 0"
sSQL += " AND (B.Height - B.Thickness) >= 0"
sSQL += " AND B.BoxVolume >= P.ProductVolume;"
conn.execute(sSQL)

# Export Data to SQLite Tables (exclude the 'Assess_Box_on_Pallet' table)
sTables = ['Assess_Product_in_Box']  # Only include 'Assess_Product_in_Box'

# Iterate through the tables and process them
for sTable in sTables:
    print('################')
    print('Loading:', sDatabaseName, ' Table:', sTable)

    # Prepare and execute the SQL query
    sSQL = f"SELECT * FROM {sTable};"
    SnapShotData = pd.read_sql_query(sSQL, conn)

    print('################')

    # Create the output table name by appending '_SnapShot' to the table name
    sTableOut = sTable + '_SnapShot'
    print('Storing:', sDatabaseName, ' Table:', sTableOut)

    # Store the data into the new table
    SnapShotData.to_sql(sTableOut, conn, if_exists="replace")

# Save the final snapshot data to a CSV file
OutputFile = sFileDir + '/' + OutputFileName
print('Saving:', OutputFile)
SnapShotData.to_csv(OutputFile, index=False)
