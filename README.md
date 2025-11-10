# WebScreenShot

A powerful tool for capturing full-page screenshots of websites using Playwright.

## 📚 Documentation

| Document | Purpose | Best For |
|----------|---------|----------|
| **[QUICKSTART.md](docs/QUICKSTART.md)** ⚡ | 5-minute setup | First-time users |
| **[INSTALLATION.md](docs/INSTALLATION.md)** 🔧 | Detailed setup guide | Installation help |
| **[WEB_SCREENSHOT_README.md](docs/WEB_SCREENSHOT_README.md)** 📖 | Full feature reference | Complete documentation |
| **[UPDATES.md](docs/UPDATES.md)** 📝 | Recent changes | What's new |
| **[QUALITY_REPORT.md](docs/QUALITY_REPORT.md)** 📊 | Code quality audit | Repository quality |

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

## 📁 Repository Structure

```
WebShot/
├── web_screenshot.py          # Main tool implementation
├── web_screenshot_example.py  # Usage examples
├── web_screenshot_config.yaml # Configuration template
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── .gitignore                 # Git ignore rules
└── docs/
    ├── QUICKSTART.md          # 5-minute setup guide
    ├── INSTALLATION.md        # Detailed installation
    ├── WEB_SCREENSHOT_README.md # Complete reference
    ├── UPDATES.md             # Recent changes
    └── QUALITY_REPORT.md      # Code quality audit
```

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

## 🚀 Getting Started

**First time?** → Start with [QUICKSTART.md](docs/QUICKSTART.md) (5 minutes)

**Need help installing?** → See [INSTALLATION.md](docs/INSTALLATION.md) (step-by-step)

**Want all details?** → Read [WEB_SCREENSHOT_README.md](docs/WEB_SCREENSHOT_README.md) (complete reference)

**Looking for what changed?** → Check [UPDATES.md](docs/UPDATES.md) (recent fixes)

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

See [UPDATES.md](docs/UPDATES.md) for complete details.

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

## 💡 Quick Command Reference

```bash
# Basic screenshot
python web_screenshot.py --url https://example.com -o out.png

# Full page (auto-adjusted viewport)
python web_screenshot.py --url https://example.com --full-page -o full.png

# Multi-page capture
python web_screenshot.py --url https://example.com --multi-page -o pages/
```

For more options: `python web_screenshot.py --help`

## 📞 Need Help?

- **Installation issues?** → [INSTALLATION.md](docs/INSTALLATION.md#troubleshooting)
- **How to use?** → [QUICKSTART.md](docs/QUICKSTART.md)
- **Advanced usage?** → [WEB_SCREENSHOT_README.md](docs/WEB_SCREENSHOT_README.md)
- **What changed?** → [UPDATES.md](docs/UPDATES.md)

## 📄 License

MIT License - See [WEB_SCREENSHOT_README.md](docs/WEB_SCREENSHOT_README.md#license)

## 🤝 Contributing

Contributions welcome! See [WEB_SCREENSHOT_README.md](docs/WEB_SCREENSHOT_README.md#contributing)

---

**Current Version:** 0.53+
**Last Updated:** November 10, 2024
**Status:** ✅ Fully Tested and Production Ready
