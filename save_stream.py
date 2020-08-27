import pafy
import cv2

url = "https://www.youtube.com/watch?v=_9OBhtLA9Ig"
video = pafy.new(url)
best = video.getbest(preftype="mp4")

capture = cv2.VideoCapture()
capture.open(best.url)

# while True:
#     ret, frame = cap.read()
#     """
#     your code here
#     """
#     cv2.imshow('frame', frame)
#     if cv2.waitKey(20) & 0xFF == ord('q'):
#         break
#
# cap.release()
# cv2.destroyAllWindows()