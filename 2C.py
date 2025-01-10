import pandas as pd

sInputFileName = r"C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Raw_Data\Country_Code.json"
InputData = pd.read_json(sInputFileName,orient='index',encoding='latin-1')

print(InputData)

ProcessData = InputData

ProcessData.drop('ISO-2-CODE', axis=1,inplace=True)
ProcessData.drop('ISO-3-Code',axis=1,inplace=True)

ProcessData.rename(columns={'Country':'Country_Name','ISO-M49':'Country_Number'},inplace=True)

ProcessData.set_index('Country_Number',inplace=True)

ProcessData.sort_values('Country_Name',axis=0,ascending=True,inplace=True)
print("--------------------------------------Processed Data ---------------------------------------------")
print(ProcessData)

sOutputFileName = r"C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Processed Data\HORUS-JSONCountry.csv"

OutputData = ProcessData

OutputData.to_csv(sOutputFileName,index=True)