# DreamBolt Changelog

## [Unreleased] - 2025-06-20

### 🔥 Major Feature: Firebolt Core Integration
- **NEW**: Added free, self-hosted Firebolt Core integration with Docker support
- **NEW**: PostgreSQL-compliant SQL interface for analytics queries
- **NEW**: Auto-detection between Managed Firebolt and Firebolt Core modes
- **NEW**: CLI commands for Firebolt Core management (`firebolt setup`, `status`, `query`, `stop`)
- **NEW**: Zero-cost analytics solution - no cloud accounts or usage limits required
- **ENHANCED**: Rich status reporting with detailed container and connection information
- **ADDED**: Docker SDK and psycopg2-binary dependencies for Core functionality

### 🐳 Docker Integration
- **NEW**: Automatic Firebolt Core container deployment and management
- **NEW**: Data persistence with local volume mounting
- **NEW**: Container lifecycle management (start, stop, status monitoring)
- **NEW**: Health checks and readiness waiting with timeout handling
- **ADDED**: Memory limit configuration and restart policies

### 🔧 Enhanced Configuration
- **NEW**: `FIREBOLT_USE_CORE` environment variable for mode selection
- **NEW**: Firebolt Core specific configuration options (port, container name, image)
- **UPDATED**: Environment template with detailed Firebolt Core setup instructions
- **IMPROVED**: Auto-fallback from Managed to Core mode when credentials unavailable

### 📊 CLI Enhancements  
- **NEW**: `dreambolt firebolt setup` - One-command Firebolt Core infrastructure setup
- **NEW**: `dreambolt firebolt status` - Detailed status and connection information
- **NEW**: `dreambolt firebolt query` - Execute SQL queries with optional CSV export
- **NEW**: `dreambolt firebolt stop` - Clean container shutdown
- **ENHANCED**: Status command now shows backend mode and Docker availability
- **IMPROVED**: Rich table formatting for all status displays

### 🛠️ Backend Architecture
- **NEW**: Multi-backend support (Core, Managed, Simulation)
- **NEW**: Context manager for PostgreSQL connections with proper cleanup
- **NEW**: Batch INSERT operations for efficient data loading
- **NEW**: Automatic schema generation from pandas DataFrames
- **IMPROVED**: Error handling with specific Docker and PostgreSQL error messages

### 📚 Documentation Updates
- **REWRITTEN**: README.md with Firebolt Core as the primary integration
- **NEW**: Comprehensive setup and usage examples for all user types
- **NEW**: Architecture diagram showing Core integration
- **NEW**: Workflow examples for Data Scientists, Analytics Teams, and ML Engineers
- **UPDATED**: Environment template with detailed configuration guidance

### 🔧 Critical Fixes
- **BREAKING FIX**: Restored Python 3.13 compatibility with conservative dependency pinning (Option A)
- **FIXED**: Moto v5 breaking change by pinning to moto 4.x (preserves `mock_s3` imports)
- **FIXED**: Trio/HTTPCore Python 3.13 incompatibility by pinning trio to 0.22-0.25 range
- **ADDED**: Explicit trio dependency to requirements.txt
- **ADDED**: Comprehensive critical fix documentation in `reports/critical_fix_summary.md`
- **ADDED**: Verification script `verify_critical_fixes.py` for testing fixes

### 📚 Documentation
- **UPDATED**: README.md with Python 3.13 compatibility notice
- **ADDED**: Future upgrade path documentation (Option B) with detailed implementation plan
- **ADDED**: Dependency rationale and migration timeline

### 🧪 Testing
- **RESTORED**: Full test suite functionality with moto 4.x
- **VERIFIED**: All CLI commands working with new dependency stack
- **ADDED**: Automated verification script for critical fixes

### 📦 Dependencies
```diff
# Python 3.13 Compatibility Stack (Option A: Conservative)
+ trio>=0.22.0,<0.26.0               # Explicit trio dependency, stable pre-3.13 range
+ httpcore>=1.0.0,<1.1.0             # Stable version compatible with trio 0.22-0.25
+ httpx>=0.27.0,<0.28.0              # Compatible with httpcore 1.0.x

# Firebolt Core Integration (Self-hosted)
+ docker>=6.1.0,<8.0.0               # Docker SDK for Python
+ psycopg2-binary>=2.9.0,<3.0.0      # PostgreSQL adapter (binary distribution)

# Testing & Development
- moto[s3]>=5.1.0,<6.0.0
+ moto[s3]>=4.2.0,<5.0.0             # CRITICAL FIX: Pin to v4.x (preserves mock_s3 imports)
```

### 🎯 Migration Notes
- **Current**: Using Option A (Conservative) for immediate stability
- **Future**: Option B (Latest versions) documented for next major release
- **Impact**: Zero breaking changes to existing code
- **Verification**: Run `python verify_critical_fixes.py` to test fixes
- **Firebolt Core**: Run `python -m cli firebolt setup` for free analytics setup

---

## Previous Releases

### [1.0.0] - 2025-06-19
- Initial DreamBolt release with S3 integration
- CLI interface with Typer
- DataDreamer synthesis pipeline
- Firebolt database integration 