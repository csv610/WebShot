"""
Example usage of the WebScreenShot class demonstrating various features.
"""

from web_screenshot import WebScreenShot

def example_basic_screenshot():
    """Basic screenshot capture."""
    print("Example 1: Basic screenshot capture")
    with WebScreenShot(verbose=True) as screenshot:
        success = screenshot.capture("https://example.com", "example_basic.png")
        if success:
            print("✓ Screenshot saved successfully\n")
        else:
            print("✗ Failed to capture screenshot\n")


def example_with_config():
    """Screenshot using configuration file."""
    print("Example 2: Using configuration file")
    with WebScreenShot(config_file="web_screenshot_config.yaml") as screenshot:
        success = screenshot.capture("https://example.com", "example_config.png")
        if success:
            print("✓ Screenshot with config saved successfully\n")
        else:
            print("✗ Failed to capture screenshot\n")


def example_auto_adjust_viewport():
    """Screenshot with auto-adjusted viewport (entire page in one screenshot)."""
    print("Example 3: Auto-adjust viewport to page dimensions")
    with WebScreenShot(viewport_auto_adjust=True, verbose=True) as screenshot:
        success = screenshot.capture("https://example.com", "example_auto_adjust.png")
        if success:
            print("✓ Auto-adjusted screenshot saved successfully\n")
        else:
            print("✗ Failed to capture screenshot\n")


def example_custom_viewport():
    """Screenshot with custom viewport dimensions."""
    print("Example 4: Custom viewport dimensions")
    with WebScreenShot(
        viewport_width=1920,
        viewport_height=1080,
        verbose=True
    ) as screenshot:
        success = screenshot.capture("https://example.com", "example_custom_viewport.png")
        if success:
            print("✓ Custom viewport screenshot saved successfully\n")
        else:
            print("✗ Failed to capture screenshot\n")


def example_multiple_screenshots():
    """Capture multiple screenshots with the same browser instance."""
    print("Example 5: Multiple screenshots with reused browser instance")
    urls = [
        "https://example.com",
        "https://www.wikipedia.org",
        "https://github.com"
    ]

    with WebScreenShot(verbose=True) as screenshot:
        for i, url in enumerate(urls, 1):
            output_path = f"example_multi_{i}.png"
            success = screenshot.capture(url, output_path)
            if success:
                print(f"✓ Captured {url}")
            else:
                print(f"✗ Failed to capture {url}")
    print()


def example_override_auto_adjust():
    """Override auto-adjust setting per capture."""
    print("Example 6: Override auto-adjust per capture")
    # Instance has auto_adjust=False, but we enable it for specific capture
    with WebScreenShot(viewport_auto_adjust=False, verbose=True) as screenshot:
        # This capture will use auto-adjust
        screenshot.capture("https://example.com", "example_override_on.png", auto_adjust=True)
        # This capture will use traditional scrolling method
        screenshot.capture("https://example.com", "example_override_off.png", auto_adjust=False)
    print()


if __name__ == "__main__":
    print("=" * 70)
    print("WebScreenShot Usage Examples")
    print("=" * 70)
    print()

    # Run examples (comment out the ones you don't want to run)
    example_basic_screenshot()
    # example_with_config()  # Requires config file
    # example_auto_adjust_viewport()
    # example_custom_viewport()
    # example_multiple_screenshots()
    # example_override_auto_adjust()

    print("=" * 70)
    print("Examples completed!")
    print("=" * 70)
