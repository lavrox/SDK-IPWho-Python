"""
Test suite for IPWho Python SDK.
"""

import pytest
import json
from unittest.mock import patch, MagicMock
from pathlib import Path

from src.client import IPWho
from src.types import GeoLocation, Timezone, Connection, Security


# Load fixture
fixture_path = Path(__file__).parent.parent / "src" / "response.json"
with open(fixture_path, "r") as f:
    fixture = json.load(f)


class TestIPWhoSDK:
    """Test suite for IPWho SDK."""

    def setup_method(self):
        """Setup for each test."""
        self.sdk = IPWho("sk_test_123")

    def test_throws_error_if_api_key_missing(self):
        """Test that API key is required."""
        with pytest.raises(ValueError, match="API Key is required"):
            IPWho("")

    def test_throws_error_if_api_key_none(self):
        """Test that None API key raises error."""
        with pytest.raises(ValueError, match="API Key is required"):
            IPWho(None)

    @patch("src.client.requests.get")
    def test_format_url_correctly_for_get_ip(self, mock_get):
        """Test that getIp formats URL correctly."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True, "data": {"ip": "8.8.8.8"}}
        mock_get.return_value = mock_response

        self.sdk._request("8.8.8.8")

        # Verify the URL contains the IP
        called_url = mock_get.call_args[0][0]
        assert "/ip/8.8.8.8" in called_url
        
        # Verify headers contain API key
        called_headers = mock_get.call_args[1]["headers"]
        assert called_headers["X-API-Key"] == "sk_test_123"

    @patch("src.client.requests.get")
    def test_format_url_correctly_for_get_me(self, mock_get):
        """Test that getMe formats URL correctly."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True, "data": {"ip": "192.168.1.1"}}
        mock_get.return_value = mock_response

        self.sdk._request()

        # Verify the URL contains /me
        called_url = mock_get.call_args[0][0]
        assert "/me" in called_url

    @patch("src.client.requests.get")
    def test_get_location_maps_correctly(self, mock_get):
        """Test that getLocation maps data correctly."""
        mock_response = MagicMock()
        mock_response.json.return_value = fixture
        mock_get.return_value = mock_response

        import asyncio
        location = asyncio.run(self.sdk.get_location("202.21.42.9"))

        assert location is not None
        assert location.continent == "Asia"
        assert location.continent_code == "AS"
        assert location.country == "India"
        assert location.country_code == "IN"
        assert location.capital == "New Delhi"
        assert location.region == "Telangana"
        assert location.region_code == "TS"
        assert location.city is None
        assert location.postal_code is None
        assert location.dial_code == "+91"
        assert location.is_in_eu is False
        assert location.latitude == 17.3843
        assert location.longitude == 78.4583
        assert location.accuracy_radius == 1000

    @patch("src.client.requests.get")
    def test_get_timezone_maps_correctly(self, mock_get):
        """Test that getTimezone maps data correctly."""
        mock_response = MagicMock()
        mock_response.json.return_value = fixture
        mock_get.return_value = mock_response

        import asyncio
        tz = asyncio.run(self.sdk.get_timezone())

        assert tz is not None
        assert tz.time_zone == "Asia/Kolkata"
        assert tz.abbr == "IST"
        assert tz.offset == 19800
        assert tz.is_dst is False
        assert tz.utc == "+05:30"
        assert tz.current_time == "2026-02-06T11:02:50+05:30"

    @patch("src.client.requests.get")
    def test_get_connection_maps_correctly(self, mock_get):
        """Test that getConnection maps data correctly."""
        mock_response = MagicMock()
        mock_response.json.return_value = fixture
        mock_get.return_value = mock_response

        import asyncio
        conn = asyncio.run(self.sdk.get_connection())

        assert conn is not None
        assert conn.asn_number == 24186
        assert conn.asn_org == "RailTel Corporation of India Ltd"
        assert conn.isp == "RailTel Corporation Of India Ltd."
        assert conn.org == "RailTel Corporation Of India Ltd."
        assert conn.domain is None
        assert conn.connection_type == "Cable/DSL"

    @patch("src.client.requests.get")
    def test_get_security_maps_correctly(self, mock_get):
        """Test that getSecurity maps data correctly."""
        mock_response = MagicMock()
        mock_response.json.return_value = fixture
        mock_get.return_value = mock_response

        import asyncio
        sec = asyncio.run(self.sdk.get_security())

        assert sec is not None
        assert sec.is_vpn is False
        assert sec.is_tor is False
        assert sec.is_threat == "low"

    @patch("src.client.requests.get")
    def test_get_me_returns_raw_api_payload(self, mock_get):
        """Test that getMe returns the raw API payload."""
        mock_response = MagicMock()
        mock_response.json.return_value = fixture
        mock_get.return_value = mock_response

        import asyncio
        data = asyncio.run(self.sdk.get_me())

        assert data is not None
        assert data.ip == "202.21.42.9"
        assert data.timezone is not None
        assert data.security is not None

    @patch("src.client.requests.get")
    def test_exposes_currency_details(self, mock_get):
        """Test that currency details are exposed."""
        mock_response = MagicMock()
        mock_response.json.return_value = fixture
        mock_get.return_value = mock_response

        import asyncio
        data = asyncio.run(self.sdk.get_me())

        assert data.currency is not None
        assert data.currency.code == "INR"
        assert data.currency.symbol == "₹"
        assert data.currency.name == "Indian Rupee"

    @patch("src.client.requests.get")
    def test_exposes_geo_location_nested_data(self, mock_get):
        """Test that geolocation data is exposed."""
        mock_response = MagicMock()
        mock_response.json.return_value = fixture
        mock_get.return_value = mock_response

        import asyncio
        data = asyncio.run(self.sdk.get_me())

        assert data.geo_location is not None
        assert data.geo_location.continent == "Asia"
        assert data.geo_location.country == "India"
        assert data.geo_location.capital == "New Delhi"
        assert data.geo_location.latitude == 17.3843
        assert data.geo_location.longitude == 78.4583

    @patch("src.client.requests.get")
    def test_exposes_user_agent_metadata(self, mock_get):
        """Test that userAgent metadata is exposed."""
        mock_response = MagicMock()
        mock_response.json.return_value = fixture
        mock_get.return_value = mock_response

        import asyncio
        data = asyncio.run(self.sdk.get_me())

        assert data.user_agent is not None
        assert data.user_agent.browser.name == "Chrome"
        assert data.user_agent.browser.version == "143.0.0.0"
        assert data.user_agent.engine.name == "Blink"
        assert data.user_agent.os.name == "macOS"
        assert data.user_agent.device.type == "desktop"
        assert data.user_agent.cpu.architecture == "Unknown"

    @patch("src.client.requests.get")
    def test_handles_api_error(self, mock_get):
        """Test that API errors are handled correctly."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": False,
            "message": "Invalid API key"
        }
        mock_get.return_value = mock_response

        with pytest.raises(Exception, match="Invalid API key"):
            self.sdk._request()
