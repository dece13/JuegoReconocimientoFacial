import cv2

from matplotlib import pyplot as plt

cap =cv2.VideoCapture(0)

ret,frame= cap.read()
print (ret)
print(frame)
plt.imshow(frame)

cap.release()

def take_photo():
    cap= cv2.VideoCapture(0)
    ret,frame =cap.read()
    cv2.imwrite('webcamPhoto.jpg',frame)
    cap.reoease()
take_photo()