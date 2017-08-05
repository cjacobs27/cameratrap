'''
This camera trap detects both motion (green rectangle)
and faces (purple rectangle)
and creates a log of both detected motion and faces in a CSV file.
It also saves the frame every 10 seconds while a face is detected.

'''

import cv2, time, pandas, os
from datetime import datetime

first_frame=None
mstatus_list=[None,None]
mtimes=[]
fstatus_list=[None,None]
ftimes=[]
mdf=pandas.DataFrame(columns=["Start","End"])
fdf=pandas.DataFrame(columns=["Start","End"])
face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
video=cv2.VideoCapture(0)

def takepic(fstatus):
    if fstatus == 1:
        file = r"C:\Users\Chelsey\Documents\Projects\cameratrap\cameratrap_faces\\"
        if os.path.exists(file):
            now = datetime.now().strftime("%I.%M.%S.%f")
            cv2.imwrite(file + "_captured_" + now + ".jpg", frame)
            print("Saving image.")
            time.sleep(1)
    elif fstatus == 0:
        pass

while True:
    check, frame = video.read()
    mstatus=0
    fstatus=0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)

    if first_frame is None:
        first_frame=gray
        continue

    delta_frame=cv2.absdiff(first_frame,gray)
    thresh_frame=cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame=cv2.dilate(thresh_frame, None, iterations=3)

    (_,cnts,_)=cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    faces = face_cascade.detectMultiScale(gray,
    scaleFactor=1.5,
    minNeighbors=5)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue

        mstatus=1

        (x, y, w, h)=cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 1)

    # mstatus_list.append(mstatus)

    for x, y, w, h in faces:
        if (w * h) < 10000:
            continue
        fstatus=1
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (152, 3, 186), 2)
        # takepic(fstatus)

    fstatus_list.append(fstatus)

    # if mstatus_list[-1]==1 and mstatus_list[-2]==0:
    #     mtimes.append(datetime.now())
    # if mstatus_list[-1]==0 and mstatus_list[-2]==1:
    #     mtimes.append(datetime.now())

    if fstatus_list[-1]==1 and fstatus_list[-2]==0:
        ftimes.append(datetime.now())
    if fstatus_list[-1]==0 and fstatus_list[-2]==1:
        ftimes.append(datetime.now())

    # cv2.imshow("Gray Frame",gray)
    # cv2.imshow("Delta Frame",delta_frame)
    # cv2.imshow("Threshold Frame",thresh_frame)
    cv2.imshow("Color Frame",frame)

    key=cv2.waitKey(1)

    if key==ord('q'):
        if fstatus==1:
            ftimes.append(datetime.now())
        if mstatus==1:
            mtimes.append(datetime.now())
        break

for f in range(0,len(ftimes),2):
    fdf=fdf.append({"Start":ftimes[f],"End":ftimes[f+1]},ignore_index=True)


# for m in range(0,len(mtimes),2):
#     mdf=mdf.append({"Start":mtimes[m],"End":mtimes[m+1]},ignore_index=True)


fdf.to_csv("FaceTimes.csv")
# mdf.to_csv("MotionTimes.csv")

video.release()
cv2.destroyAllWindows
