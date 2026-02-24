# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-02-24

### Added

- Initial public release
- Full support for IPWho Geolocation API
- Type-safe dataclass definitions for all response types:
  - `GeoLocation` - Geographic location data
  - `Timezone` - Timezone information
  - `Connection` - Network connection details
  - `Security` - Security threat information
  - `Flag` - Country flag data
  - `Currency` - Currency information
  - `UserAgent` - User agent parsing data
  - `IPWhoData` - Complete API response wrapper
- Core client methods:
  - `get_location()` - Retrieve geolocation for IP
  - `get_timezone()` - Retrieve timezone for IP
  - `get_connection()` - Retrieve connection info for IP
  - `get_security()` - Retrieve security data for IP
  - `get_ip()` - Get complete data for specific IP
  - `get_me()` - Get complete data for caller's IP
- Support for both camelCase and snake_case field names
- Automatic field mapping from API response
- Comprehensive error handling
- Full test suite with mock fixtures
- Complete documentation and examples
- MIT License
