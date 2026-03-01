#!/usr/bin/env python3
"""
Simple test runner for IPWho Python SDK.
Does not require pytest - uses only Python built-ins.
"""

import sys
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.client import IPWho
from src.types import GeoLocation, Timezone, Connection, Security

# Load fixture
fixture_path = Path(__file__).parent / "src" / "response.json"
with open(fixture_path, "r") as f:
    fixture = json.load(f)


class TestResults:
    """Track test results."""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def add_pass(self, test_name):
        self.passed += 1
        print(f"  ✓ {test_name}")
    
    def add_fail(self, test_name, error):
        self.failed += 1
        self.errors.append((test_name, error))
        print(f"  ✗ {test_name}")
        print(f"    Error: {error}\n")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Test Results: {self.passed}/{total} passed")
        print(f"{'='*60}\n")
        return self.failed == 0


results = TestResults()

def test(name):
    """Decorator for test functions."""
    def decorator(func):
        def wrapper():
            try:
                func()
                results.add_pass(name)
            except AssertionError as e:
                results.add_fail(name, str(e))
            except Exception as e:
                results.add_fail(name, f"{type(e).__name__}: {str(e)}")
        return wrapper
    return decorator


# Tests

@test("API key validation - empty string")
def test_api_key_empty():
    try:
        IPWho("")
        raise AssertionError("Expected ValueError for empty API key")
    except ValueError as e:
        assert "API Key is required" in str(e)


@test("API key validation - None")
def test_api_key_none():
    try:
        IPWho(None)
        raise AssertionError("Expected ValueError for None API key")
    except ValueError as e:
        assert "API Key is required" in str(e)


@test("Client initialization with valid API key")
def test_client_init():
    client = IPWho("sk_test_123")
    assert client.api_key == "sk_test_123"
    assert client.base_url == "https://api.ipwho.org/v1"


@test("GeoLocation type mapping")
def test_geo_location_type():
    geo_data = fixture["data"]["geoLocation"]
    location = GeoLocation(geo_data)
    
    assert location.continent == "Asia"
    assert location.continent_code == "AS"
    assert location.country == "India"
    assert location.country_code == "IN"
    assert location.capital == "New Delhi"
    assert location.latitude == 17.3843
    assert location.longitude == 78.4583
    assert isinstance(location.latitude, float)
    assert isinstance(location.longitude, float)


@test("Timezone type mapping")
def test_timezone_type():
    tz_data = fixture["data"]["timezone"]
    timezone = Timezone(tz_data)
    
    assert timezone.time_zone == "Asia/Kolkata"
    assert timezone.abbr == "IST"
    assert timezone.offset == 19800
    assert timezone.is_dst is False
    assert isinstance(timezone.offset, int)
    assert isinstance(timezone.is_dst, bool)


@test("Connection type mapping")
def test_connection_type():
    conn_data = fixture["data"]["connection"]
    connection = Connection(conn_data)
    
    assert connection.asn_number == 24186
    assert connection.asn_org == "RailTel Corporation of India Ltd"
    assert connection.isp == "RailTel Corporation Of India Ltd."
    assert connection.org == "RailTel Corporation Of India Ltd."
    assert connection.domain is None
    assert connection.connection_type == "Cable/DSL"
    assert isinstance(connection.asn_number, int)


@test("Security type mapping")
def test_security_type():
    sec_data = fixture["data"]["security"]
    security = Security(sec_data)
    
    assert security.is_vpn is False
    assert security.is_tor is False
    assert security.is_threat == "low"
    assert isinstance(security.is_vpn, bool)
    assert isinstance(security.is_tor, bool)


@test("IPWhoData with all nested types")
def test_ipwho_data_full():
    from src.types import IPWhoData
    data = IPWhoData(fixture["data"])
    
    assert data.ip == "202.21.42.9"
    assert data.geo_location is not None
    assert data.timezone is not None
    assert data.flag is not None
    assert data.currency is not None
    assert data.connection is not None
    assert data.user_agent is not None
    assert data.security is not None


@test("Currency type mapping")
def test_currency_type():
    from src.types import Currency
    curr_data = fixture["data"]["currency"]
    currency = Currency(curr_data)
    
    assert currency.code == "INR"
    assert currency.symbol == "₹"
    assert currency.name == "Indian Rupee"
    assert currency.name_plural == "Indian rupees"
    assert currency.hex_unicode == "20b9"


@test("UserAgent composite type")
def test_user_agent_type():
    ua_data = fixture["data"]["userAgent"]
    from src.types import UserAgent
    user_agent = UserAgent(ua_data)
    
    assert user_agent.browser.name == "Chrome"
    assert user_agent.browser.version == "143.0.0.0"
    assert user_agent.engine.name == "Blink"
    assert user_agent.os.name == "macOS"
    assert user_agent.device.type == "desktop"
    assert user_agent.cpu.architecture == "Unknown"


@test("Handle camelCase and snake_case fields")
def test_field_name_conversion():
    # Test with snake_case
    data = {
        "continent": "Europe",
        "continent_code": "EU",
        "country": "France",
        "country_code": "FR"
    }
    location = GeoLocation(data)
    assert location.continent == "Europe"
    assert location.continent_code == "EU"
    
    # Test mixed camelCase
    data2 = {
        "continentCode": "AS",
        "continent": "Asia",
        "country": "Japan",
        "countryCode": "JP"
    }
    location2 = GeoLocation(data2)
    assert location2.continent_code == "AS"


@test("Null/None field handling")
def test_none_fields():
    data = {
        "continent": "Asia",
        "continent_code": "AS",
        "country": "India",
        "country_code": "IN",
        "city": None,
        "postal_code": None,
        "dial_code": None
    }
    location = GeoLocation(data)
    assert location.city is None
    assert location.postal_code is None
    assert location.dial_code is None


@test("API response wrapper type")
def test_api_response_type():
    from src.types import IPWhoAPIResponse
    response = IPWhoAPIResponse(fixture)
    
    assert response.success is True
    assert response.message is None
    assert response.data is not None
    assert response.data.ip == "202.21.42.9"


@test("Extra fields handling in types")
def test_extra_fields():
    data = {
        "name": "Chrome",
        "version": "143.0.0.0",
        "custom_field": "custom_value"
    }
    from src.types import BrowserInfo
    browser = BrowserInfo(data)
    
    assert browser.name == "Chrome"
    assert browser.version == "143.0.0.0"
    assert browser.extra.get("custom_field") == "custom_value"


# Run all tests
if __name__ == "__main__":
    print("\n" + "="*60)
    print("IPWho Python SDK - Test Suite")
    print("="*60 + "\n")
    
    # Collect all test functions
    test_functions = [obj for name, obj in list(globals().items()) if name.startswith("test_")]
    
    # Run tests
    for test_func in test_functions:
        test_func()
    
    # Print summary
    success = results.summary()
    
    sys.exit(0 if success else 1)
