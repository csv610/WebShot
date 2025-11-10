# WebScreenShot Installation Guide

Complete step-by-step guide for installing and setting up WebScreenShot.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Verification](#verification)
4. [Troubleshooting](#troubleshooting)
5. [Platform-Specific Instructions](#platform-specific-instructions)

## System Requirements

### Minimum Requirements

- **Python 3.11** or later
- **pip** package manager
- 500 MB disk space (for Playwright browsers and dependencies)

### Recommended

- **Python 3.11** - Best compatibility with all dependencies
- **Python 3.13-3.14** - Latest versions also supported
- macOS 11+ / Ubuntu 18+ / Windows 10+

### Not Supported

- **Python 3.10 or earlier** - Pillow dependency issues
- **Python 3.14** (with outdated Pillow) - Requires Python 3.11 for venv

## Installation Steps

### Step 1: Verify Python Version

```bash
python3 --version
# or
python --version
```

Expected output: `Python 3.11.x` or later

### Step 2: Create Virtual Environment

**Recommended:** Use Python 3.11 explicitly:

```bash
python3.11 -m venv webenv
```

**Activate the virtual environment:**

- **macOS/Linux:**
  ```bash
  source webenv/bin/activate
  ```

- **Windows (Command Prompt):**
  ```bash
  webenv\Scripts\activate
  ```

- **Windows (PowerShell):**
  ```bash
  webenv\Scripts\Activate.ps1
  ```

You should see `(webenv)` prefix in your terminal.

### Step 3: Update pip

```bash
pip install --upgrade pip setuptools wheel
```

### Step 4: Install Dependencies

**Option A: Using requirements.txt (Recommended)**

```bash
pip install -r requirements.txt
```

**Option B: Manual installation**

```bash
pip install playwright==1.55.0
pip install Pillow==10.1.0
pip install PyYAML==6.0.1
```

### Step 5: Install Playwright Browsers

```bash
python -m playwright install chromium
```

This downloads the Chromium browser binary (~200 MB).

### Step 6: Verify Installation

```bash
python << 'EOF'
from web_screenshot import WebScreenShot
print("✓ WebScreenShot imported successfully")

shot = WebScreenShot()
print("✓ WebScreenShot instance created")

shot.open()
print("✓ Browser launched successfully")
shot.close()
print("✓ Installation successful!")
EOF
```

## Verification

### Quick Test

Run a simple screenshot:

```bash
python web_screenshot.py --url https://example.com --output test.png
```

Expected output:
```
Screenshot saved to test.png
```

### Check File

```bash
ls -lh test.png
# Should show a file > 10 KB
```

## Troubleshooting

### Issue: "No module named 'playwright'"

**Solution:** Ensure you're in the activated virtual environment:
```bash
source webenv/bin/activate  # macOS/Linux
```

### Issue: "Failed to build 'Pillow' wheel"

**Solution:** Use Python 3.11:
```bash
python3.11 -m venv webenv
source webenv/bin/activate
pip install -r requirements.txt
```

### Issue: "Timeout waiting for browser to start"

**Solution:** Check if Chromium is installed:
```bash
python -m playwright install chromium --with-deps
```

### Issue: "command not found: python3.11"

**Solution:** Install Python 3.11 first:
- **macOS (Homebrew):** `brew install python@3.11`
- **Ubuntu/Debian:** `sudo apt install python3.11 python3.11-venv`
- **Windows:** Download from [python.org](https://www.python.org/downloads/)

### Issue: "ModuleNotFoundError: No module named 'PIL'"

**Solution:** Reinstall Pillow:
```bash
pip install --force-reinstall Pillow==10.1.0
```

### Issue: "Playwright Sync API inside the asyncio loop"

**Solution:** Always use context managers:
```python
# ✓ CORRECT
with WebScreenShot() as shot:
    shot.capture("https://example.com", "output.png")

# ✗ WRONG - Don't do this
shot = WebScreenShot()
shot.capture("https://example.com", "output.png")
```

## Platform-Specific Instructions

### macOS

```bash
# Using Homebrew (recommended)
brew install python@3.11

# Create venv
python3.11 -m venv webenv
source webenv/bin/activate

# Install dependencies
pip install -r requirements.txt
python -m playwright install chromium

# Run test
python web_screenshot.py --url https://example.com -o test.png
```

### Linux (Ubuntu/Debian)

```bash
# Install Python 3.11
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev

# Create venv
python3.11 -m venv webenv
source webenv/bin/activate

# Install system dependencies for Playwright
sudo apt install libnss3 libxss1 libappindicator1 libindicator7

# Install dependencies
pip install -r requirements.txt
python -m playwright install chromium --with-deps

# Run test
python web_screenshot.py --url https://example.com -o test.png
```

### Windows (Command Prompt)

```batch
REM Install Python 3.11 from https://www.python.org/downloads/
REM Or use: choco install python311

REM Create venv
python -m venv webenv
webenv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt
python -m playwright install chromium

REM Run test
python web_screenshot.py --url https://example.com -o test.png
```

## Next Steps

After successful installation:

1. **Read the main README:**
   ```bash
   cat WEB_SCREENSHOT_README.md
   ```

2. **Run the examples:**
   ```bash
   python web_screenshot_example.py
   ```

3. **Try the CLI:**
   ```bash
   python web_screenshot.py --help
   python web_screenshot.py --url https://example.com --full-page -o full.png
   ```

4. **Create a config file:**
   ```bash
   cp web_screenshot_config.yaml my_config.yaml
   # Edit my_config.yaml as needed
   ```

## Environment Variables

Optional environment variables for Playwright:

```bash
# Use custom browser cache location
export PLAYWRIGHT_BROWSERS_PATH=~/.cache/playwright

# Disable browser telemetry
export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=0

# Run with these
python web_screenshot.py --url https://example.com
```

## Uninstallation

To remove WebScreenShot and all dependencies:

```bash
# Deactivate the virtual environment
deactivate

# Remove the virtual environment
rm -rf webenv

# Or on Windows
rmdir /s webenv
```

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review the [platform-specific instructions](#platform-specific-instructions)
3. Check the main [WEB_SCREENSHOT_README.md](WEB_SCREENSHOT_README.md)
4. See [Playwright documentation](https://playwright.dev/python/)

## Version Information

Current recommended versions:

| Package | Version | Purpose |
|---------|---------|---------|
| Python | 3.11+ | Runtime |
| playwright | 1.55.0+ | Browser automation |
| Pillow | 10.1.0+ | Image handling |
| PyYAML | 6.0.1+ | Config file parsing |

Last Updated: November 2024
