"""
IPWho Python SDK - Client implementation.
"""

import requests
from typing import Optional
from .types import IPWhoData, GeoLocation, Timezone, Connection, Security


class IPWho:
    """IPWho API client for geolocation, timezone, connection, and security data."""

    def __init__(self, api_key: str):
        """
        Initialize the IPWho client.

        Args:
            api_key: The API key for authentication. Required.

        Raises:
            ValueError: If API key is empty or None.
        """
        if not api_key:
            raise ValueError("API Key is required")
        self.api_key = api_key
        self.base_url = "https://api.ipwho.org/v1"

    def _fetcher(self, endpoint: str) -> dict:
        """
        Make an HTTP request to the API.

        Args:
            endpoint: The API endpoint (e.g., '/ip/8.8.8.8' or '/me')

        Returns:
            The parsed JSON response data.

        Raises:
            Exception: If the API request fails or returns an error.
        """
        separator = "&" if "?" in endpoint else "?"
        url = f"{self.base_url}{endpoint}{separator}"

        response = requests.get(
            url,
            headers={"X-API-Key": self.api_key}
        )

        body = response.json()

        if not body.get("success"):
            raise Exception(body.get("message", "Request failed"))

        return body.get("data", {})

    def _request(self, ip: Optional[str] = None) -> IPWhoData:
        """
        Make a request to the API for IP data.

        Args:
            ip: Optional IP address. If not provided, uses caller's IP.

        Returns:
            IPWhoData object with the response.
        """
        endpoint = f"/ip/{ip}" if ip else "/me"
        data = self._fetcher(endpoint)
        return IPWhoData(data)

    async def get_location(self, ip: Optional[str] = None) -> Optional[GeoLocation]:
        """
        Get geolocation data for an IP address.

        Args:
            ip: Optional IP address. If not provided, uses caller's IP.

        Returns:
            GeoLocation object or None if not available.
        """
        data = self._request(ip)
        return data.geo_location if data.geo_location else None

    async def get_timezone(self, ip: Optional[str] = None) -> Optional[Timezone]:
        """
        Get timezone data for an IP address.

        Args:
            ip: Optional IP address. If not provided, uses caller's IP.

        Returns:
            Timezone object or None if not available.
        """
        data = self._request(ip)
        return data.timezone if data.timezone else None

    async def get_connection(self, ip: Optional[str] = None) -> Optional[Connection]:
        """
        Get connection data for an IP address.

        Args:
            ip: Optional IP address. If not provided, uses caller's IP.

        Returns:
            Connection object or None if not available.
        """
        data = self._request(ip)
        return data.connection if data.connection else None

    async def get_security(self, ip: Optional[str] = None) -> Optional[Security]:
        """
        Get security data for an IP address.

        Args:
            ip: Optional IP address. If not provided, uses caller's IP.

        Returns:
            Security object or None if not available.
        """
        data = self._request(ip)
        return data.security if data.security else None

    async def get_ip(self, ip: str) -> IPWhoData:
        """
        Get all data for a specific IP address.

        Args:
            ip: The IP address to look up.

        Returns:
            IPWhoData object with the response.
        """
        return self._request(ip)

    async def get_me(self) -> IPWhoData:
        """
        Get all data for the caller's IP address.

        Returns:
            IPWhoData object with the response.
        """
        return self._request()
