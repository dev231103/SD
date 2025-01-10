import pandas as pd
sInputFileName = r"C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Raw_Data\Country_Code.csv"
InputData = pd.read_csv(sInputFileName,encoding='latin-1')
print("---------------------------Raw Data--------------------------------------")
print(InputData)
ProcessData = InputData
ProcessData.drop('ISO-2-CODE',axis=1,inplace=True)
ProcessData.drop('ISO-3-Code',axis=1,inplace=True)
ProcessData.rename(columns={'Country':'Country_Name','ISO-M49':'Country_Number'},inplace=True)
ProcessData.set_index('Country_Number',inplace=True)
ProcessData.sort_values('Country_Name',ascending=False,axis=0,inplace=True)
OutputData = ProcessData
sOutputFileName = r"C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Processed Data\CSVTOHORUS.csv"
print("------------------------------Output Data---------------------------------")
print(OutputData)
OutputData.to_csv(sOutputFileName,index=False)
print("Sucessfully converted CSV to HORUS!")

