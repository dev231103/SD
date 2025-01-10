import pandas as pd
import sqlite3 as sq

InputFileName = r"C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Raw_Data\utility.db"

conn = sq.connect(InputFileName)  #establish a connection with the database
InputTable = 'Country_Code' #Specify the table you want to import
query = 'select * from ' + InputTable +";" #write the query you want to execute
InputData = pd.read_sql_query(query,conn)  #Use the pandas read_sql_query method to convert the SQL file into Pandas Data Frame

print(InputData)

#Create a copy of original data
ProcessData = InputData

ProcessData.drop('ISO-2-CODE',axis=1,inplace=True)
ProcessData.drop('ISO-3-Code',axis=1,inplace=True)
ProcessData.drop('index',axis=1,inplace=True)

ProcessData.rename(columns={'Country':'Country Name','ISO-M49':'Country Number'},inplace=True)

ProcessData.set_index('Country Number',inplace=True)

ProcessData.sort_values('Country Name',axis=0,ascending=True,inplace=True)

print("-------------Processed Data------------------")
print(ProcessData)


#finally save the data into a CSV file

OutputFile = ProcessData
sOutputFileName = r"C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Processed Data\MYSQLtoHORUS.csv"

OutputFile.to_csv(sOutputFileName,index=True)
print("Mysql to HORUS conversion successful")