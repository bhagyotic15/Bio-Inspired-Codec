import cv2
import os
from pydub import AudioSegment

cap = cv2.VideoCapture('/home/ntu-user/PycharmProjects/COMP40731---ACS---CWK---N1218683/COMP40731_video.mp4/COMP40731_video.mp4')

if not os.path.exists('frames'):
    os.makedirs('frames')

frame_count = 0
while (cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imwrite(f'frames/frame_{frame_count:03d}.png', frame)
    frame_count += 1

audio = AudioSegment.from_file('/home/ntu-user/PycharmProjects/COMP40731---ACS---CWK---N1218683/COMP40731_video.mp4/COMP40731_video.mp4')
audio.export('audio.mp3', format= 'mp3')


cap.release()
cv2.destroyAllWindows()



