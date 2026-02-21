import pytest
from obdtracker.sms import SMSCommandBuilder

def test_sms_builder_default_password():
    builder = SMSCommandBuilder()
    assert builder.set_speed_alarm(80) == "speed123456 080"
    assert builder.set_speed_alarm(0) == "speed123456 000"

def test_sms_builder_custom_password():
    builder = SMSCommandBuilder("666888")
    assert builder.set_move_alarm(300) == "move666888 300"
    assert builder.change_password("111222") == "password666888 111222"

def test_sms_builder_admin_numbers():
    builder = SMSCommandBuilder()
    assert builder.set_admin_number("13712345678") == "admin123456 13712345678"
    assert builder.delete_admin_number(1) == "D101#"
    assert builder.delete_admin_number(3) == "D103#"
    with pytest.raises(ValueError):
        builder.delete_admin_number(4)

def test_sms_builder_network():
    builder = SMSCommandBuilder()
    assert builder.set_apn("cmnet") == "apn123456 cmnet"
    assert builder.set_ip_port("123.142.106.193", 8800) == "IP 123.142.106.193 8800"

def test_sms_builder_alarms():
    builder = SMSCommandBuilder()
    assert builder.set_power_off_sms_alarm(True) == "pwrsms123456,1"
    assert builder.set_power_off_sms_alarm(False) == "pwrsms123456,0"
    assert builder.set_vibration_sms_alarm(True) == "125#"
    assert builder.set_vibration_sms_alarm(False) == "126#"
    assert builder.set_vibration_time(3) == "vibtime123456,3"
    with pytest.raises(ValueError):
        builder.set_vibration_time(20)

def test_sms_builder_control():
    builder = SMSCommandBuilder()
    assert builder.cut_oil_electricity() == "DY"
    assert builder.restore_oil_electricity() == "KY"
    assert builder.reset_device() == "CQ"
    assert builder.format_device() == "FORMAT"
    assert builder.check_info() == "CXZT"
    assert builder.get_google_link() == "g1234"
