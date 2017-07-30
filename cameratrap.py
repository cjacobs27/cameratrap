import cv2, time, pandas, os
from datetime import datetime


class Cameratrap:

    def __init__(self):
        self.first_frame = None
        self.mstatus_list = [None, None]
        self.mtimes = []
        self.fstatus_list = [None, None]
        self.ftimes = []
        self.mdf = pandas.DataFrame(columns=["Start", "End"])
        self.fdf = pandas.DataFrame(columns=["Start", "End"])
        self.face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.video = cv2.VideoCapture(0)
        self.mstatus = 0
        self.fstatus = 0
        print("1")


    def getCam(self):
        while True:
            self.check, self.frame = self.video.read()
            # cv2.imshow("Webcam Feed", self.frame)
            self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            self.gray = cv2.GaussianBlur(self.gray, (21, 21), 0)
            if self.first_frame is None:
                self.first_frame = self.gray
            self.delta_frame = cv2.absdiff(self.first_frame, self.gray)
            self.thresh_frame = cv2.threshold(self.delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
            self.thresh_frame = cv2.dilate(self.thresh_frame, None, iterations=3)
            self.faceDetect()
            cv2.imshow("Webcam Feed", self.frame)
            cv2.imshow("Gray Frame",self.gray)
            cv2.imshow("Delta Frame",self.delta_frame)
            cv2.imshow("Threshold Frame",self.thresh_frame)
            self.key = cv2.waitKey(1)
            if self.key == ord('q'):
                self.video.release()
                cv2.destroyAllWindows

    def faceDetect(self):
        faces = self.face_cascade.detectMultiScale(self.gray,
        scaleFactor=1.5,
        minNeighbors=5)
        for x, y, w, h in faces:
            if (w * h) < 10000:
                continue
            self.fstatus = 1
            self.frame = cv2.rectangle(self.frame, (x, y), (x + w, y + h), (152, 3, 186), 2)
            #takepic

#TODO: Fix close bug