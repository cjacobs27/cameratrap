'''
This camera trap detects both motion (green rectangle)
and faces (purple rectangle)
and creates a log of both detected motion and faces in a CSV file.
It also saves the frame to .jpg every 10 seconds while a face is detected.
You could use this to see who comes up to your front door while you're out, for example.

'''

import cv2, time, pandas, os
from datetime import datetime

first_frame=None
mstatus_list=[None,None]
mtimes=[]
mdf=pandas.DataFrame(columns=["Start","End"])
fstatus_list=[None,None]
ftimes=[]
fdf=pandas.DataFrame(columns=["Start","End"])
face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
video=cv2.VideoCapture(0)

def takepic(fstatus):
    if fstatus == 1:
        # CHANGE THIS FILEPATH TO WHEREVER YOU WANT TO SAVE THE FILES, this is just an example filepath:
        file = r"/Users/chelseyjacobs/Desktop/camerapics/"
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

    (cnts,_)=cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    faces = face_cascade.detectMultiScale(gray,
    scaleFactor=1.5,
    minNeighbors=5)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue

        (x, y, w, h)=cv2.boundingRect(contour)
        mstatus=1
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,255), 1)
    mstatus_list.append(mstatus)
    mstatus_list=mstatus_list[-2:]

    for x, y, w, h in faces:
        if (w * h) < 10000:
            continue
        fstatus=1
        frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255,0,0), 2)
        takepic(fstatus)

    fstatus_list.append(fstatus)
    fstatus_list=fstatus_list[-2:]

    if mstatus_list[-1]==1 and mstatus_list[-2]==0:
        mtimes.append(datetime.now())
    if mstatus_list[-1]==0 and mstatus_list[-2]==1:
        mtimes.append(datetime.now())

    if fstatus_list[-1]==1 and fstatus_list[-2]==0:
        ftimes.append(datetime.now())
    if fstatus_list[-1]==0 and fstatus_list[-2]==1:
        ftimes.append(datetime.now())

#uncomment these to see vaguely sci-fi filters.
    # cv2.imshow("Gray Frame",gray)
    # cv2.imshow("Delta Frame",delta_frame)
    # cv2.imshow("Threshold Frame",thresh_frame)
    cv2.imshow("Color Frame",frame)

    key=cv2.waitKey(1)

    if key==ord('q'):
        ftimes.append(datetime.now())
        break
print(fstatus_list)

for f in range(0,len(ftimes),2):
    if len(ftimes) % 2 == 0:
        fdf=fdf.append({"Start":ftimes[f],"End":ftimes[f+1]}, ignore_index=True)
    else:
        ftimes.append(datetime.now())
        fdf = fdf.append({"Start": ftimes[f], "End": ftimes[f + 1]}, ignore_index=True)

for m in range(0,len(mtimes),2):
    if len(mtimes) % 2 == 0:
        mdf=mdf.append({"Start":mtimes[m],"End":mtimes[m+1]}, ignore_index=True)
    else:
        mtimes.append(datetime.now())
        mdf = mdf.append({"Start": mtimes[m], "End": mtimes[m + 1]}, ignore_index=True)

print(mdf)


fdf.to_csv("FaceTimes.csv")
mdf.to_csv("MotionTimes.csv")

video.release()
cv2.destroyAllWindows
