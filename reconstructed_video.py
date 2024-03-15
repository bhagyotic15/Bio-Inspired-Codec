import cv2
import numpy as np
import os

# Path to the folder containing reconstructed frames
frames_folder = 'reconstructedFigures/reconstucted_image'

# Path to the folder where the reconstructed video will be saved
output_folder = 'reconstructed_video'
os.makedirs(output_folder, exist_ok=True)

# Get the list of frames in the folder
frames_list = sorted(os.listdir(frames_folder))

# Load reconstructed audio
reconstructed_audio_path = 'reconstructed_audio/reconstructed_audio.npy'
audio_data = np.load(reconstructed_audio_path, allow_pickle=True)

# Get the dimensions of the first frame to use for video resolution
first_frame_path = os.path.join(frames_folder, frames_list[0])
first_frame = cv2.imread(first_frame_path)
height, width, _ = first_frame.shape

# Specify the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Specify the codec
output_video_path = os.path.join(output_folder, 'reconstructed_video.mp4')
out = cv2.VideoWriter(output_video_path, fourcc, 30.0, (width, height))  # Use dimensions of original images

# Iterate over each frame and write it to the video
for frame_file in frames_list:
    frame_path = os.path.join(frames_folder, frame_file)
    frame = cv2.imread(frame_path)
    if frame is not None:
        out.write(frame)

# Release the VideoWriter object
out.release()

print(f"Reconstructed video saved at: {output_video_path}")
