class SMSCommandBuilder:
    """Utility class to generate exact SMS strings for device configuration."""
    
    def __init__(self, password: str = "123456"):
        self.password = password
        
    def change_password(self, new_password: str) -> str:
        return f"password{self.password} {new_password}"
        
    def set_admin_number(self, phone_number: str) -> str:
        """Set the administrator phone number."""
        return f"admin{self.password} {phone_number}"
        
    def delete_admin_number(self, index: int) -> str:
        """Delete administrator number. Index should be 1, 2, or 3."""
        if index not in (1, 2, 3):
            raise ValueError("Admin index must be 1, 2, or 3")
        return f"D10{index}#"
        
    def set_apn(self, apn: str) -> str:
        return f"apn{self.password} {apn}"
        
    def set_apn_user(self, user: str) -> str:
        return f"apnuser{self.password} {user}"
        
    def set_apn_password(self, pwd: str) -> str:
        return f"apnpasswd{self.password} {pwd}"
        
    def set_ip_port(self, ip: str, port: int) -> str:
        return f"IP {ip} {port}"
        
    def set_power_off_sms_alarm(self, enable: bool) -> str:
        return f"pwrsms{self.password},{1 if enable else 0}"
        
    def set_power_off_call_alarm(self, enable: bool) -> str:
        return f"pwrcall{self.password},{1 if enable else 0}"
        
    def set_acc_auto_arm(self, enable: bool) -> str:
        return f"ACCLOCK,{self.password},{1 if enable else 0}"
        
    def set_auto_arm_time(self, minutes: int) -> str:
        return f"ACCLT,{self.password},{minutes}"
        
    def set_vibration_sms_alarm(self, enable: bool) -> str:
        return "125#" if enable else "126#"
        
    def set_vibration_call_alarm(self, enable: bool) -> str:
        return "122#" if enable else "121#"
        
    def set_vibration_time(self, seconds: int) -> str:
        """Set vibration alarm time. 0 cancels, max is 15."""
        if not (0 <= seconds <= 15):
             raise ValueError("Vibration time must be between 0 and 15 seconds")
        return f"vibtime{self.password},{seconds}"
        
    def set_speed_alarm(self, speed_kmh: int) -> str:
        """Set speed alarm. 0 cancels the alarm."""
        return f"speed{self.password} {speed_kmh:03d}"
        
    def set_move_alarm(self, distance_meters: int) -> str:
        return f"move{self.password} {distance_meters}"
        
    def cut_oil_electricity(self) -> str:
        return "DY"
        
    def restore_oil_electricity(self) -> str:
        return "KY"
        
    def format_device(self) -> str:
        return "FORMAT"
        
    def reset_device(self) -> str:
        return "CQ"
        
    def check_info(self) -> str:
        return "CXZT"
        
    def get_google_link(self) -> str:
        return "g1234"
