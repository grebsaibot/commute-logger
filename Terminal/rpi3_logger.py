#!/usr/bin/python
from gpiozero import LED, Button
from time import sleep
import datetime
from signal import pause
import requests

button1 = Button(17)
button2 = Button(27)
button3 = Button(22)
button4 = Button(23)
button5 = Button(24)
led = LED(18)

def buttonPressed(button):
    now = datetime.datetime.now().isoformat()
    print(str(button.pin.number) + ' pressed @ ' + now)
    led.on()
    if button.pin.number == 17:
        option=1
    if button.pin.number == 27:
        option=2
    if button.pin.number == 22:
        option=3
    if button.pin.number == 23:
        option=4
    if button.pin.number == 24:
        option=5

    address = 'http://10.162.8.33:8888/opt=' + str(option)
    r = requests.get(address, headers={'User-Agent': 'Mozilla/5.0 Chrome/55.0.2883.75'})

    print(r.status_code)
    sleep(1)
    led.off()
    while button.is_pressed:
        True

while True:
    if button1.is_pressed:
        buttonPressed(button1)
    if button2.is_pressed:
        buttonPressed(button2)
    if button3.is_pressed:
        buttonPressed(button3)
    if button4.is_pressed:
        buttonPressed(button4)
    if button5.is_pressed:
        buttonPressed(button5)


#button.when_pressed = buttonPressed
#pause()
