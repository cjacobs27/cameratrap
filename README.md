**_Camera Trap with Motion & Face Detection Times Graph_**

**To run this program with the graph feature, please run trap_plotting.py.**

**If you just want to run the camera trap, run cameratrap.py instead.**

**You still need both files to run trap_plotting.py though, plus the Haar cascade: haarcascade_frontalface_default.xml.**

The cameratrap.py script will:
* Open a window showing your webcam feed.
* Immediately set a 'baseline' image against which it will check for movement, eg your front porch, or your garden.
* Movement detected in the feed will be indicated in the feed window, with a yellow rectangle around the moving object.
* Faces will be indicated with a blue rectangle. Multiple faces can be detected at once.
* While a face is detected, a .jpg image will be saved from the webcam feed every second.
* **Hit Q at any time to end the webcam feed and image recording.**
* Date and time information about every instance of faces and/or movement will be recorded in a .csv file.
* Please note this information is overwritten every time cameratrap.py is run, but the .jpg images are not overwritten or deleted.

The trap_plotting.py script will:
* Run cameratrap.py.
* When Q is pressed or the window closed, the .csv files are created.
* A Bokeh graph of the .csv information will open in your browser.
* You may be prompted to select a program to open the graph html file - please select your normal web browser.

_Troubleshooting_

*I got a cv2 error :(*

This needs a webcam to work. The cameratrap.py script looks in the default local port for a webcam, so if you get the following error:

``cv2.error: C:\projects\opencv-python\opencv\modules\imgproc\src\color.cpp:9748: error: (-215) scn == 3 || scn == 4 in function cv::cvtColor``

You either need to plug your webcam in, or edit the following line to the correct port for your webcam:

``
video=cv2.VideoCapture(0)
``

0 is the default port, so if you needed port 500 for example, change it to:

``
video=cv2.VideoCapture(500)
``

*I want to change how often it saves pictures*

To adjust the frequency of .jpg saving, go to this function in cameratrap.py:

```
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
```
And change the number in this line:

`time.sleep(1)`

The number represents the number of seconds between images you want to leave. The highest I recommend is 10 seconds, to 
prevent lag (in the case of additional faces appearing between image saves for example).
#####I want to change where it saves pictures

No worries, just change the filepath in this line, in the same function as above:

`        file = r"C:\Users\Chelsey\Documents\Projects\cameratrap\cameratrap_faces\\"`
