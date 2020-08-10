Church Attendance API
=====================

The Church Attendance API is an application use to take the attendace for the Walla Walla University Church.

It is written in Python, and uses Tensorflow for determining the the amount of people present in the church and Tkinter for its graphical interface.

The application connects to Raspberry Pis with camera modules that are atteched to the ceiling and requests images to process them in the local computer to determine attendace. The API handles the connectivity with the Pis, processing of the images and the outputting of result. At every algorithm run, the received images from the previous session are deleted.

[![MenuDemo.jpg](https://i.postimg.cc/hPFJJmgw/MenuDemo.jpg)](https://postimg.cc/qgLBSzNX)

Watch a demo video

Installation
---------------------

### Build from source

To build for Windows install [Python](https://www.python.org/downloads/release/python-373/).

Open cmd and create new virtual enviorment called "churchapp_env" using the following:

```
python -m venv churchapp_env
```
Then, activate the environment by issuing

```
churchapp_env\Scripts\activate.bat
```

Install the necessary packages needed for the app by issuing the following commands:

```
pip install opencv-python==4.1.0.25
pip install tensorflow==1.13.1
pip install matplotlib==3.0.3
pip install pillow==6.0.0
pip install pysftp==0.2.9
pip install pyinstaller==3.6
```

In the cmd prompt, go to the ChurchAttendanceAPI directory and run the app using:

```
python ChurchAttendanceAPI.py
```

### Download the executable file

The project can be run as an executable stand alone file for convenience purposes. Download [here](https://www.dropbox.com/s/qy2uhh94vxb8coo/ChurchAttendanceAPI.zip?dl=0)

Usage
-----

[![Church-Attendace-Features.png](https://i.postimg.cc/xdy73bFt/Church-Attendace-Features.png)](https://postimg.cc/sBxwV1zh)

-	Run the thread button: Once this button is press, a thread that requests the images form the Pis and runs church attendance algorithm will begin.
-	Device manager tab: In order to tell the API what device to connect and request images, a device manager tab was created so that the user can connect to RPis by giving the host a name (or IP address), username and password.
-	Output count: After the algorithm is done processing the images, it will display the count of people per image and the total attendance count which is the sum of each individual image count.
-	Visual verification of count: The purpose of this feature is so that the user can evaluate the algorithm result and determine if the count is legitimate. 
-	Images dropdown menu: A dropdown menu to switch to other processed images from other Pis and find its respective count. 

More information about the project regarding the development process and reliability can be found under the capstone [project report](https://www.dropbox.com/s/8sqb05b3igar5to/FinalReport2020_LuisJimenez.pdf?dl=0).
