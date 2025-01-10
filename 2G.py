# Standard Tools
from scipy.io import wavfile
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#=============================================================
def show_info(aname, a, r):
    """Show basic information about the audio signal."""
    print(f'Audio: {aname}')
    print(f'Rate: {r} Hz')
    print(f'Shape: {a.shape}')
    print(f'Dtype: {a.dtype}')
    print(f'Min, Max: {a.min()}, {a.max()}')
    plot_info(aname, a, r)

def plot_info(aname, a, r):
    """Plot the waveform of the audio signal."""
    sTitle = f'Signal Wave - {aname} at {r}Hz'
    plt.title(sTitle)
    sLegend = [f'Ch{c+1}' for c in range(a.shape[1])]
    for c in range(a.shape[1]):
        plt.plot(a[:, c], label=f'Ch{c+1}')
    plt.legend(sLegend)
    plt.show()

def process_audio_file(input_filename, output_filename, channels):
    """Process the audio file, plot information, and save data as CSV."""
    print(f'Processing: {input_filename}')
    InputRate, InputData = wavfile.read(input_filename)
    show_info(f'{channels} channel', InputData, InputRate)

    ProcessData = pd.DataFrame(InputData)
    ProcessData.columns = [f'Ch{i+1}' for i in range(channels)]
    ProcessData.to_csv(output_filename, index=False)
    print(f'Saved processed data to: {output_filename}')

#=============================================================
# Process audio files for 2, 4, 6, and 8 channels
audio_files = [
    (r"C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Raw_Data\2ch-sound.wav", r'C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Processed Data\HORUS-Audio-2ch.csv', 2),
    (r"C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Raw_Data\4ch-sound.wav", r'C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Processed Data\HORUS-Audio-4ch.csv', 4),
    (r"C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Raw_Data\6ch-sound.wav", r'C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Processed Data\HORUS-Audio-6ch.csv', 6),
    (r"C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Raw_Data\8ch-sound.wav", r'C:\Users\Rohsn Chimbaikar\PycharmProjects\Data-Science_Practicals\Processed Data\HORUS-Audio-8ch.csv', 8)
]

for input_file, output_file, channels in audio_files:
    process_audio_file(input_file, output_file, channels)

print('Audio to HORUS - Done')
