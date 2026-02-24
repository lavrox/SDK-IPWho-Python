"""
Type definitions for the IPWho Python SDK.
"""

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Optional


@dataclass
class BrowserInfo:
    """Browser information."""
    name: str = ""
    version: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def __init__(self, data: Dict[str, Any] = None):
        if data is None:
            data = {}
        self.name = data.get("name", "")
        self.version = data.get("version")
        # Store extra fields not explicitly defined
        defined_keys = {"name", "version"}
        self.extra = {k: v for k, v in data.items() if k not in defined_keys}


@dataclass
class EngineInfo:
    """Engine information."""
    name: str = ""
    version: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def __init__(self, data: Dict[str, Any] = None):
        if data is None:
            data = {}
        self.name = data.get("name", "")
        self.version = data.get("version")
        defined_keys = {"name", "version"}
        self.extra = {k: v for k, v in data.items() if k not in defined_keys}


@dataclass
class OSInfo:
    """Operating System information."""
    name: str = ""
    version: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def __init__(self, data: Dict[str, Any] = None):
        if data is None:
            data = {}
        self.name = data.get("name", "")
        self.version = data.get("version")
        defined_keys = {"name", "version"}
        self.extra = {k: v for k, v in data.items() if k not in defined_keys}


@dataclass
class DeviceInfo:
    """Device information."""
    type: Optional[str] = None
    vendor: Optional[str] = None
    model: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def __init__(self, data: Dict[str, Any] = None):
        if data is None:
            data = {}
        self.type = data.get("type")
        self.vendor = data.get("vendor")
        self.model = data.get("model")
        defined_keys = {"type", "vendor", "model"}
        self.extra = {k: v for k, v in data.items() if k not in defined_keys}


@dataclass
class CPUInfo:
    """CPU information."""
    architecture: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def __init__(self, data: Dict[str, Any] = None):
        if data is None:
            data = {}
        self.architecture = data.get("architecture")
        defined_keys = {"architecture"}
        self.extra = {k: v for k, v in data.items() if k not in defined_keys}


@dataclass
class UserAgent:
    """User Agent information."""
    browser: BrowserInfo
    engine: EngineInfo
    os: OSInfo
    device: DeviceInfo
    cpu: CPUInfo
    extra: Dict[str, Any] = field(default_factory=dict)

    def __init__(self, data: Dict[str, Any] = None):
        if data is None:
            data = {}
        self.browser = BrowserInfo(data.get("browser", {}))
        self.engine = EngineInfo(data.get("engine", {}))
        self.os = OSInfo(data.get("os", {}))
        self.device = DeviceInfo(data.get("device", {}))
        self.cpu = CPUInfo(data.get("cpu", {}))
        defined_keys = {"browser", "engine", "os", "device", "cpu"}
        self.extra = {k: v for k, v in data.items() if k not in defined_keys}


@dataclass
class Flag:
    """Flag information."""
    flag_icon: str = ""
    flag_unicode: str = ""
    extra: Dict[str, Any] = field(default_factory=dict)

    def __init__(self, data: Dict[str, Any] = None):
        if data is None:
            data = {}
        # Handle both camelCase and snake_case
        self.flag_icon = data.get("flagIcon") or data.get("flag_icon") or data.get("flag_Icon", "")
        self.flag_unicode = data.get("flagUnicode") or data.get("flag_unicode", "")
        defined_keys = {"flagIcon", "flag_icon", "flag_Icon", "flagUnicode", "flag_unicode"}
        self.extra = {k: v for k, v in data.items() if k not in defined_keys}


@dataclass
class Currency:
    """Currency information."""
    code: str = ""
    symbol: str = ""
    name: str = ""
    name_plural: Optional[str] = None
    hex_unicode: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def __init__(self, data: Dict[str, Any] = None):
        if data is None:
            data = {}
        self.code = data.get("code", "")
        self.symbol = data.get("symbol", "")
        self.name = data.get("name", "")
        self.name_plural = data.get("namePlural") or data.get("name_plural")
        self.hex_unicode = data.get("hexUnicode") or data.get("hex_unicode")
        defined_keys = {"code", "symbol", "name", "namePlural", "name_plural", "hexUnicode", "hex_unicode"}
        self.extra = {k: v for k, v in data.items() if k not in defined_keys}


@dataclass
class GeoLocation:
    """Geolocation information."""
    continent: str = ""
    continent_code: str = ""
    country: str = ""
    country_code: str = ""
    capital: Optional[str] = None
    region: Optional[str] = None
    region_code: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    dial_code: Optional[str] = None
    is_in_eu: Optional[bool] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    accuracy_radius: Optional[int] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def __init__(self, data: Dict[str, Any] = None):
        if data is None:
            data = {}
        self.continent = data.get("continent", "")
        self.continent_code = data.get("continentCode") or data.get("continent_code", "")
        self.country = data.get("country", "")
        self.country_code = data.get("countryCode") or data.get("country_code", "")
        self.capital = data.get("capital")
        self.region = data.get("region")
        self.region_code = data.get("regionCode") or data.get("region_code")
        self.city = data.get("city")
        self.postal_code = data.get("postal_Code") or data.get("postalCode") or data.get("postal_code")
        self.dial_code = data.get("dial_code") or data.get("dialCode")
        self.is_in_eu = data.get("is_in_eu") or data.get("isInEu")
        self.latitude = data.get("latitude")
        self.longitude = data.get("longitude")
        self.accuracy_radius = data.get("accuracy_radius") or data.get("accuracyRadius")
        
        defined_keys = {
            "continent", "continentCode", "continent_code", "country", "countryCode",
            "country_code", "capital", "region", "regionCode", "region_code", "city",
            "postalCode", "postal_Code", "postal_code", "dial_code", "dialCode", "isInEu",
            "is_in_eu", "latitude", "longitude", "accuracy_radius", "accuracyRadius"
        }
        self.extra = {k: v for k, v in data.items() if k not in defined_keys}


@dataclass
class Timezone:
    """Timezone information."""
    time_zone: str = ""
    abbr: Optional[str] = None
    offset: Optional[int] = None
    is_dst: Optional[bool] = None
    utc: Optional[str] = None
    current_time: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def __init__(self, data: Dict[str, Any] = None):
        if data is None:
            data = {}
        self.time_zone = data.get("time_zone") or data.get("timeZone", "")
        self.abbr = data.get("abbr")
        self.offset = data.get("offset")
        self.is_dst = data.get("is_dst") or data.get("isDst")
        self.utc = data.get("utc")
        self.current_time = data.get("current_time") or data.get("currentTime")
        
        defined_keys = {"time_zone", "timeZone", "abbr", "offset", "is_dst", "isDst", "utc", "current_time", "currentTime"}
        self.extra = {k: v for k, v in data.items() if k not in defined_keys}


@dataclass
class Connection:
    """Connection information."""
    asn_number: Optional[int] = None
    asn_org: Optional[str] = None
    isp: Optional[str] = None
    org: Optional[str] = None
    domain: Optional[str] = None
    connection_type: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def __init__(self, data: Dict[str, Any] = None):
        if data is None:
            data = {}
        self.asn_number = data.get("asn_number") or data.get("asnNumber")
        self.asn_org = data.get("asn_org") or data.get("asnOrg")
        self.isp = data.get("isp")
        self.org = data.get("org")
        self.domain = data.get("domain")
        self.connection_type = data.get("connection_type") or data.get("connectionType")
        
        defined_keys = {"asn_number", "asnNumber", "asn_org", "asnOrg", "isp", "org", "domain", "connection_type", "connectionType"}
        self.extra = {k: v for k, v in data.items() if k not in defined_keys}


@dataclass
class Security:
    """Security information."""
    is_vpn: Optional[bool] = None
    is_tor: Optional[bool] = None
    is_threat: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def __init__(self, data: Dict[str, Any] = None):
        if data is None:
            data = {}
        self.is_vpn = data.get("is_vpn") or data.get("isVpn")
        self.is_tor = data.get("is_tor") or data.get("isTor")
        self.is_threat = data.get("is_threat") or data.get("isThreat")
        
        defined_keys = {"is_vpn", "isVpn", "is_tor", "isTor", "is_threat", "isThreat"}
        self.extra = {k: v for k, v in data.items() if k not in defined_keys}


@dataclass
class IPWhoData:
    """Main IPWho API response data."""
    ip: str = ""
    geo_location: Optional[GeoLocation] = None
    timezone: Optional[Timezone] = None
    flag: Optional[Flag] = None
    currency: Optional[Currency] = None
    connection: Optional[Connection] = None
    user_agent: Optional[UserAgent] = None
    security: Optional[Security] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def __init__(self, data: Dict[str, Any] = None):
        if data is None:
            data = {}
        self.ip = data.get("ip", "")
        
        # Handle both geoLocation and geo_location
        geo_data = data.get("geoLocation") or data.get("geo_location")
        self.geo_location = GeoLocation(geo_data) if geo_data else None
        
        # Handle timezone
        tz_data = data.get("timezone") or data.get("time_zone")
        self.timezone = Timezone(tz_data) if tz_data else None
        
        # Handle flag
        flag_data = data.get("flag")
        self.flag = Flag(flag_data) if flag_data else None
        
        # Handle currency
        currency_data = data.get("currency")
        self.currency = Currency(currency_data) if currency_data else None
        
        # Handle connection
        connection_data = data.get("connection")
        self.connection = Connection(connection_data) if connection_data else None
        
        # Handle userAgent
        ua_data = data.get("userAgent") or data.get("user_agent")
        self.user_agent = UserAgent(ua_data) if ua_data else None
        
        # Handle security
        security_data = data.get("security")
        self.security = Security(security_data) if security_data else None
        
        defined_keys = {
            "ip", "geoLocation", "geo_location", "timezone", "time_zone", "flag",
            "currency", "connection", "userAgent", "user_agent", "security"
        }
        self.extra = {k: v for k, v in data.items() if k not in defined_keys}


@dataclass
class IPWhoAPIResponse:
    """IPWho API Response wrapper."""
    success: bool = False
    message: Optional[str] = None
    data: Optional[IPWhoData] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def __init__(self, data: Dict[str, Any] = None):
        if data is None:
            data = {}
        self.success = data.get("success", False)
        self.message = data.get("message")
        
        response_data = data.get("data")
        self.data = IPWhoData(response_data) if response_data else None
        
        defined_keys = {"success", "message", "data"}
        self.extra = {k: v for k, v in data.items() if k not in defined_keys}
