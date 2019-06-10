webServer.py is the main program logging incoming logging events and serving http pages.
webServer.py needs python 3 to run.
The logging data are saved in a .json file for each day.

index.html shows the last five days of commute logging

The logger hardware is documented in the Terminal folder.
The logging terminal uses a Raspberry Pi3 with 5 buttons connected.
A simple python script (rpi3_logger.py) is running on the raspberry which reads the buttons and sends the info to the webServer.py 
The script is set to autostart when the Raspberry powers up.
The terminal uses arcade style button, but any button will do.
A flat plate was 3D printed to hold the buttons and the Raspberry Pi3

