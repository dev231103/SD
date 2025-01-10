import os
import pandas as pd
import numpy as np
from imageio.v2 import imread

# Input directory and initialization
dataBaseDir = r'C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Store_Video'

processedData = pd.DataFrame()

print("==== Start Frame Processing ====")

# Loop through each image file in the directory
for file in os.listdir(dataBaseDir):
    if file.endswith(".jpg"):
        inputFileName = os.path.join(dataBaseDir, file)
        print(f"Processing: {inputFileName}")

        try:
            # Read image data
            inputData = imread(inputFileName, pilmode='RGBA')  # Adjusted for imageio
            print(f"Input Data Shape: {inputData.shape}")

            # Reshape and process data
            processRawData = inputData.flatten()
            rows = int(processRawData.shape[0] / (inputData.shape[2] + 2))
            processedFrameData = pd.DataFrame(
                np.reshape(processRawData, (rows, inputData.shape[2] + 2))
            )
            processedFrameData['Frame'] = file

            # Append to main dataset
            processedData = pd.concat([processedData, processedFrameData], ignore_index=True)

        except Exception as e:
            print(f"Error processing {inputFileName}: {e}")

# Add column names
columns = ['AxisX', 'AxisY', 'Red', 'Green', 'Blue', 'Alpha', 'FrameName']
processedData.columns = columns

# Save as CSV
outputFileName = r'C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Processed Data\HORUS-Movie-Frames.csv'
processedData.to_csv(outputFileName, index=False)
print(f"Processed Data Stored: {outputFileName}")

print("==== Frame Processing Completed ====")
