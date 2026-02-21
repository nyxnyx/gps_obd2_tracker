from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum

class WarnType(Enum):
    POWER_OFF = "Power off"
    VIBRATION = "Vibration"
    OVER_SPEED = "Over speed"
    MOVE_ALARM = "Move alarm"
    UNKNOWN = "Unknown"
    NONE = "None"
    
    @classmethod
    def from_string(cls, text: Optional[str]) -> "WarnType":
        if not text:
            return cls.NONE
        for item in cls:
            if item.value.lower() == text.lower():
                return item
        return cls.UNKNOWN

@dataclass
class DeviceInfo:
    device_id: int
    device_name: str
    model: int
    sn: str
    imei: Optional[str] = None
    key: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DeviceInfo":
        return cls(
            device_id=int(data.get("deviceID", 0)),
            device_name=data.get("deviceName", ""),
            model=int(data.get("model", 0)),
            sn=data.get("sn", ""),
            imei=data.get("ICCID"),
            key=data.get("key2018")
        )

@dataclass
class LocationData:
    lat: float
    lng: float
    speed: float
    course: int
    position_time: str
    is_gps: bool
    is_stop: bool
    battery: int
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LocationData":
        return cls(
            lat=float(data.get("lat", 0.0)),
            lng=float(data.get("lng", 0.0)),
            speed=float(data.get("speed", 0.0)),
            course=int(data.get("course", 0)),
            position_time=data.get("positionTime", ""),
            is_gps=int(data.get("isGPS", 0)) == 1,
            is_stop=int(data.get("isStop", 0)) == 1,
            battery=int(data.get("battery", 0))
        )

@dataclass
class DeviceStatusData:
    status: str
    battery: int
    battery_status: str
    signal_strength: int
    state: str
    warn_txt: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DeviceStatusData":
        return cls(
            status=data.get("status", ""),
            battery=int(data.get("battery", 0)),
            battery_status=data.get("batteryStatus", ""),
            signal_strength=int(data.get("xg", 0)),
            state=data.get("state", ""),
            warn_txt=data.get("warnTxt")
        )
        
    @property
    def is_ignition_on(self) -> bool:
        """
        Derive ignition (ACC) state from `state` string.
        Typically, state strings contain 'ACC on' or 'ACC off'.
        """
        if not self.state:
            return False
        return "acc on" in self.state.lower()
        
    @property
    def warning_type(self) -> WarnType:
        """Get the parsed Enum type for the warning text."""
        return WarnType.from_string(self.warn_txt)
