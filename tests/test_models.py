import pytest
from obdtracker.models import DeviceInfo, LocationData, DeviceStatusData, WarnType

def test_device_info_from_dict():
    data = {"deviceID": "123", "deviceName": "Test", "model": "456", "sn": "sn123", "ICCID": "iccid123", "key2018": "key123"}
    model = DeviceInfo.from_dict(data)
    assert model.device_id == 123
    assert model.device_name == "Test"
    assert model.model == 456
    assert model.sn == "sn123"
    assert model.imei == "iccid123"
    assert model.key == "key123"

def test_location_data_from_dict():
    data = {"lat": "12.34", "lng": "56.78", "speed": "100.5", "course": "90", "positionTime": "2023-10-27 10:00:00", "isGPS": "1", "isStop": "0", "battery": "80"}
    loc = LocationData.from_dict(data)
    assert loc.lat == 12.34
    assert loc.lng == 56.78
    assert loc.speed == 100.5
    assert loc.course == 90
    assert loc.position_time == "2023-10-27 10:00:00"
    assert loc.is_gps is True
    assert loc.is_stop is False
    assert loc.battery == 80

def test_device_status_data_from_dict():
    data = {"status": "Online", "battery": "100", "batteryStatus": "Charging", "xg": "4", "state": "Normal, ACC on", "warnTxt": "Power off"}
    status = DeviceStatusData.from_dict(data)
    assert status.status == "Online"
    assert status.battery == 100
    assert status.battery_status == "Charging"
    assert status.signal_strength == 4
    assert status.state == "Normal, ACC on"
    assert status.warn_txt == "Power off"
    assert status.is_ignition_on is True
    assert status.warning_type == WarnType.POWER_OFF

def test_device_status_ignition_and_warning_edge_cases():
    data = {"state": "ACC off, door closed", "warnTxt": "Unknown warning something"}
    status = DeviceStatusData.from_dict(data)
    assert status.is_ignition_on is False
    assert status.warning_type == WarnType.UNKNOWN
    
    data2 = {"state": "", "warnTxt": ""}
    status2 = DeviceStatusData.from_dict(data2)
    assert status2.is_ignition_on is False
    assert status2.warning_type == WarnType.NONE
