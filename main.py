import time
from MusicController import *
from LightStrip import *

myLightStrip = LightStrip(name='light strip', pin=2, numleds=16, brightness=0.5)

time.sleep(0.1) # Wait for USB to become ready

print("Hello, Pi Pico!")

MusicController().run()