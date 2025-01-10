import os
import cv2

# Input video file and output directory
inputFileName = r"C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Raw_Data\Dog.mp4"
dataBaseDir = r'C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Store_Video'

# Create output directory if it doesn't exist
if not os.path.exists(dataBaseDir):
    os.makedirs(dataBaseDir)

print("==== Start Movie to Frames ====")

# Capture video
vidcap = cv2.VideoCapture(inputFileName)
success, image = vidcap.read()
frame_count = 0

# Loop through the video frames
while success:
    frameFileName = os.path.join(dataBaseDir, f'dog-frame-{frame_count:04d}.jpg')
    cv2.imwrite(frameFileName, image)  # Save frame as .jpg file

    if os.path.getsize(frameFileName) == 0:  # Remove empty frames
        os.remove(frameFileName)
        print(f"Removed: {frameFileName}")
    else:
        print(f"Extracted: {frameFileName}")

    success, image = vidcap.read()
    frame_count += 1

print(f"==== Generated {frame_count} Frames ====")
print("==== Movie to Frames Completed ====")
