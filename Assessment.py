import cv2

# providing the file path
video_path = 'COMP40731_video.mp4'

# open the video capture
cap = cv2.VideoCapture(video_path)
# checking the video capture is successfully opened
if not cap.isOpened():
    print(f"Error: Update to open the video at path {video_path}")
else:
    print("press'q' to stop the video")

    # read and display each frame from the video
    while True:
        ret, frame = cap.read()

        # Break the loop if video has ended
        if not ret:
            break
        # Break the loop if 'q'is pressed
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    # Released the video capture object
    cap.release()
    # Closed all windows
    cv2.destroyAllWindows()




