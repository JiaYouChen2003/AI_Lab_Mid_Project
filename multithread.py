import threading 
import socket
import sys
import time
import cv2
# from PIL import Image, ImageDraw, ImageFont
import numpy as np

from utils.plots import Annotator
from utils.plots import colors
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

move = ""

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
            # print(frame.shape)
            annotator = Annotator(frame, line_width=3)
            
            for *xywh, conf, cls in bbox:
                if (bbox[:-2].all() <= 1 and bbox[:-2].all() >= 0):
                    # print(bbox)
                    xywh[0] *= width
                    xywh[1] *= height
                    xywh[2] *= width
                    xywh[3] *= height
                    print(xywh[0], xywh[1], xywh[2], xywh[3])
                    x, y, w, h = xywh
                    xyxy = xywh
                    xyxy[0], xyxy[1] = (x - w) / 2, (y - h) / 2
                    xyxy[2], xyxy[3] = (x + w) / 2, (y + h) / 2
                    cls = int(cls)
                    label = names[cls]
            
                    annotator.box_label(box=xyxy, label=label, color=colors(cls, True))
                    frame = annotator.result()

            cv2.imshow("UAV video", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# 10 class
#  m00 m01 m02 m03 m04 m07 m09 m11 m12 m21
target = ["m00"]

def control():
    # time.sleep(3)
    global bbox
    bbox = []
    while target:
        for *xyxy, conf, cls in bbox:
            xyxy[0] *= frame.shape[1]
            xyxy[1] *= frame.shape[0]
            xyxy[2] *= frame.shape[1]
            xyxy[3] *= frame.shape[0]
            x, y, w, h = xyxy
            xyxy[0], xyxy[1] = (x - w / 2).long().item(), (y - h / 2).long().item()
            xyxy[2], xyxy[3] = (x + w / 2).long().item(), (y + h / 2).long().item()
            cls = int(cls)
            label = names[cls]
            if label in target:
                if xyxy[3] - (xyxy[3] - xyxy[1]) // 2 < 0.6:
                    msg = 'up 20'
                    sock.sendto(msg.encode("utf-8"), tello_address)
                    time.sleep(2)
                elif xyxy[3] - (xyxy[3] - xyxy[1]) // 2 > 0.6:
                    msg = 'down 20'
                    sock.sendto(msg.encode("utf-8"), tello_address)
                    time.sleep(2)
                elif xyxy[2] - (xyxy[2] - xyxy[0]) // 4 < 0.5:
                    # target left
                    msg = 'left 20'
                    sock.sendto(msg.encode("utf-8"), tello_address)
                    time.sleep(2)
                elif xyxy[0] + (xyxy[2] - xyxy[0]) * 3 // 4 > 0.5:
                    # target right
                    msg = 'right 20'
                    sock.sendto(msg.encode("utf-8"), tello_address)
                    time.sleep(2)
                elif xyxy[2] - xyxy[0] < 1 // 3:
                    #target forward
                    msg = 'forward 20'
                    sock.sendto(msg.encode("utf-8"), tello_address)
                    time.sleep(2)
                else:
                    msg = 'forward 50'
                    sock.sendto(msg.encode("utf-8"), tello_address)
                    time.sleep(5)
                    # msg = 'backward 300'
                    # sock.sendto(msg.encode("utf-8"), tello_address)
                    # time.sleep(10)
                    target.remove(label)

    msg = 'land'
    sock.sendto(msg.encode("utf-8"), tello_address)
    # time.sleep(2)

def detect():
    global isFrame
    global bbox
    model = tarot_model()
    print("Model load successful!")
    while True:
        if isFrame:
            print("detect bbox!")
            bbox = model.run(frame)
            print(bbox)

def main():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(locaddr)

    for i in range(0,len(_msg)):
        msg1 = _msg[i]
        sock.sendto(msg1.encode("utf-8"), tello_address)
        time.sleep(_delay[i])

    capturethread = threading.Thread(target = capture)
    capturethread.start()

    detectthread = threading.Thread(target = detect)
    detectthread.start()

if __name__ == '__main__':
    main()