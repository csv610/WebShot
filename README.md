# WebScreenShot Documentation

WebScreenShot is a powerful tool for capturing full-page screenshots of websites using Playwright.

## 📚 Documentation Structure

### 1. **[QUICKSTART.md](QUICKSTART.md)** - Start Here! ⚡
- Get started in 5 minutes
- Basic usage examples
- Common use cases
- Quick troubleshooting
- **Best for:** First-time users

### 2. **[INSTALLATION.md](INSTALLATION.md)** - Setup Guide 🔧
- System requirements
- Step-by-step installation
- Platform-specific instructions (macOS, Linux, Windows)
- Verification and testing
- Detailed troubleshooting
- **Best for:** Setting up the tool

### 3. **[WEB_SCREENSHOT_README.md](WEB_SCREENSHOT_README.md)** - Full Documentation 📖
- Complete features overview
- API reference
- Configuration file options
- Advanced usage examples
- Performance tips
- Changelog
- **Best for:** Detailed usage and configuration

### 4. **[UPDATES.md](UPDATES.md)** - What's New 📝
- Recent fixes and improvements
- Files updated
- Test results
- Known issues fixed
- Breaking changes (if any)
- **Best for:** Understanding recent changes

## 🚀 Quick Start

```bash
# Install
python3.11 -m venv webenv
source webenv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium

# Use
python web_screenshot.py --url https://example.com -o screenshot.png
```

Or in Python:

```python
from web_screenshot import WebScreenShot

with WebScreenShot() as shot:
    shot.capture("https://example.com", "screenshot.png")
```

## 📋 Files Overview

| File | Purpose | Last Updated |
|------|---------|--------------|
| `web_screenshot.py` | Main tool | Nov 2024 |
| `web_screenshot_example.py` | Usage examples | Nov 2024 |
| `web_screenshot_config.yaml` | Config template | Nov 2024 |
| `requirements.txt` | Dependencies | Nov 2024 |
| **QUICKSTART.md** | 5-minute setup | Nov 2024 |
| **INSTALLATION.md** | Detailed setup | Nov 2024 |
| **WEB_SCREENSHOT_README.md** | Full reference | Nov 2024 |
| **UPDATES.md** | Recent changes | Nov 2024 |
| **README.md** | This file | Nov 2024 |

## ✨ Features

✅ Full-page website screenshots
✅ Command-line interface
✅ Python library API
✅ Configurable timeouts and delays
✅ Custom viewport support
✅ Viewport auto-adjustment (entire page in one screenshot)
✅ Multi-page capture (paginated screenshots)
✅ YAML configuration file support
✅ Reusable browser instance
✅ Lazy-loaded image handling
✅ Context manager support
✅ Verbose logging

## 🔍 Choose Your Path

### I want to...

#### ...get started quickly
→ Read [QUICKSTART.md](QUICKSTART.md)

#### ...install WebScreenShot
→ Read [INSTALLATION.md](INSTALLATION.md)

#### ...understand all features
→ Read [WEB_SCREENSHOT_README.md](WEB_SCREENSHOT_README.md)

#### ...see what changed
→ Read [UPDATES.md](UPDATES.md)

#### ...use the CLI
```bash
python web_screenshot.py --help
```

#### ...use it in Python code
See examples in [QUICKSTART.md](QUICKSTART.md) or run:
```bash
python web_screenshot_example.py
```

#### ...troubleshoot issues
Check the troubleshooting sections in:
- [QUICKSTART.md](QUICKSTART.md#5-troubleshooting)
- [INSTALLATION.md](INSTALLATION.md#troubleshooting)
- [WEB_SCREENSHOT_README.md](WEB_SCREENSHOT_README.md#troubleshooting)

## ✅ Recent Improvements

### Version 0.53+ (Current)
- ✅ Playwright upgraded to 1.55.0 (fixed macOS Chromium issues)
- ✅ Request throttling disabled by default (fixed event loop blocking)
- ✅ Comprehensive testing completed (all tests passing)
- ✅ Documentation significantly improved
- ✅ Installation guide created
- ✅ Quick start guide created

### Key Fixes
- ✅ Fixed "Target page, context or browser has been closed" errors
- ✅ Fixed asyncio event loop conflicts with multiple captures
- ✅ Fixed Playwright 1.40.0 compatibility issues on macOS

See [UPDATES.md](UPDATES.md) for complete details.

## 🧪 Testing Status

All tests passing:
- ✅ Basic screenshot capture
- ✅ Multiple captures with browser reuse
- ✅ Invalid URL handling
- ✅ Multi-page capture
- ✅ CLI operations
- ✅ Custom configurations

## 📖 System Requirements

- **Python:** 3.11 or later (3.11 recommended)
- **OS:** macOS 11+, Linux (Ubuntu 18+), Windows 10+
- **Disk:** 500 MB (for Playwright browsers)

## 🎯 Next Steps

1. **New user?** Start with [QUICKSTART.md](QUICKSTART.md)
2. **Need to install?** Go to [INSTALLATION.md](INSTALLATION.md)
3. **Want all details?** Read [WEB_SCREENSHOT_README.md](WEB_SCREENSHOT_README.md)
4. **Check recent changes?** See [UPDATES.md](UPDATES.md)

## 📞 Support

For help:
1. Check the relevant troubleshooting section in the docs
2. Review [INSTALLATION.md](INSTALLATION.md#troubleshooting) for common issues
3. See [WEB_SCREENSHOT_README.md](WEB_SCREENSHOT_README.md#troubleshooting) for advanced issues

## 📄 License

MIT License - See [WEB_SCREENSHOT_README.md](WEB_SCREENSHOT_README.md#license)

## 🤝 Contributing

Contributions welcome! See [WEB_SCREENSHOT_README.md](WEB_SCREENSHOT_README.md#contributing)

---

**Current Version:** 0.53+
**Last Updated:** November 10, 2024
**Status:** ✅ Fully Tested and Production Ready
