---
marp: true
theme: default
class: lead
paginate: true
backgroundColor: #f8f9fa
---

# 🚗 GPS OBD2 Tracker & Home Assistant Integration
## Project Overview
**Tracking your vehicle with AIKA cloud and Home Assistant**

---

## 🎯 What is this project?

A complete open-source solution to integrate Chinese GPS OBD2 Trackers (using the AIKA mobile app infrastructure) with your custom Python applications and **Home Assistant**.

**It breaks down into two core tools:**
1. **`obdtracker`**: A robust, asyncio Python library wrapping the AIKA cloud API.
2. **`maika`**: A custom Home Assistant component (`custom_component`) for seamless Smart Home integration.

---

## 📱 Supported Devices

The project supports GPS OBD2 trackers that utilize the **AIKA** mobile app and cloud service (`XX.aika168.com`).

* **How to identify supported devices:**
  * Purchased from AliExpress, Wish, Gearbest, etc.
  * Their manual points to `3.tkstargps.net` or `aika168.com`.
  * The companion mobile app features a blue top bar and is listed as **"AIKA"** on the Google Play Store.

---

## ⚙️ The Core API: `obdtracker`

A modern Python library that communicates with the GPS tracker's cloud servers.

- **Asynchronous**: Built on `asyncio` and `httpx` for non-blocking network calls.
- **Typed Models**: Clean Python dataclasses for `DeviceInfo`, `LocationData`, and `DeviceStatus`. 
   - *NEW*: `WarnType` Enums and `is_ignition_on` detection for precise hardware state checking.
- **Modular Updaters**: Easily fetch tracking data (`Location`), vehicle diagnostics (`OBD`), or general stats (`DeviceStatus`).
- **Device Control**: Leverage `send_command()` to dynamically push configurations or remote actions (like Cut Oil/Electricity) directly to your car via the platform API.
- **SMS Fallback**: Includes the robust `SMSCommandBuilder` class to instantly generate perfectly formatted direct-to-SIM configuration texts (e.g. APN setups, alarms, passwords).
- **Fully Tested**: Powered by a 100% passing `pytest` and `pytest-asyncio` suite, safely mocking network layers.

---

## 🏠 Home Assistant Integration: `maika`

The `maika` component brings your car's data directly into your Home Assistant dashboard!

- **Auto-Discovery**: Automatically spawns sensors and a `device_tracker` entity.
- **Device Tracking**: Follow your vehicle on the Home Assistant map (`device_tracker` entity with GPS source type).
- **Extensive Sensors**: Over 20+ entities exposing real-time vehicle data securely derived from the updated API schema.
- **Service Action Calls**: *NEW* Support for `maika.send_command` allowing Home Assistant automations to push commands (like `DY` to cut engine) back to the remote device!

---

## 📊 Live Sensor Data in Home Assistant

Get detailed insights about your vehicle directly in HA, including:

* **Location Details**: Latitude, Longitude, Course, Speed
* **Device Status**: Battery percentage, Battery status, Signal strength (Xg), Online State
* **Hardware Info**: ICCID, Serial Number, VIN, Model
* **Warnings & Alerts**: Granular warnings mapped to precise Enums (`Warning Type` sensor) such as *Power off*, *Over speed*, or *Move alarm*.
* **Ignition State**: Dedicated explicit `maika.ignition` state tracking derived dynamically from onboard diagnostic flags (the ACC line).

Everything updates periodically based on a configurable async dispatcher loop.

---

## 🛠️ How to configure `maika`

Simply drop the `maika` custom component into your HA folder and add this to `configuration.yaml`:

```yaml
maika:
  username: !secret aika_username    # Your device serial number
  password: !secret aika_password    # Your aika password (default: 123456)
  address: !secret aika_server       # http://www.aika168.com
```

The system will handle login, session retention, and gracefully updating all spawned sensors.

---

## 🚀 Moving Forward & Next Steps

* **Expanded Cloud Support**: Investigate and add support for other Chinese GPS cloud services (e.g., `gpscj.net` / `gps18.com`).
* **Protocol Insights**: Develop standalone apps to analyze the direct protocol between the OBD device and the AIKA gateway.
* **Component Refinements**: Leverage the newly modernized `pytest` setups in both projects to aggressively refactor and iterate on new Home Assistant features safely!

---

# Thank You!
### Drive Safe & Keep Tracking! 🚗💨
