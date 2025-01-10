import pandas as pd
 #Dont Forget to download lxml library -- pip install lxml

sInputFileName = r"C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Raw_Data\Country_Code.xml"

InputData = pd.read_xml(sInputFileName)

print(InputData)

#Manipulate the data
#First create a copy of the data

ProcessData=InputData

ProcessData.drop('ISO-2-CODE',axis=1,inplace=True)
ProcessData.drop('ISO-3-Code',axis=1,inplace=True)

#Now Lets Rename the Columns

ProcessData.rename(columns={'Country':'Country Name', 'ISO-M49':'Country Number'},inplace=True)

ProcessData.set_index('Country Number', inplace=True)

ProcessData.sort_values('Country Name',ascending=True,axis=0,inplace=True)

print("----------------------------------------------")
print(ProcessData)

#Finally save this processed data into a CSV file

sOutputFileName = r"C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Processed Data\XMl2Horus.csv"
OutputData = ProcessData

OutputData.to_csv(sOutputFileName,index=True)

print('XML to Horus Converted Sucessfully......')