# GPS OBD2 tracker
This project is for Chinese GPS tracker for cars.

# Which GPS ODB2 trackers are supported?
This is good question and very hard to find proper answer. It was developed and tested on devices bought on 
AliExpress which looks like this one:
![GPS ODB2 Tracker](/doc/images/gps_tracker.png)
After reading attached instruction - I have found error - they say to connect to 3.tkstargps.net side but app is AIKA. What I found - that device is connecting (after sending SMS to it) to XX.aika168.com - and communication between mobile app and server is open (no ssl). This was an invitation to create this library. Other GPS OBD2 Trackers that work with AIKA mobile app should work with this library too. How to check that? Look at pictures of 
mobile app that usuary is shown on pages where somebody is selling device. If you see something like:
![AIKA APP](/doc/images/OBD-II-GPS-Tracker.jpg)

Map with blue top bar with reload button on right and back arrow on left. This is AIKA app. And here is a link to Google app store: [AIKA app](https://play.google.com/store/apps/details?id=com.fw.gps.xinmai&hl=en_US).

# How to use this code?
It's a library. To integrate with your code you have to write something like this:
```
from obdtracker import api, device_status, obd, location
import logging

def main():
    la = api.API("http://www.aika168.com/")
    la.registerUpdater(location.Location(la))
    la.registerUpdater(device_status.DeviceStatus(la))

    loop = asyncio.get_event_loop()

    loop.run_until_complete(la.doLogin('<Your device id>', '<Your server password>') )
    loop.run_until_complete(la.doUpdate())

    attrs = vars(la)
    print(', '.join("%s: %s" % item for item in attrs.items()))

if __name__ == "__main__":
    main()
```

# What is next step?
Right now I'm working on:
- Home Assistant device tracker
- App for getting information about protocol between device and gateway at XX.aika168.com
