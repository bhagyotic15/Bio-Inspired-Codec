import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
import io
from scipy.io import wavfile

filename = 'sounds/audio.mp3'
# Function to convert mp3 to wav and return its data
def read_mp3(filename):
    sound = AudioSegment.from_mp3(filename)
    with io.BytesIO() as wav_data:
        sound.export(wav_data, format="wav")
        wav_data.seek(0)
        rate, data = wavfile.read(wav_data)
    return rate, data

# Function to display sound file information
def display_info(data, rate):
    num_samples = len(data)
    length = len(data) / rate
    min_val = np.min(data)
    max_val = np.max(data)
    print("Number of samples:", num_samples)
    print("Length (seconds):", length)
    print("Minimum value:", min_val)
    print("Maximum value:", max_val)

# Read the mp3 files
rateAudio, dataAudio = read_mp3(filename)

# Display information about each sound file
print("Sound Information:")
display_info(dataAudio, rateAudio)


# Plot the data
plt.figure(figsize=(10, 5))

plt.plot(dataAudio, color='blue')  # Plot data1 in blue
plt.title('Sound ')
plt.xlabel('Sample')
plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()

# Store the data in npy files
np.save('sounds/dataAudio.npy', dataAudio)
np.save('sounds/rateAudio.npy', rateAudio)

