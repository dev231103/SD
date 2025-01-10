import imageio.v2 as imageio
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

sInputFileName = r"C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Raw_Data\Angus.jpg"
InputData = imageio.imread(sInputFileName)

print('Input Data Values ===================================')
print('X: ', InputData.shape[0])
print('Y: ', InputData.shape[1])
print('RGBA: ', InputData.shape[2])
print('=====================================================')

ProcessRawData = InputData.flatten()
y = InputData.shape[2] + 2
x = int(ProcessRawData.shape[0] / y)
ProcessData = pd.DataFrame(np.reshape(ProcessRawData, (x, y)))
sColumns = ['XAxis', 'YAxis', 'Red', 'Green', 'Blue']
ProcessData.columns = sColumns
ProcessData.index.names = ['ID']
print('Rows: ', ProcessData.shape[0])
print('Columns: ', ProcessData.shape[1])
print('=====================================================')
print('Process Data Values =================================')
print('=====================================================')
plt.imshow(InputData)
plt.show()
print('=====================================================')

OutputData = ProcessData
print('Storing File')
sOutputFileName = r'C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Processed Data\HORUS-Picture.csv'
OutputData.to_csv(sOutputFileName, index=False)
print('=====================================================')
print('Picture to HORUS - Done')
print('=====================================================')
# Utility done ===============================================
