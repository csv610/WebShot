# WebScreenShot - Full-Page Website Screenshot Tool

A powerful and flexible tool for capturing full-page screenshots of websites using Playwright.

## Features

- ✅ URL validation with blank image fallback
- ✅ Configurable timeouts and delays
- ✅ Custom viewport support
- ✅ **NEW: Viewport auto-adjustment** - Capture entire page in one screenshot
- ✅ **NEW: YAML configuration file support**
- ✅ Reusable browser instance for multiple screenshots
- ✅ Logging support for debugging
- ✅ Handles lazy-loaded images
- ✅ Context manager support
- ✅ Command-line interface

## Installation

### Prerequisites

- **Python 3.11 or later** (Python 3.14 recommended for best compatibility)
- macOS, Linux, or Windows

### Setup Steps

1. **Create a virtual environment** (recommended):
```bash
python3.11 -m venv webenv
source webenv/bin/activate  # On Windows: webenv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install playwright==1.55.0 pyyaml pillow
```

3. **Install Playwright browsers**:
```bash
python -m playwright install chromium
```

### Requirements File

The `requirements.txt` contains:
```
playwright==1.55.0
Pillow==10.1.0
PyYAML==6.0.1
```

**Note:** We recommend using Playwright 1.55.0 or later. Earlier versions (1.40.0) may have compatibility issues on macOS.

## Quick Start

### Basic Usage

```python
from web_screenshot import WebScreenShot

with WebScreenShot(verbose=True) as screenshot:
    screenshot.capture("https://example.com", "output.png")
```

### Command Line Usage

```bash
# Basic screenshot (default viewport)
python web_screenshot.py --url https://example.com

# Specify output file
python web_screenshot.py --url https://example.com --output screenshot.png

# Capture entire page in one screenshot (auto-adjust viewport)
python web_screenshot.py --url https://example.com --full-page --output full_page.png

# Capture multiple pages as separate PNG files
python web_screenshot.py --url https://example.com --multi-page --output screenshots_dir

# Alternative short options
python web_screenshot.py -u https://example.com -o output.png
python web_screenshot.py -u https://example.com -f  # full-page
python web_screenshot.py -u https://example.com -m  # multi-page
```

## Configuration File

Create a `web_screenshot_config.yaml` file to configure default settings:

```yaml
# Browser settings
browser:
  headless: true

# Timeout settings (milliseconds)
timeouts:
  navigation_timeout: 60000
  action_timeout: 60000
  final_wait: 5000

# Scroll settings
scroll:
  delay: 1.0  # seconds

# Request throttling settings
throttling:
  page_delay: 2.0  # Delay between capturing pages (seconds)
  request_delay: 0.5  # Delay between requests (seconds)
  enable_request_throttling: false  # Disabled by default (causes event loop issues)

# Viewport settings
viewport:
  width: null  # null = browser default
  height: null
  auto_adjust: false  # Set to true to capture entire page in one screenshot
  max_width: 7680     # Maximum width when auto-adjusting
  max_height: 43200   # Maximum height when auto-adjusting

# Logging settings
logging:
  verbose: false
  level: "WARNING"
```

## Viewport Auto-Adjustment Feature

### What is it?

The viewport auto-adjustment feature allows you to capture the **entire webpage in a single screenshot** by automatically adjusting the browser viewport to match the page dimensions. This is different from the traditional full-page screenshot approach which stitches multiple viewport captures together.

### Why use it?

**Benefits:**
- ✅ Captures the page exactly as it would render at that size
- ✅ No scrolling artifacts
- ✅ Faster for many pages
- ✅ Better for pages with fixed/sticky elements
- ✅ Ideal for responsive design testing

**When to use traditional full-page (auto_adjust=False):**
- ❌ Very tall pages (>43200px by default)
- ❌ Pages with dynamic content that changes based on viewport size
- ❌ When you want to see the page at a specific viewport size

### How to use

#### Method 1: Enable in code

```python
with WebScreenShot(viewport_auto_adjust=True, verbose=True) as screenshot:
    screenshot.capture("https://example.com", "output.png")
```

#### Method 2: Enable in config file

```yaml
viewport:
  auto_adjust: true
```

#### Method 3: Override per capture

```python
with WebScreenShot(viewport_auto_adjust=False) as screenshot:
    # This capture uses auto-adjust
    screenshot.capture("https://example.com", "auto.png", auto_adjust=True)

    # This capture uses traditional scrolling
    screenshot.capture("https://example.com", "traditional.png", auto_adjust=False)
```

#### Method 4: Command line

```bash
python web_screenshot.py https://example.com --auto-adjust
```

## Advanced Usage Examples

### Multiple Screenshots with Reused Browser

```python
from web_screenshot import WebScreenShot

urls = [
    "https://example.com",
    "https://github.com",
    "https://stackoverflow.com"
]

with WebScreenShot(verbose=True) as screenshot:
    for i, url in enumerate(urls, 1):
        screenshot.capture(url, f"screenshot_{i}.png")
```

### Custom Configuration

```python
from web_screenshot import WebScreenShot

screenshot = WebScreenShot(
    navigation_timeout=30000,
    action_timeout=30000,
    scroll_delay=0.5,
    final_wait=2000,
    viewport_width=1920,
    viewport_height=1080,
    headless=True,
    verbose=True
)

with screenshot:
    screenshot.capture("https://example.com", "output.png")
```

### Using Config File

```python
from web_screenshot import WebScreenShot

with WebScreenShot(config_file="web_screenshot_config.yaml") as screenshot:
    screenshot.capture("https://example.com", "output.png")
```

## API Reference

### WebScreenShot Class

#### Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `navigation_timeout` | int | 60000 | Timeout for page navigation (ms) |
| `action_timeout` | int | 60000 | Timeout for page actions (ms) |
| `scroll_delay` | float | 1.0 | Delay between scroll actions (seconds) |
| `final_wait` | int | 5000 | Final wait after network idle (ms) |
| `viewport_width` | int\|None | None | Custom viewport width (pixels) |
| `viewport_height` | int\|None | None | Custom viewport height (pixels) |
| `viewport_auto_adjust` | bool | False | Auto-adjust viewport to page size |
| `max_viewport_width` | int | 7680 | Max width when auto-adjusting |
| `max_viewport_height` | int | 43200 | Max height when auto-adjusting |
| `headless` | bool | True | Run browser in headless mode |
| `verbose` | bool | False | Enable verbose logging |
| `config_file` | str\|None | None | Path to YAML config file |

#### Methods

##### `capture(url, output_path=None, auto_adjust=None)`

Capture a full-page screenshot.

**Parameters:**
- `url` (str): URL of the webpage to capture
- `output_path` (str, optional): Path to save screenshot (default: auto-generated timestamp)
- `auto_adjust` (bool, optional): Override instance auto_adjust setting

**Returns:**
- `bool`: True if successful, False if URL invalid

##### `open()`

Manually open the browser instance.

##### `close()`

Manually close the browser instance.

## Command-Line Options

```
usage: web_screenshot.py [-h] --url URL [--output OUTPUT]
                         [--full-page] [--multi-page]

required arguments:
  --url URL, -u URL     URL of the webpage to capture

optional arguments:
  -h, --help            Show this help message and exit
  --output OUTPUT, -o OUTPUT
                        Output path/directory for screenshot(s)
  --full-page, -f       Capture entire webpage in one screenshot by
                        auto-adjusting viewport
  --multi-page, -m      Capture all pages as separate PNG files in a
                        directory
```

### Examples
```bash
# Basic viewport-based screenshot
python web_screenshot.py --url https://example.com

# Save to custom location
python web_screenshot.py -u https://example.com -o my_screenshot.png

# Full-page screenshot (auto-adjusted viewport)
python web_screenshot.py -u https://example.com --full-page -o full.png

# Multi-page capture
python web_screenshot.py -u https://example.com --multi-page -o pages_dir
```

## Troubleshooting

### Playwright Installation Issues

**Problem:** `Failed to build 'Pillow' when getting requirements to build wheel`

**Solution:** Use Python 3.11 instead of Python 3.14:
```bash
python3.11 -m venv webenv
source webenv/bin/activate
pip install -r requirements.txt
```

### Chromium Crashes on macOS

**Problem:** Browser crashes with "Target page, context or browser has been closed"

**Solution:** Upgrade Playwright to 1.55.0 or later:
```bash
pip install --upgrade playwright==1.55.0
python -m playwright install chromium
```

### Multiple Captures Fail with Asyncio Error

**Problem:** `It looks like you are using Playwright Sync API inside the asyncio loop`

**Solution:** Always use context managers for proper browser lifecycle management:
```python
# ✓ CORRECT
with WebScreenShot() as shot:
    shot.capture("https://example.com", "output.png")

# ✗ WRONG
shot = WebScreenShot()
shot.capture("https://example.com", "output.png")
```

### Screenshots are blank
- Check URL validity (enable `verbose=True` to see validation errors)
- Increase `navigation_timeout` and `action_timeout`
- Enable verbose mode to see what's happening
- Try disabling headless mode to see the browser in action

### Page content is cut off
- Try enabling `viewport_auto_adjust` to capture the entire page
- Increase `max_viewport_height` if the page is very tall (default: 43200px)
- Adjust `scroll_delay` and `final_wait` for slower-loading pages

### Images not loading
- Increase `final_wait` time (default: 5000ms)
- Images are automatically loaded when using traditional scrolling (auto_adjust=False)
- Try increasing `scroll_delay` (default: 1.0s)

### Request Throttling Issues

**Problem:** Requests time out when `enable_request_throttling: true`

**Solution:** Request throttling is **disabled by default** (0.53+) as it can block Playwright's event loop. If you need it, use it carefully or increase timeouts significantly.

## Examples

See `web_screenshot_example.py` for complete working examples including:
- Basic screenshot capture
- Using configuration files
- Auto-adjusting viewport
- Custom viewport dimensions
- Multiple screenshots with reused browser
- Per-capture setting overrides

## Recent Updates (v0.53+)

### Fixed Issues
- ✅ **macOS Chromium Compatibility** - Upgraded Playwright from 1.40.0 to 1.55.0
- ✅ **Event Loop Blocking** - Disabled request throttling by default (was causing asyncio issues)
- ✅ **Browser Lifecycle Management** - Added proper cleanup in context managers
- ✅ **Multiple Captures** - Fixed asyncio loop conflicts when reusing browser instance

### Testing

The tool has been thoroughly tested with:
- ✅ Basic screenshot capture
- ✅ Multiple captures with browser reuse
- ✅ Invalid URL handling
- ✅ Multi-page capture
- ✅ CLI operations (basic, full-page, multi-page)
- ✅ Custom viewports and configurations

Run tests with:
```bash
python << 'EOF'
from web_screenshot import WebScreenShot
import os

# Test 1: Basic capture
with WebScreenShot() as shot:
    success = shot.capture("https://example.com", "test.png")
    assert success and os.path.exists("test.png")

# Test 2: Multiple captures
with WebScreenShot() as shot:
    for i, url in enumerate(["https://example.com", "https://httpbin.org"]):
        success = shot.capture(url, f"test_{i}.png")
        assert success

# Test 3: Invalid URL handling
with WebScreenShot() as shot:
    success = shot.capture("invalid://url", "blank.png")
    assert not success and os.path.exists("blank.png")

print("All tests passed!")
EOF
```

## Performance Tips

1. **Reuse browser instance** for multiple captures:
   ```python
   with WebScreenShot() as shot:
       for url in urls:
           shot.capture(url, f"output_{urls.index(url)}.png")
   ```

2. **Adjust timeouts** based on page load speed:
   ```python
   shot = WebScreenShot(
       navigation_timeout=30000,  # Faster pages
       final_wait=2000           # Reduce wait time
   )
   ```

3. **Use viewport auto-adjust** for large pages:
   ```python
   with WebScreenShot(viewport_auto_adjust=True) as shot:
       shot.capture("https://example.com", "output.png")
   ```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Changelog

### v0.53+ (Current)
- Upgraded Playwright to 1.55.0
- Disabled request throttling by default
- Fixed asyncio event loop issues
- Added comprehensive testing suite
- Improved documentation and troubleshooting guide

### v0.50
- Initial release with auto-adjust viewport and YAML config support
