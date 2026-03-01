# IPWho (ipwho.org) Python SDK

[![Python version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/) [![license](https://img.shields.io/github/license/lavrox/SDK-IPWho-Python?style=flat-square)](https://github.com/lavrox/SDK-IPWho-Python/blob/main/LICENSE)

Official Python client for the IPWho Geolocation API — fetch geolocation, timezone, connection and security information for IP addresses using a lightweight, type-safe SDK.

## Installation

Install via pip:

```bash
pip install ipwho-ip-geolocation-api
```

Or install from source:

```bash
git clone https://github.com/lavrox/SDK-IPWho-Python.git
cd sdk-ipwho-python
pip install -e .
```

## Quick Start

```python
from src import IPWho

client = IPWho(api_key="your-api-key")

# Get caller's location (uses your IP by default)
import asyncio

location = asyncio.run(client.get_location())
print(location)

# Get location for a specific IP
location = asyncio.run(client.get_location("8.8.8.8"))
print(f"Country: {location.country}")
print(f"City: {location.city}")
```

Example minimal response (normalized):

```python
{
    "continent": "North America",
    "continent_code": "NA",
    "country": "United States",
    "country_code": "US",
    "capital": "Washington",
    "region": "California",
    "region_code": "CA",
    "city": "San Francisco",
    "latitude": 37.7749,
    "longitude": -122.4194,
    "postal_code": "94105",
    "dial_code": "+1",
    "is_in_eu": False
}
```

## API Reference

### IPWho Client

The main client class for interacting with the IPWho API.

#### Constructor

```python
client = IPWho(api_key: str)
```

- **api_key** (str): Your IPWho API key. Required.
- **Raises**: `ValueError` if API key is empty.

#### Methods

##### `get_location(ip: Optional[str] = None) -> Optional[GeoLocation]`

Get geolocation data for an IP address.

```python
location = await client.get_location("8.8.8.8")
if location:
    print(f"Country: {location.country}")
```

##### `get_timezone(ip: Optional[str] = None) -> Optional[Timezone]`

Get timezone data for an IP address.

```python
timezone = await client.get_timezone("8.8.8.8")
if timezone:
    print(f"Time Zone: {timezone.time_zone}")
    print(f"Offset: {timezone.offset}")
```

##### `get_connection(ip: Optional[str] = None) -> Optional[Connection]`

Get connection/network data for an IP address.

```python
connection = await client.get_connection("8.8.8.8")
if connection:
    print(f"ISP: {connection.isp}")
    print(f"ASN: {connection.asn_number}")
```

##### `get_security(ip: Optional[str] = None) -> Optional[Security]`

Get security information for an IP address.

```python
security = await client.get_security("8.8.8.8")
if security:
    print(f"Is VPN: {security.is_vpn}")
    print(f"Is Tor: {security.is_tor}")
```

##### `get_ip(ip: str) -> IPWhoData`

Get complete data for a specific IP address.

```python
data = await client.get_ip("8.8.8.8")
print(f"IP: {data.ip}")
print(f"Country: {data.geo_location.country}")
print(f"ISP: {data.connection.isp}")
```

##### `get_me() -> IPWhoData`

Get complete data for the caller's IP address.

```python
data = await client.get_me()
print(f"Your IP: {data.ip}")
print(f"Your location: {data.geo_location.city}, {data.geo_location.country}")
```

## Type Definitions

### GeoLocation

```python
@dataclass
class GeoLocation:
    continent: str
    continent_code: str
    country: str
    country_code: str
    capital: Optional[str]
    region: Optional[str]
    region_code: Optional[str]
    city: Optional[str]
    postal_code: Optional[str]
    dial_code: Optional[str]
    is_in_eu: Optional[bool]
    latitude: Optional[float]
    longitude: Optional[float]
    accuracy_radius: Optional[int]
```

### Timezone

```python
@dataclass
class Timezone:
    time_zone: str
    abbr: Optional[str]
    offset: Optional[int]
    is_dst: Optional[bool]
    utc: Optional[str]
    current_time: Optional[str]
```

### Connection

```python
@dataclass
class Connection:
    asn_number: Optional[int]
    asn_org: Optional[str]
    isp: Optional[str]
    org: Optional[str]
    domain: Optional[str]
    connection_type: Optional[str]
```

### Security

```python
@dataclass
class Security:
    is_vpn: Optional[bool]
    is_tor: Optional[bool]
    is_threat: Optional[str]
```

### IPWhoData

The main response object containing all available data:

```python
@dataclass
class IPWhoData:
    ip: str
    geo_location: Optional[GeoLocation]
    timezone: Optional[Timezone]
    flag: Optional[Flag]
    currency: Optional[Currency]
    connection: Optional[Connection]
    user_agent: Optional[UserAgent]
    security: Optional[Security]
```

## Testing

Run the test suite:

```bash
pytest tests/
```

Run tests with coverage:

```bash
pytest --cov=src tests/
```

## Troubleshooting

### "API Key is required" Error

Make sure you're providing a valid API key:

```python
# ❌ Wrong
client = IPWho("")

# ✅ Correct
client = IPWho("your-api-key")
```

### No data returned

Some fields may be `None` if they're not available for a given IP:

```python
location = await client.get_location("8.8.8.8")
if location and location.city:
    print(f"City: {location.city}")
else:
    print("City data not available")
```

## Changelog

### v1.0.0 (2026-02-24)

- Initial release
- Support for geolocation, timezone, connection, and security lookups
- Type-safe dataclass definitions
- Comprehensive test suite
- Full parity with TypeScript and PHP SDKs

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- Contact: [Contact](https://www.ipwho.org/contact)
- GitHub Issues: https://github.com/lavrox/SDK-IPWho-Python/issues
- Documentation: [Documentation](https://github.com/lavrox/SDK-IPWho-Python)
