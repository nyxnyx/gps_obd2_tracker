import pytest
from obdtracker.utils import get_json, getJSON

def test_get_json_valid():
    xml = '<?xml version="1.0" encoding="utf-8"?><string xmlns="http://tempuri.org/">{"key": "value"}</string>'
    result = get_json(xml)
    assert result == {"key": "value"}

def test_get_json_empty_text():
    xml = '<?xml version="1.0" encoding="utf-8"?><string xmlns="http://tempuri.org/"></string>'
    result = get_json(xml)
    assert result == {}

def test_get_json_legacy_name():
    xml = '<?xml version="1.0" encoding="utf-8"?><string xmlns="http://tempuri.org/">{"k": "v"}</string>'
    result = getJSON(xml)
    assert result == {"k": "v"}
