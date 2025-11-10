# WebScreenShot Quick Start Guide

Get started with WebScreenShot in 5 minutes.

## 1. Install (1 minute)

```bash
# Create virtual environment
python3.11 -m venv webenv
source webenv/bin/activate

# Install
pip install -r requirements.txt
python -m playwright install chromium
```

## 2. First Screenshot (1 minute)

### Option A: Command Line (Easiest)

```bash
python web_screenshot.py --url https://example.com -o screenshot.png
```

### Option B: Python Code

```python
from web_screenshot import WebScreenShot

with WebScreenShot() as shot:
    shot.capture("https://example.com", "screenshot.png")
```

## 3. Common Use Cases

### Capture Full Page (Single Screenshot)

```bash
python web_screenshot.py --url https://example.com --full-page -o full.png
```

### Capture Multiple Pages

```bash
python web_screenshot.py --url https://example.com --multi-page -o pages_dir
```

### Multiple URLs (Python)

```python
from web_screenshot import WebScreenShot

urls = ["https://example.com", "https://github.com"]

with WebScreenShot() as shot:
    for i, url in enumerate(urls, 1):
        shot.capture(url, f"screenshot_{i}.png")
```

### Custom Settings

```python
from web_screenshot import WebScreenShot

with WebScreenShot(
    navigation_timeout=30000,  # 30 seconds
    viewport_width=1920,       # Desktop size
    viewport_height=1080,
    verbose=True              # Show debug info
) as shot:
    shot.capture("https://example.com", "output.png")
```

## 4. Configuration File

Create `config.yaml`:

```yaml
browser:
  headless: true

timeouts:
  navigation_timeout: 60000
  final_wait: 3000

viewport:
  width: 1920
  height: 1080
```

Use it:

```python
from web_screenshot import WebScreenShot

with WebScreenShot(config_file="config.yaml") as shot:
    shot.capture("https://example.com", "output.png")
```

## 5. Troubleshooting

### First capture works, second fails?
✅ **Always use context managers:**
```python
# ✓ CORRECT
with WebScreenShot() as shot:
    shot.capture("https://example.com", "1.png")
    shot.capture("https://github.com", "2.png")

# ✗ WRONG - Don't reuse after exiting with block
shot = WebScreenShot()
```

### Screenshot is blank?
✅ **Check URL and enable verbose mode:**
```python
with WebScreenShot(verbose=True) as shot:
    success = shot.capture("https://example.com", "output.png")
    print(f"Success: {success}")
```

### Installation fails?
✅ **Use Python 3.11:**
```bash
python3.11 -m venv webenv
```

See [INSTALLATION.md](INSTALLATION.md) for more help.

## 6. CLI Help

```bash
python web_screenshot.py --help
```

Output:
```
usage: web_screenshot.py [-h] --url URL [--output OUTPUT]
                         [--full-page] [--multi-page]

required arguments:
  --url URL, -u URL     URL of the webpage to capture

optional arguments:
  -h, --help            Show this help message
  --output OUTPUT, -o OUTPUT
                        Output path/directory
  --full-page, -f       Capture entire page
  --multi-page, -m      Capture multiple pages
```

## 7. Next Steps

- Read full docs: [WEB_SCREENSHOT_README.md](WEB_SCREENSHOT_README.md)
- Installation guide: [INSTALLATION.md](INSTALLATION.md)
- See examples: `python web_screenshot_example.py`
- Check updates: [UPDATES.md](UPDATES.md)

## 8. Common Commands Cheat Sheet

```bash
# Basic screenshot
python web_screenshot.py -u https://example.com -o out.png

# Full page (no viewport height limit)
python web_screenshot.py -u https://example.com -f -o full.png

# Multiple pages (paginated)
python web_screenshot.py -u https://example.com -m -o pages

# Verbose output (for debugging)
python web_screenshot.py -u https://example.com -o out.png

# From Python
python << 'EOF'
from web_screenshot import WebScreenShot
with WebScreenShot() as shot:
    shot.capture("https://example.com", "out.png")
EOF
```

## Tips & Tricks

### Speed up captures
```python
WebScreenShot(
    navigation_timeout=30000,  # Reduce from 60000
    final_wait=2000            # Reduce from 5000
)
```

### Reuse browser for many URLs
```python
with WebScreenShot() as shot:
    for url in [url1, url2, url3, ...]:  # Saves time!
        shot.capture(url, f"{url}.png")
```

### Capture very large pages
```python
WebScreenShot(
    viewport_auto_adjust=True,     # Fits entire page
    max_viewport_height=100000     # Handle huge pages
)
```

---

**Having issues?** Check [INSTALLATION.md](INSTALLATION.md) troubleshooting section or read the full [WEB_SCREENSHOT_README.md](WEB_SCREENSHOT_README.md).

**Want to contribute?** See [WEB_SCREENSHOT_README.md](WEB_SCREENSHOT_README.md#contributing).
