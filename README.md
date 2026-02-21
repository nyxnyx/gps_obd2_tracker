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
It's an asynchronous library. To integrate with your code:

```python
import asyncio
from obdtracker import API, Location, DeviceStatus

async def main():
    # Use the context manager to ensure connections are closed
    async with API("http://www.aika168.com/") as tracker:
        tracker.register_updater(Location(tracker))
        tracker.register_updater(DeviceStatus(tracker))

        # Login and update data
        await tracker.login('<Your device id>', '<Your server password>')
        await tracker.update()

        # Access typed data
        if tracker.location:
             print(f"Position: {tracker.location.lat}, {tracker.location.lng}")
        
        if tracker.status:
             print(f"Battery: {tracker.status.battery}%")
             print(f"Ignition is {'ON' if tracker.status.is_ignition_on else 'OFF'}")
             print(f"Warning: {tracker.status.warning_type.name}")

        # You can also send commands to the device across the network
        # await tracker.send_command("DY") # Cut oil/electricity
        
if __name__ == "__main__":
    asyncio.run(main())
```

### SMS Fallback Generator
If the GPS tracker doesn't connect to the internet, you can create standard SMS commands using `SMSCommandBuilder`:

```python
from obdtracker.sms import SMSCommandBuilder
sms = SMSCommandBuilder(password="123456")
message = sms.set_speed_alarm(80) 
print(message) # "speed123456 080"
```


# NEW: list of UNSUPPORTED mobile applications
If you are going to buy GPS OBD2 Tracker checkout this list to see which mobile apps are unsupported. Acually it means that those mobile apps use cloud service that is not supported with this tool:
(Unsupported cloud / OBD2 GPS Trackers)[/doc/unsupported.md]

# Supported apps / cloud services:
1. aika168.com / www.aika168.com - developed using this cloud service - works
1. gpscj.net / gps18.com - not sure - possibly it is working

# What is next step?
Right now I'm working on:
- App for getting information about protocol between device and gateway at XX.aika168.com
- Further expanding commands and mapping hardware protocols.

**Home Assistant Integration**: The Home Assistant custom component for this library is available at [maika](https://github.com/nyxnyx/maika).
