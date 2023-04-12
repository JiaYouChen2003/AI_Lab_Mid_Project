import threading 
import socket
import time
import cv2
# import sys
# from PIL import Image, ImageDraw, ImageFont
# import numpy as np

# from utils.plots import Annotator
# from utils.plots import colors
from yolov3_tarot import tarot_model

# Tello EDU 的IP和port，所有控制命令將發送到此位置
tello_address = ('192.168.10.1', 8889)

# 本機監聽port地址，將會從這邊收到來自無人機的response
host = ''
port = 9000
locaddr = (host,port)


_msg = ["command", "streamon", "speed 50", "takeoff"]
_delay=[3, 3, 3, 3]

# 10 class
# m00 m01 m02 m03 m04 m07 m09 m11 m12 m21
# classes = ["m00", "m01", "m02", "m03", "m04", "m07", "m09", "m11", "m12", "m21"]
names = ["m00", "m01", "m02", "m03", "m04", "m07", "m09", "m11", "m12", "m21"]

# move = ""

bbox = []
frame = None
isFrame = 0

# bboxes = []
# scores = []
# colors = []
# names = []
# classes = ["m00", "m01", "m02", "m03", "m04", "m07", "m09", "m11", "m12", "m21"]

# imgsz = (720, 960, 3)
def capture():
    # cap=cv2.VideoCapture("udp://192.168.10.1:11111")
    cap=cv2.VideoCapture(0)
    global bbox
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    while True:
        global isFrame, frame
        isFrame , frame=cap.read() # (720, 960, 3)

        if isFrame:
            cv2.imshow("UAV video", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# 10 class
#  m00 m01 m02 m03 m04 m07 m09 m11 m12 m21
target = ["m00"]

def control():
    for i in range(0,len(_msg)):
        msg1 = _msg[i]
        sock.sendto(msg1.encode("utf-8"), tello_address)
        time.sleep(_delay[i])
    global bbox
    bbox = []
    while target:
        for *xywh, conf, cls in bbox:            
            x, y, w, h = xywh
            cls = int(cls)
            label = names[cls]
            if label in target:
                flag = False
                if y < 0.4:
                    msg = 'up 20'
                    sock.sendto(msg.encode("utf-8"), tello_address)
                    time.sleep(2)
                elif y > 0.6:
                    msg = 'down 20'
                    sock.sendto(msg.encode("utf-8"), tello_address)
                    time.sleep(2)
                elif x < 0.4:
                    # target left
                    msg = 'left 20'
                    sock.sendto(msg.encode("utf-8"), tello_address)
                    time.sleep(2)
                elif x > 0.6:
                    # target right
                    msg = 'right 20'
                    sock.sendto(msg.encode("utf-8"), tello_address)
                    time.sleep(2)
                else:
                    msg = 'up 30'
                    sock.sendto(msg.encode("utf-8"), tello_address)
                    time.sleep(3)
                    msg = 'forward 300'
                    sock.sendto(msg.encode("utf-8"), tello_address)
                    time.sleep(5)
                    msg = 'land'
                    sock.sendto(msg.encode("utf-8"), tello_address)
                    time.sleep(5)

def detect():
    global isFrame, bbox
    model = tarot_model()
    print("Model load successful!")
    while True:
        if isFrame:
            if model.run(frame).shape[0] != 0:
                bbox = model.run(frame)
            print(bbox)

def main():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(locaddr)

    capturethread = threading.Thread(target = capture)
    capturethread.start()

    detectthread = threading.Thread(target = detect)
    detectthread.start()

    controlthread = threading.Thread(target = control)
    controlthread.start()

if __name__ == '__main__':
    main()